from django.contrib import admin
#-*-coding:utf-8 -*-
# Register your models here.

from login import models

from import_export import resources
from login.models import lessons
from login.models import reserved
from login.models import pjhz
from login.models import pjjl
from import_export.admin import ImportExportModelAdmin


class LessonResource(resources.ModelResource):

    class Meta:
        model = lessons
        export_order = ('id', 'whatday', 'detaltime', 'beginfinsh', 'lessonsname', 'name', 'place', 'comprise', 'lessonsmargin')


@admin.register(lessons)
class LessonAdmin(ImportExportModelAdmin):
    list_display = ('id', 'whatday', 'detaltime', 'beginfinsh', 'lessonsname', 'name', 'place', 'comprise', 'lessonsmargin')
    search_fields = ('whatday', 'lessonsname','name')
    resource_class = LessonResource


class ReservedResource(resources.ModelResource):

    class Meta:
        model = reserved
        export_order = ('id', 'xid','xname','name','lessonsname', 'whatday', 'detaltime', 'whichweek',  'place', 'comprise')


@admin.register(reserved)
class LessonAdmin(ImportExportModelAdmin):
    list_display = ('id', 'xid', 'xname', 'name', 'lessonsname', 'whatday', 'detaltime', 'whichweek',  'place', 'comprise')
    search_fields = ('whatday', 'lessonsname', 'name', 'xname')
    resource_class = ReservedResource


class PjjlResource(resources.ModelResource):

    class Meta:
        model = pjjl
        export_order = ('id', 'name','lessonsname', 'xname',  'item1', 'item2', 'item3', 'item4', 'item5', 'item6',
                        'item7', 'item8',  'item9',  'item10', 'item11', 'item12', 'item13', 'item14')


@admin.register(pjjl)
class PjjlAdmin(ImportExportModelAdmin):
    list_display = ('name','lessonsname','xname','item1','item2','item3','item4','item5','item6','item7','item8','item9','item10'
                        ,'item11','item12','item13','item14')
    search_fields = ('name','xname')
    resource_class = PjjlResource


class PjhzResource(resources.ModelResource):

    class Meta:
        model = pjhz
        export_order = ('id','name','xname1','grade1','xname2','grade2','xname3','grade3','xname4','grade4','xname5'
                        ,'grade5','xname6','grade6','xname7','grade7','xname8','grade8','xname9','grade9','xname10',
                        'grade10')


@admin.register(pjhz)
class PjjlAdmin(ImportExportModelAdmin):
    list_display = ('name','xname1','grade1','xname2','grade2','xname3','grade3','xname4','grade4','xname5'
                        ,'grade5','xname6','grade6','xname7','grade7','xname8','grade8','xname9','grade9','xname10',
                        'grade10')
    search_fields = ('name',)
    resource_class = PjhzResource





admin.site.register(models.User)
admin.site.site_header = "管理平台"
admin.site.site_title = "管理平台"







