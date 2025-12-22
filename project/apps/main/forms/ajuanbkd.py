from django import forms
from django.utils.translation import gettext_lazy as _

from apps.services.mixins import FormErrorsMixin
from apps.main.models import AjuanBKD, Semester, Asesor


class AjuanBKDForm(forms.ModelForm, FormErrorsMixin):
    class Meta:
        model   = AjuanBKD
        exclude  = ['user', 'status_ajuan']

        labels  = {
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
        self.fields['semester'].queryset = Semester.objects.filter(aktif=True)



class AdminAjuanBKDForm(AjuanBKDForm):
    class Meta:
        model   = AjuanBKD
        exclude  = ['user', 'status']