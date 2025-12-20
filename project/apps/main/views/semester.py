from json import dumps

from apps.main.forms.semester import SemesterForm
from apps.main.models import Semester
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)


# =====================================================================================================
#                                               MIXINS
# =====================================================================================================
def in_grup(user, grup_name):
    if user:
        return user.groups.filter(name=grup_name).count() > 0
    return False


class AdminRequiredMixin(AccessMixin):
    """Mixin untuk membatasi akses hanya untuk grup personalia."""
    def dispatch(self, request, *args, **kwargs):
        if not in_grup(request.user, 'admin'):
            return HttpResponseForbidden("Anda tidak memiliki hak akses.")
        return super().dispatch(request, *args, **kwargs)


class CustomTemplateBaseMixin(LoginRequiredMixin):
    """Mixin dasar untuk semua view"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ===[Select CSS and JS Files]===
        context['datatables']       = True
        context['select2']          = False
        context['summernote']       = False
        context['maxlength']        = False
        context['inputmask']        = False
        context['duallistbox']      = False
        context['moment']           = False
        context['daterange']        = False
        context['chartjs']          = False
        return context


# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================
class AdminSemesterListView(AdminRequiredMixin, CustomTemplateBaseMixin, ListView):
    model = Semester
    template_name = 'main/admin/semester/table.html'
    context_object_name = 'data_semester'

    def get_queryset(self):
        return self.model.objects.order_by('-id')


class AdminSemesterCreateView(AdminRequiredMixin, CustomTemplateBaseMixin, CreateView):
    model = Semester
    template_name = 'main/admin/semester/add.html'
    form_class = SemesterForm
    success_url = reverse_lazy('main:admin.semester.table')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Data semester berhasil dibuat!")
        return response


class AdminSemesterUpdateView(AdminRequiredMixin, CustomTemplateBaseMixin, UpdateView):
    model = Semester
    template_name = 'main/admin/semester/add.html'
    form_class = SemesterForm
    success_url = reverse_lazy('main:admin.semester.table')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs.get('id'))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Data semester berhasil diperbarui")
        return response


# =====================================================================================================
#                                                SERVICE
# =====================================================================================================
class AdminSemesterDeleteListView(AdminRequiredMixin, View):
    def post(self, request):
        list_id = request.POST.getlist('list_id')

        if not list_id:
            messages.error(request, 'Invalid request!')
            return redirect('main:admin.semester.table')

        try:
            with transaction.atomic():
                # delete sekaligus (lebih cepat & aman)
                deleted_count, _ = Semester.objects.filter(id__in=list_id).delete()

            if deleted_count > 0:
                messages.success(request, f'{deleted_count} data berhasil dihapus')
            else:
                messages.warning(request, 'Tidak ada data dipilih untuk dihapus')

        except Exception as e:
            messages.error(request, f'Terdapat kesalahan ketika menghapus data {str(e)}')

        return redirect('main:admin.semester.table')
