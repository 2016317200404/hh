#-*-coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from login import models
from login import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            cid = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(id=cid)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())
# 登出
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


# 主页
def index(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        sname = request.session.get('user_name')
        lessons_list = models.lessons.objects.exclude(name=sname)
        lesson_list = models.reserved.objects.exclude(name=sname)
        list = []  ## 空列表
        list2 =[]
        for ls in lessons_list:
            cname=ls.name
            cmargin=ls.lessonsmargin
            if cmargin==0:
                list2.append(cmargin)
            for le in lesson_list:
                lname=le.name
                if cname==lname:
                    list.append(lname)  ## 使用 append() 添加元素
        lessons_list = models.lessons.objects.exclude(name=sname).exclude(name__in=list).exclude(lessonsmargin__in=list2)

        return render(request, 'login/index.html', {'lessons_list': lessons_list})
    else:
        return redirect("/login/")


#已选查看
def reserved(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        name = request.session.get('user_name')
        reserved_list = models.reserved.objects.filter(xname=name).exclude(mark=1)

        return render(request, 'login/reserved.html', {'reserved_list': reserved_list})
    else:
        return redirect("/index/")


#按课程名或教师名搜索
def search(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        sname = request.session.get('user_name')
        list=[]
        list2 = []
        list.append(sname)
        lesson_list = models.lessons.objects.exclude(name=sname)
        for ls in lesson_list:
            cmargin = ls.lessonsmargin
            if cmargin == 0:
                list2.append(cmargin)
        less_list = models.reserved.objects.filter(xname=sname)
        for ls in less_list:
            name=ls.name
            list.append(name)
        if request.method == 'GET':
            q = request.GET.get('q')
            if q:

                lessons_list = (models.lessons.objects.filter(name__contains=q) or models.lessons.objects.filter(lessonsname__contains=q) or models.lessons.objects.filter( detaltime__contains=q)).exclude(name__in=list).exclude(lessonsmargin__in=list2)

            return render(request,'login/index.html', {'lessons_list': lessons_list})
    else:
        return redirect("/index/")


def unreserved(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        if request.method == 'GET':
            q = request.GET.get('q')
            if not q:
                return redirect("/reserved/")

            lesson_obj = models.reserved.objects.filter(id=q)
            for lesson in lesson_obj:
                name=lesson.name
                lessons_obj = models.lessons.objects.filter(name=name)
                for chakan in lessons_obj:
                    margin = chakan.lessonsmargin
                    lessonsmargin=margin+1
                    models.lessons.objects.filter(name=name).update(lessonsmargin=lessonsmargin)
                    lesson_obj.delete()
            return redirect("/reserved/")
    else:
        return redirect("/login/")


def choose(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        if request.method == 'GET':
            q = request.GET.get('q')
            if not q:
                return redirect("/index/")
            lesson_obj = models.lessons.objects.filter(id=q)
            for i in lesson_obj:
                margin = i.lessonsmargin
                if margin>0:
                    return render(request, 'login/choise.html', {'lessons_list': lesson_obj})
                else:
                    return redirect("/index/")
    else:
        return redirect("/login/")


def add(request):
    if request.session.get('is_login', None):
        request.session.set_expiry(900)
        xname = request.session.get('user_name')
        if request.method == 'POST':
            q = request.POST.get('q')

            if not q:
                return redirect("/index/")
            lesson_obj = models.lessons.objects.filter(id=q)
            less_obj = models.reserved.objects.filter(xname=xname)
            for m in lesson_obj:
                name = m.name
                lessonsname = m.lessonsname
                whatday = m.whatday
                detaltime = m.detaltime
                palce = m.place
                comprise = m.comprise
                whichweek = request.POST.get('w')
                xid = request.session.get('user_id')
                if len(less_obj):
                    for les in less_obj:
                        vname=les.name
                        if vname!=name:
                            models.reserved.objects.create(xid=xid, xname=xname, name=name, lessonsname=lessonsname,
                                                           whatday=whatday, detaltime=detaltime, whichweek=whichweek,
                                                           place=palce, comprise=comprise,mark=0)
                            lessonsmargin = m.lessonsmargin
                            lessonsmargin = lessonsmargin - 1
                            models.lessons.objects.filter(name=name).update(lessonsmargin=lessonsmargin)
                            return redirect("/reserved/")
                        else:
                            return redirect("/index/")
                else:
                    models.reserved.objects.create(xid=xid, xname=xname, name=name, lessonsname=lessonsname,
                                                   whatday=whatday, detaltime=detaltime, whichweek=whichweek,
                                                   place=palce, comprise=comprise, mark=0)
                    lessonsmargin = m.lessonsmargin
                    lessonsmargin = lessonsmargin - 1
                    models.lessons.objects.filter(name=name).update(lessonsmargin=lessonsmargin)
                    return redirect("/reserved/")
    else:
        return redirect("/login/")


def evaluate(request,id):
    if request.session.get('is_login', None):
        if not id:
             return redirect("/reserved/")
        return render(request, 'login/evaluate.html', {'cdid': id})
    else:
        return redirect("/login/")


def addevaluate(request):
    if request.session.get('is_login', None):
        if request.method == 'POST':
            name = ''
            lsname = ''
            xname = request.session.get('user_name')
            q = request.POST.get('pjid')
            lesson_obj = models.reserved.objects.filter(id=q)
            for lesson in lesson_obj:
                name = lesson.name
                # 获取被听老师姓名
                lsname = lesson.lessonsname
            q1 = request.POST.get('x1')
            q2 = request.POST.get('x2')
            q3 = request.POST.get('x3')
            q4 = request.POST.get('x4')
            q5 = request.POST.get('x5')
            q6 = request.POST.get('x6')
            q7 = request.POST.get('x7')
            q8 = request.POST.get('x8')
            q9 = request.POST.get('x9')
            q10 = request.POST.get('x10')
            q11 = request.POST.get('x11')
            q12 = request.POST.get('x12')
            q13 = request.POST.get('x13')
            q14 = request.POST.get('x14')
            if q1 and q2 and q3 and q4 and q5 and q6 and q7 and q8 and q9 and q10 and q11 and q12 and q13 and q14:
                q1 = float(q1)
                q2 = float(q2)
                q3 = float(q3)
                q4 = float(q4)
                q5 = float(q5)
                q6 = float(q6)
                q7 = float(q7)
                q8 = float(q8)
                q9 = float(q9)
                q10 = float(q10)
                q11 = float(q11)
                q12 = float(q12)
                q13 = float(q13)
                q14 = float(q14)
                score = q1*1.0+q2*1.0+q3*1.0+q4*1.0+q5*2.0+q6*1.4+q7*1.6+q9*2.0+q8*2.0+q10*1.4+q11*1.4+q12*1.2+q13*2.0+q14*1.0
                score = round(score, 3)

                hz = models.pjhz.objects.all()
                if not hz:
                    # 汇总表为空
                    models.pjhz.objects.create(name=name, xname1=xname, grade1=score, xname2="", grade2=0.0,xname3="", grade3=0.0,xname4="", grade4=0.0,xname5="", grade5=0.0,xname6="", grade6=0.0,xname7="", grade7=0.0,xname8="", grade8=0.0,xname9="", grade9=0.0,xname10="", grade10=0.0)
                    models.reserved.objects.filter(id=q).update(mark=1)
                    models.pjjl.objects.create(name=name, xname=xname, lessonsname=lsname, item1=q1, item2=q2, item3=q3, item4=q4, item5=q5,
                                               item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                               item11=q11, item12=q12, item13=q13, item14=q14, )
                else:
                    for hzlist in hz:
                        if hzlist.name == name:
                            xid = hzlist.id
                            lls = models.pjhz.objects.filter(id=xid)
                            for llss in lls:
                                if not llss.xname2:
                                    if xname ==llss.xname1:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname2=xname, grade2=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname3:
                                    if xname == llss.xname2:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname3=xname, grade3=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname,item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')
                                elif not llss.xname4:
                                    if xname == llss.xname3:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname4=xname, grade4=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname5:
                                    if xname == llss.xname4:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname5=xname, grade5=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname6:
                                    if xname == llss.xname5:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname6=xname, grade6=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname, lessonsname=lsname,item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname7:
                                    if xname == llss.xname6:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname7=xname, grade7=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname8:
                                    if xname == llss.xname7:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname8=xname, grade8=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname, lessonsname=lsname,item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                                elif not llss.xname9:
                                    if xname == llss.xname8:
                                        return redirect('/haveevaluated/')
                                    models.pjhz.objects.filter(id=xid).update(xname9=xname, grade9=score)
                                    models.reserved.objects.filter(id=q).update(mark=1)
                                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3,
                                                           item4=q4, item5=q5,
                                                           item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                                           item11=q11, item12=q12, item13=q13, item14=q14, )
                                    return redirect('/haveevaluated/')

                    models.pjhz.objects.create(name=name, xname1=xname, grade1=score, xname2="", grade2=0.0,
                                                       xname3="", grade3=0.0, xname4="", grade4=0.0, xname5="",
                                                       grade5=0.0, xname6="", grade6=0.0, xname7="", grade7=0.0,
                                                       xname8="", grade8=0.0, xname9="", grade9=0.0, xname10="",
                                                       grade10=0.0)
                    models.reserved.objects.filter(id=q).update(mark=1)
                    models.pjjl.objects.create(name=name, xname=xname,lessonsname=lsname, item1=q1, item2=q2, item3=q3, item4=q4, item5=q5,
                                               item6=q6, item7=q7, item8=q8, item9=q9, item10=q10,
                                               item11=q11, item12=q12, item13=q13, item14=q14, )
                return redirect('/haveevaluated/')
            else:
                return render(request, 'login/evaluate.html')
    else:
        return redirect("/login/")


def haveevaluated(request):
    if request.session.get('is_login', None):
            xname = request.session.get('user_name')
            reserved_list = models.reserved.objects.filter(xname=xname, mark=1)
            return render(request, 'login/evaluationed.html', {'reserved_list': reserved_list})
    else:
        return redirect("/index/")

