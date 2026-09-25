import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import Lower

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

from apps.authentication.models import Profile
from apps.main.models.m_ajuan import AjuanBKD



class Command(BaseCommand):
    help = (
        'Gabungkan akun yang memakai email sama. '
        'Tanpa --pair: tampilkan daftar email duplikat. '
        'Dengan --pair KEEP:DROP: pindahkan akun Google, EmailAddress, dan ajuan dari DROP ke KEEP, '
        'lalu nonaktifkan DROP (tidak dihapus). Default dry-run; tambahkan --apply untuk menyimpan.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--pair', action='append', default=[], metavar='KEEP:DROP', help='ID user dipertahankan : ID user dinonaktifkan')
        parser.add_argument('--apply', action='store_true', help='Simpan perubahan (tanpa ini hanya dry-run)')
        parser.add_argument('--backup-dir', default=os.path.join(settings.BASE_DIR, 'backups'), help='Folder backup JSON sebelum --apply')


    def handle(self, *args, **options):
        if not options['pair']:
            if options['apply']:
                raise CommandError('--apply wajib disertai --pair KEEP:DROP (contoh: --pair 1926:2346 --apply)')
            return self.list_duplicates()

        pairs = self.parse_pairs(options['pair'])
        for keep, drop in pairs:
            self.show_pair(keep, drop)

        if not options['apply']:
            self.stdout.write(self.style.WARNING('\nDRY-RUN: tidak ada perubahan. Tambahkan --apply untuk menyimpan.'))
            return

        backup_path = self.backup(pairs, options['backup_dir'])
        self.stdout.write(self.style.SUCCESS(f'\nBackup: {backup_path}'))

        with transaction.atomic():
            for keep, drop in pairs:
                keep = User.objects.select_for_update().get(pk=keep.pk)
                drop = User.objects.select_for_update().get(pk=drop.pk)
                s = SocialAccount.objects.filter(user=drop).update(user=keep)
                e = EmailAddress.objects.filter(user=drop).update(user=keep)
                a = AjuanBKD.objects.filter(user=drop).update(user=keep)
                drop.email = ''
                drop.is_active = False
                drop.save(update_fields=['email', 'is_active'])
                self.stdout.write(f'{keep.pk} <- {drop.pk} | google {s} | emailaddr {e} | ajuan {a}')

        self.stdout.write(self.style.SUCCESS('Selesai.'))


    def list_duplicates(self):
        dup = (User.objects.exclude(email='').annotate(e=Lower('email'))
               .values('e').annotate(n=Count('id')).filter(n__gt=1))
        if not dup:
            self.stdout.write(self.style.SUCCESS('Tidak ada email duplikat.'))
            return
        for row in dup:
            self.stdout.write(self.style.MIGRATE_HEADING(row['e']))
            for u in User.objects.filter(email__iexact=row['e']).order_by('date_joined'):
                self.stdout.write('  ' + self.describe(u))


    def parse_pairs(self, raw_pairs):
        pairs, seen = [], set()
        for raw in raw_pairs:
            try:
                keep_id, drop_id = (int(x) for x in raw.split(':'))
            except ValueError:
                raise CommandError(f'Format --pair salah: {raw!r} (contoh: 1926:2346)')
            if keep_id == drop_id or {keep_id, drop_id} & seen:
                raise CommandError(f'ID pada --pair {raw} sama atau sudah dipakai di pair lain')
            seen |= {keep_id, drop_id}
            try:
                keep, drop = User.objects.get(pk=keep_id), User.objects.get(pk=drop_id)
            except User.DoesNotExist:
                raise CommandError(f'User pada --pair {raw} tidak ditemukan')
            if not drop.email or keep.email.lower() != drop.email.lower():
                raise CommandError(f'Email user {keep_id} dan {drop_id} tidak sama: {keep.email!r} vs {drop.email!r}')
            pairs.append((keep, drop))
        return pairs


    def show_pair(self, keep, drop):
        self.stdout.write(self.style.MIGRATE_HEADING(f'\n{keep.email}'))
        self.stdout.write('  KEEP ' + self.describe(keep))
        self.stdout.write('  DROP ' + self.describe(drop))


    def describe(self, u):
        google = list(SocialAccount.objects.filter(user=u).values_list('uid', flat=True))
        ajuan = list(AjuanBKD.objects.filter(user=u).values_list('id', flat=True))
        return (f'id={u.pk} username={u.username!r} nama={u.get_full_name()!r} active={u.is_active} '
                f'password={u.has_usable_password()} google={google} ajuan={ajuan}')


    def backup(self, pairs, backup_dir):
        ids = [u.pk for pair in pairs for u in pair]
        objs = (list(User.objects.filter(pk__in=ids))
                + list(Profile.objects.filter(user_id__in=ids))
                + list(SocialAccount.objects.filter(user_id__in=ids))
                + list(EmailAddress.objects.filter(user_id__in=ids))
                + list(AjuanBKD.objects.filter(user_id__in=ids)))
        os.makedirs(backup_dir, exist_ok=True)
        path = os.path.join(backup_dir, 'gabung_akun_email_{}.json'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
        with open(path, 'w') as f:
            f.write(serializers.serialize('json', objs, indent=1))
        return path
