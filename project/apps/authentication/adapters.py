from django.contrib import messages
from django.shortcuts import redirect

from allauth.account.utils import filter_users_by_email
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter



class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # Akun Google sudah terhubung ke user -> login normal
        if sociallogin.account.pk:
            return

        # Tolak jika email Google dipakai lebih dari satu user (tidak jelas harus login ke user mana)
        for address in sociallogin.email_addresses:
            if len(filter_users_by_email(address.email)) > 1:
                messages.error(request, 'Email {} terdaftar pada lebih dari satu akun. Silakan hubungi Admin atau IT Support.'.format(address.email))
                raise ImmediateHttpResponse(redirect('authentication:signin'))
