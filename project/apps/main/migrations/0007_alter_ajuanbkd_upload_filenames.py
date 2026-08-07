from django.db import migrations, models

import apps.main.models.m_ajuan


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_ajuanbkd_jabatanfungsional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajuanbkd',
            name='surat_permohonan',
            field=models.FileField(max_length=255, upload_to=apps.main.models.m_ajuan.upload_surat_permohonan),
        ),
        migrations.AlterField(
            model_name='ajuanbkd',
            name='bukti_pembayaran',
            field=models.FileField(max_length=255, upload_to=apps.main.models.m_ajuan.upload_bukti_pembayaran),
        ),
        migrations.AlterField(
            model_name='ajuanbkd',
            name='surat_persetujuan',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=apps.main.models.m_ajuan.upload_surat_persetujuan),
        ),
        migrations.AlterField(
            model_name='ajuanbkd',
            name='surat_penugasan',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=apps.main.models.m_ajuan.upload_surat_penugasan),
        ),
    ]
