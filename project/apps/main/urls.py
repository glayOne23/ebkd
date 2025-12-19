from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.main.views import (
    services,
    profile,
    account,
    dashboard,
    category,
    setting,
)

app_name = 'main'

urlpatterns = [
    path('dashboard/',                              dashboard.index,            name='dashboard'),
    path('profile/',                                profile.index,              name='profile'),

    path('services/', include([
        path('setprofilesync/',                     services.setprofilesync,    name='services_setprofilesync'),
    ])),

    path('account/', include([
        # =================================================[ LOAD PAGE ]=================================================
        path('table/',                              account.table,              name='account_table'),
        path('role/',                               account.role,               name='account_role'),
        path('add/',                                account.add,                name='account_add'),        
        path('edit/<int:id>/',                      account.edit,               name='account_edit'),
        path('edit_group/<int:id>/',                account.edit_group,         name='account_edit_group'),
        
        # ==================================================[ SERVICE ]==================================================
        path('delrole/<int:userid>/<int:groupid>/', account.delrole,            name='account_delrole'),
        path('deletelist/',                         account.deletelist,         name='account_deletelist'),
        path('synclist/',                           account.synclist,           name='account_synclist'),
        path('setisactive/<str:mode>/',             account.setisactive,        name='account_setisactive'),
        path('datatable/',                          account.datatable,          name='account_datatable'),
        path('import/',                             account.import_user,        name='account_import'),
        path('data_employee/',                      account.api_data_employee,  name='account_data_employee'),
    ])),


    path('category/', include([
        # =================================================[ LOAD PAGE ]=================================================
        path('table/',                              category.table,             name='category_table'),
        path('add/',                                category.add,               name='category_add'),
        path('edit/<int:id>/',                      category.edit,              name='category_edit'),

        # ==================================================[ SERVICE ]==================================================
        path('deletelist/',                         category.deletelist,        name='category_deletelist'),
    ])),


    path('setting/', include([
        # =================================================[ LOAD PAGE ]=================================================
        path('edit/',                               setting.edit,               name='setting_edit'),

        # ==================================================[ SERVICE ]==================================================
        path('deletefile/<int:id>/',                setting.deletefile,         name='setting_deletefile'),
    ])),
]