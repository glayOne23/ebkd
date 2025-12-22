from apps.main.forms.ajuanbkd import AdminAjuanBKDForm, AjuanBKDForm
from apps.main.models import AjuanBKD, Asesor
from apps.main.views.base import AdminRequiredMixin, CustomTemplateBaseMixin
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)


# =====================================================================================================
#                                               MIXINS
# =====================================================================================================
class UserUpdateRequiredMixin(AccessMixin):
    """Mixin untuk membatasi akses hanya untuk grup admin."""
    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        get_object_or_404(AjuanBKD, id=id)
        return super().dispatch(request, *args, **kwargs)


# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================
class UserAjuanBKDListView(CustomTemplateBaseMixin, ListView):
    model = AjuanBKD
    template_name = 'main/user/ajuanbkd/table.html'
    context_object_name = 'data_ajuanbkd'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-id')


class UserAjuanBKDCreateView(CustomTemplateBaseMixin, CreateView):
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


class UserAjuanBKDUpdateView(UserUpdateRequiredMixin, CustomTemplateBaseMixin, UpdateView):
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
class UserAjuanBKDDeleteListView(View):
    def post(self, request):
        list_id = request.POST.getlist('list_id')

        if not list_id:
            messages.error(request, 'Invalid request!')
            return redirect('main:admin.ajuanbkd.table')

        try:
            with transaction.atomic():
                # delete sekaligus (lebih cepat & aman)
                deleted_count, _ = AjuanBKD.objects.filter(id__in=list_id, user=request.user).delete()

            if deleted_count > 0:
                messages.success(request, 'data berhasil dihapus')
            else:
                messages.warning(request, 'Tidak ada data dipilih untuk dihapus')

        except Exception as e:
            messages.error(request, f'Terdapat kesalahan ketika menghapus data {str(e)}')

        return redirect('main:admin.ajuanbkd.table')




# =====================================================================================================
#                                               ADMIN
# =====================================================================================================
class AdminAjuanBKDListView(AdminRequiredMixin, CustomTemplateBaseMixin, ListView):
    model = AjuanBKD
    template_name = 'main/admin/ajuanbkd/table.html'
    context_object_name = 'data_ajuanbkd'

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')

class AdminAjuanBKDUpdateView(AdminRequiredMixin, CustomTemplateBaseMixin, UpdateView):
    model = AjuanBKD
    template_name = 'main/admin/ajuanbkd/add.html'
    form_class = AdminAjuanBKDForm
    success_url = reverse_lazy('main:admin.ajuanbkd.table')

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
#                                                ADMIN SERVICE
# =====================================================================================================
class AdminAjuanBKDDeleteListView(AdminRequiredMixin, View):
    def post(self, request):
        list_id = request.POST.getlist('list_id')

        if not list_id:
            messages.error(request, 'Invalid request!')
            return redirect('main:admin.ajuanbkd.table')

        try:
            with transaction.atomic():
                # delete sekaligus (lebih cepat & aman)
                deleted_count, _ = AjuanBKD.objects.filter(id__in=list_id).delete()

            if deleted_count > 0:
                messages.success(request, 'data berhasil dihapus')
            else:
                messages.warning(request, 'Tidak ada data dipilih untuk dihapus')

        except Exception as e:
            messages.error(request, f'Terdapat kesalahan ketika menghapus data {str(e)}')

        return redirect('main:admin.ajuanbkd.table')


# =====================================================================================================
#                                               ASESO
# =====================================================================================================
class AsesorAjuanBKDListView(CustomTemplateBaseMixin, ListView):
    model = AjuanBKD
    template_name = 'main/asesor/ajuanbkd/table.html'
    context_object_name = 'data_ajuanbkd'

    def get_queryset(self):
        return self.model.objects.filter(Q(asesor1__user=self.request.user) | Q(asesor2__user=self.request.user)).order_by('-id')