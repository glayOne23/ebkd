from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.main.views import (
    services,
    profile,
    account,
    dashboard,
    category,
    setting,
    asesor,
    semester,
    ajuanbkd
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
        path('generate/',                           account.generate,           name='account_generate'),
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

    path('admin/', include([
        path('asesor/', include([
            # =================================================[ LOAD PAGE ]=================================================
            path('table/', asesor.AdminAsesorListView.as_view(), name='admin.asesor.table'),
            path('add/', asesor.AdminAsesorCreateView.as_view(), name='admin.asesor.add'),
            path('<int:id>/update/', asesor.AdminAsesorUpdateView.as_view(), name='admin.asesor.update'),
            path('excel_import/', asesor.AdminAsesorExcelImportView.as_view(), name='admin.asesor.excel_import'),
            # ==================================================[ SERVICE ]==================================================
            path('deletelist/', asesor.AdminAsesorDeleteListView.as_view(), name='admin.asesor.deletelist'),
        ])),
        path('semester/', include([
            # =================================================[ LOAD PAGE ]=================================================
            path('table/', semester.AdminSemesterListView.as_view(), name='admin.semester.table'),
            path('add/', semester.AdminSemesterCreateView.as_view(), name='admin.semester.add'),
            path('<int:id>/update/', semester.AdminSemesterUpdateView.as_view(), name='admin.semester.update'),
            # ==================================================[ SERVICE ]==================================================
            path('deletelist/', semester.AdminSemesterDeleteListView.as_view(), name='admin.semester.deletelist'),
        ])),
        path('ajuanbkd/', include([
            # =================================================[ LOAD PAGE ]=================================================
            path('table/', ajuanbkd.AdminAjuanBKDListView.as_view(), name='admin.ajuanbkd.table'),
            path('<int:id>/update/', ajuanbkd.AdminAjuanBKDUpdateView.as_view(), name='admin.ajuanbkd.update'),
            # ==================================================[ SERVICE ]==================================================
            path('deletelist/', ajuanbkd.AdminAjuanBKDDeleteListView.as_view(), name='admin.ajuanbkd.deletelist'),
        ])),
    ])),

    path('user/', include([
        path('ajuanbkd/', include([
            # =================================================[ LOAD PAGE ]=================================================
            path('table/', ajuanbkd.UserAjuanBKDListView.as_view(), name='user.ajuanbkd.table'),
            path('add/', ajuanbkd.UserAjuanBKDCreateView.as_view(), name='user.ajuanbkd.add'),
            path('<int:id>/update/', ajuanbkd.UserAjuanBKDUpdateView.as_view(), name='user.ajuanbkd.update'),
            # ==================================================[ SERVICE ]==================================================
            path('deletelist/', ajuanbkd.UserAjuanBKDDeleteListView.as_view(), name='user.ajuanbkd.deletelist'),
        ])),
    ])),

    path('asesor/', include([
        path('ajuanbkd/', include([
            # =================================================[ LOAD PAGE ]=================================================
            path('table/', ajuanbkd.AsesorAjuanBKDListView.as_view(), name='asesor.ajuanbkd.table'),
        ])),
    ])),
]