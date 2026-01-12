from django.contrib.auth.models import User
from django.db import models

TIPE_RUMPUN_CHOICES = [
    ('rumpun', 'Rumpun Ilmu'),
    ('subrumpun', 'Sub Rumpun Ilmu'),
    ('bidang', 'Bidang Ilmu'),
]

STATUS_AJUAN_CHOICES = [
    ('proses', 'Proses'),
    ('revisi', 'Revisi'),
    ('disetujui', 'Disetujui'),
]


class JabatanFungsional(models.Model):
    nama       = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return self.nama


class JenjangPendidikan(models.Model):
    nama       = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return self.nama


class RumpunIlmu(models.Model):
    kode_rumpun = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=255)
    tipe_rumpun = models.CharField(max_length=100, choices=TIPE_RUMPUN_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return self.nama


class Asesor(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    nira       = models.CharField(max_length=255, unique=True)
    jabatanfungsional = models.ForeignKey(JabatanFungsional, on_delete=models.SET_NULL, null=True, blank=True)
    pendidikanterakhir = models.ForeignKey(JenjangPendidikan, on_delete=models.SET_NULL, null=True, blank=True)
    rumpunilmu = models.ForeignKey(RumpunIlmu, on_delete=models.SET_NULL, null=True, blank=True, related_name='asesor_rumpunilmu')
    subrumpunilmu = models.ForeignKey(RumpunIlmu, on_delete=models.SET_NULL, null=True, blank=True, related_name='asesor_subrumpunilmu')
    bidangilmu = models.ForeignKey(RumpunIlmu, on_delete=models.SET_NULL, null=True, blank=True, related_name='asesor_bidangilmu')
    aktif      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return self.user.get_full_name()


class Semester(models.Model):
    nama       = models.CharField(max_length=100, unique=True)
    aktif      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return self.nama


class AjuanBKD(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pengusul = models.CharField(max_length=255)
    nidn = models.CharField(max_length=50)
    nomortelepon = models.CharField(max_length=15)
    perguruantinggi = models.CharField(max_length=255)
    semester = models.ManyToManyField(Semester)
    asesor1 = models.ForeignKey(Asesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='ajuanbkd_asesor1')
    asesor2 = models.ForeignKey(Asesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='ajuanbkd_asesor2')
    keterangan = models.TextField(null=True, blank=True)
    nomor_surat = models.CharField(max_length=100)
    surat_permohonan = models.FileField(upload_to='surat_permohonan/')
    bukti_pembayaran = models.FileField(upload_to='bukti_pembayaran/')
    surat_persetujuan = models.FileField(upload_to='surat_persetujuan/', blank=True, null=True)
    surat_penugasan = models.FileField(upload_to='surat_penugasan/', blank=True, null=True)
    status_ajuan = models.CharField(max_length=100, choices=STATUS_AJUAN_CHOICES, default='proses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        return f"Ajuan BKD {self.pengusul}"