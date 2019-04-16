from django.db import models
#-*-coding:utf-8 -*-

# Create your models here.


class User(models.Model):

    gender=(
        ('male',"男"),
        ('female',"女"),
    )

    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name="用户"
        verbose_name_plural="用户"


class lessons(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    whatday =models.CharField("星期几",max_length=30)
    detaltime = models.CharField("上课节次", max_length=30)
    beginfinsh = models.CharField("起始周", max_length=30)
    lessonsname = models.CharField("课程名称", max_length=256)
    name = models.CharField("姓名", max_length=128)
    place=models.CharField("上课地点",max_length=128)
    comprise=models.CharField("教学班组成",max_length=128)
    lessonsmargin=models.IntegerField("余量")

    def _str_(self):
        return self.id

    class Meta:
        db_table="lessons"
        verbose_name="课程"
        verbose_name_plural="课程"


class reserved(models.Model):
    id = models.IntegerField(primary_key=True,db_column='FId')
    xid=models.CharField("选课人工号",max_length=30)
    xname =models.CharField("选课人",max_length=30)
    name = models.CharField("姓名", max_length=128)
    lessonsname = models.CharField("课程名称", max_length=256)
    whatday =models.CharField("星期几",max_length=30)
    detaltime = models.CharField("上课节次", max_length=30)
    whichweek = models.CharField("起始周", max_length=30)
    place = models.CharField("上课地点", max_length=128)
    comprise = models.CharField("教学班组成", max_length=128)
    mark = models.BooleanField("是否已评价")

    def _str_(self):
        return self.id

    class Meta:
        db_table="reserved"
        verbose_name="选课单"
        verbose_name_plural="选课单"


class pjjl(models.Model):
    id = models.IntegerField(primary_key=True,db_column='FId')
    name = models.CharField("姓名", max_length=128)
    lessonsname = models.CharField("课程名称", max_length=256)
    xname = models.CharField("听课老师", max_length=30)
    item1 = models.IntegerField("标准1")
    item2 = models.IntegerField("标准2")
    item3 = models.IntegerField("标准3")
    item4 = models.IntegerField("标准4")
    item5 = models.IntegerField("标准5")
    item6 = models.IntegerField("标准6")
    item7 = models.IntegerField("标准7")
    item8 = models.IntegerField("标准8")
    item9 = models.IntegerField("标准9")
    item10 = models.IntegerField("标准10")
    item11 = models.IntegerField("标准11")
    item12 = models.IntegerField("标准12")
    item13 = models.IntegerField("标准13")
    item14 = models.IntegerField("标准14")

    def _str_(self):
        return self.id

    class Meta:
        db_table = "evaluation_records"
        verbose_name = "评价记录表"
        verbose_name_plural = "评价记录表"


class pjhz(models.Model):
    id = models.IntegerField(primary_key=True, db_column='FId')
    name = models.CharField("姓名", max_length=128)
    xname1=models.CharField("听课老师",max_length=30)
    grade1= models.FloatField("评分")
    xname2=models.CharField("听课老师",max_length=30)
    grade2 = models.FloatField("评分")
    xname3=models.CharField("听课老师",max_length=30)
    grade3= models.FloatField("评分")
    xname4=models.CharField("听课老师",max_length=30)
    grade4= models.FloatField("评分")
    xname5=models.CharField("听课老师",max_length=30)
    grade5= models.FloatField("评分")
    xname6=models.CharField("听课老师",max_length=30)
    grade6= models.FloatField("评分")
    xname7=models.CharField("听课老师",max_length=30)
    grade7= models.FloatField("评分")
    xname8=models.CharField("听课老师",max_length=30)
    grade8= models.FloatField("评分")
    xname9 =models.CharField("听课老师",max_length=30)
    grade9 = models.FloatField("评分")
    xname10 = models.CharField("听课老师",max_length=30)
    grade10 = models.FloatField("评分")

    def _str_(self):
        return self.id

    class Meta:
        db_table = "evaluation"
        verbose_name = "评价汇总表"
        verbose_name_plural = "评价汇总表"




