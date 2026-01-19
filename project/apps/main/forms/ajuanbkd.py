from apps.main.models import AjuanBKD, Asesor, Semester
from apps.services.mixins import FormErrorsMixin
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class AjuanBKDForm(forms.ModelForm, FormErrorsMixin):
    class Meta:
        model   = AjuanBKD
        exclude  = ['user', 'status_ajuan', 'surat_persetujuan', 'surat_penugasan']

        labels  = {
            'jabatanfungsional'        : _('Jabatan Fungsional'),
            'nomortelepon'        : _('No. Handphone (Whatsapp)'),
            'perguruantinggi' : _('Nama Perguruan Tinggi'),
            'semester' : _('Semester yang dinilai'),
        }

        widgets = {
            'asesor1' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'asesor2' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
        }

        help_texts = {
            'asesor1': 'Untuk melihat daftar asesor, <a href="" data-toggle="modal" data-target="#asesorModal">lihat di sini</a>',
            'asesor2': 'Untuk melihat daftar asesor, <a href="" data-toggle="modal" data-target="#asesorModal">lihat di sini</a>',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ filter semester aktif saja
        self.fields['asesor1'].queryset = Asesor.objects.filter(aktif=True)
        self.fields['asesor2'].queryset = Asesor.objects.filter(aktif=True)
        self.fields['semester'].queryset = Semester.objects.filter(aktif=True).order_by("-id")



class AdminAjuanBKDForm(AjuanBKDForm):
    class Meta:
        model   = AjuanBKD
        exclude  = ['user', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            url = reverse('main:admin.ajuanbkd.surat_persetujuan_pdf', kwargs={'id': self.instance.pk})
            self.fields['surat_persetujuan'].label = mark_safe(f'Surat Persetujuan 'f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank"><i class="fa fa-file-pdf"></i> Unduh Template</a>')
            self.fields['surat_penugasan'].label = mark_safe(f'Surat Penugasan 'f'<a href="{url}?tipe_surat=penugasan" class="btn btn-sm btn-primary" target="_blank"><i class="fa fa-file-pdf"></i> Unduh Template</a>')