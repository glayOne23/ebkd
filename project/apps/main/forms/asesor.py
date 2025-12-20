from django import forms
from django.utils.translation import gettext_lazy as _

from apps.services.mixins import FormErrorsMixin
from apps.main.models import Asesor


class AsesorForm(forms.ModelForm, FormErrorsMixin):
    class Meta:
        model   = Asesor
        fields  = '__all__'

        labels  = {
            'jabatanfungsional'        : _('Jabatan Fungsional'),
            'pendidikanterakhir' : _('Pendidikan Terakhir'),
            'rumpunilmu' : _('Rumpun Ilmu'),
            'subrumpunilmu' : _('Sub Rumpun Ilmu'),
            'bidangilmu' : _('Bidang Ilmu'),
        }

        widgets = {
            'user'        : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'jabatanfungsional' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'pendidikanterakhir' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'rumpunilmu' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'subrumpunilmu' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
            'bidangilmu' : forms.Select(attrs={'class': 'select form-control select2bs4'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].label_from_instance = (
            lambda obj: f"{obj.get_full_name()} ({obj.username})"
        )


class AsesorExcelForm(forms.Form, FormErrorsMixin):
    excel_file = forms.FileField(
        label=_('Unggah Berkas Excel'),
        help_text=_('Unggah berkas Excel yang berisi data presensi.'),
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx, .xls'})
    )
