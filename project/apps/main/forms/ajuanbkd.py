from django import forms
from django.utils.translation import gettext_lazy as _

from apps.services.mixins import FormErrorsMixin
from apps.main.models import AjuanBKD


class AjuanBKDForm(forms.ModelForm, FormErrorsMixin):
    class Meta:
        model   = AjuanBKD
        exclude  = ['user',]

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
