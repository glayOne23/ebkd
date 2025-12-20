from django import forms
from django.utils.translation import gettext_lazy as _

from apps.services.mixins import FormErrorsMixin
from apps.main.models import Asesor


class AsesorForm(forms.ModelForm, FormErrorsMixin):
    class Meta:
        model   = Asesor
        fields  = '__all__'

        # labels  = {
        #     'name'        : _('Name'),
        #     'description' : _('Description'),
        # }


class AsesorExcelForm(forms.Form, FormErrorsMixin):
    excel_file = forms.FileField(
        label=_('Unggah Berkas Excel'),
        help_text=_('Unggah berkas Excel yang berisi data presensi.'),
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx, .xls'})
    )