from django.contrib import admin
from apps.main.models import *

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

class AdminSetting(admin.ModelAdmin):
    list_display = ('id', 'category', 'key', 'alias', 'mode', 'value', 'file')


admin.site.register(Category, AdminCategory)
admin.site.register(Setting, AdminSetting)
admin.site.register(JenjangPendidikan)
admin.site.register(RumpunIlmu)
admin.site.register(JabatanFungsional)
admin.site.register(Asesor)
admin.site.register(Semester)
admin.site.register(AjuanBKD)