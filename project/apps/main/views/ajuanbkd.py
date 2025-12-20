from json import dumps

from apps.main.forms.ajuanbkd import AjuanBKDForm
from apps.main.models import AjuanBKD, Asesor
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from apps.main.views.base import CustomTemplateBaseMixin


# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================
class AjuanBKDListView(CustomTemplateBaseMixin, ListView):
    model = AjuanBKD
    template_name = 'main/user/ajuanbkd/table.html'
    context_object_name = 'data_ajuanbkd'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-id')


class AjuanBKDCreateView(CustomTemplateBaseMixin, CreateView):
    model = AjuanBKD
    template_name = 'main/user/ajuanbkd/add.html'
    form_class = AjuanBKDForm
    success_url = reverse_lazy('main:user.ajuanbkd.table')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Data Ajuan BKD berhasil dibuat!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ===[Select CSS and JS Files]===
        context['dataasesor'] = Asesor.objects.filter(aktif=True)
        return context


class AjuanBKDUpdateView(CustomTemplateBaseMixin, UpdateView):
    model = AjuanBKD
    template_name = 'main/user/ajuanbkd/add.html'
    form_class = AjuanBKDForm
    success_url = reverse_lazy('main:user.ajuanbkd.table')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs.get('id'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Data Ajuan BKD berhasil diperbarui")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ===[Select CSS and JS Files]===
        context['dataasesor'] = Asesor.objects.filter(aktif=True)
        return context


# =====================================================================================================
#                                                SERVICE
# =====================================================================================================
class AjuanBKDDeleteListView(View):
    def post(self, request):
        list_id = request.POST.getlist('list_id')

        if not list_id:
            messages.error(request, 'Invalid request!')
            return redirect('main:user.ajuanbkd.table')

        try:
            with transaction.atomic():
                # delete sekaligus (lebih cepat & aman)
                deleted_count, _ = AjuanBKD.objects.filter(id__in=list_id, user=request.user).delete()

            if deleted_count > 0:
                messages.success(request, f'{deleted_count} data berhasil dihapus')
            else:
                messages.warning(request, 'Tidak ada data dipilih untuk dihapus')

        except Exception as e:
            messages.error(request, f'Terdapat kesalahan ketika menghapus data {str(e)}')

        return redirect('main:user.ajuanbkd.table')
