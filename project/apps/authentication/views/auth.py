from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

from apps.authentication.forms.auth import FormSignUp, FormSignUpProfile, FormSignIn, FormResetPassword
from apps.services.decorators import logout_required
from apps.services.utils import setsession, send_otp_by_email, username_in_cas




# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================

@logout_required('main:dashboard')
def signin(request):
    context = {}
    context['formsignin'] = FormSignIn(request, data=request.POST or None)
    context['email_config_available'] = ( hasattr(settings, 'EMAIL_HOST_USER') and hasattr(settings, 'EMAIL_HOST_PASSWORD') and settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD )

    if request.POST:
        if context['formsignin'].is_valid():
            username = context['formsignin'].cleaned_data.get('username')
            password = context['formsignin'].cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:

                    setsession(request, user)
                    login(request, user)
                    messages.success(request, 'Berhasil signin. Selamat datang, {}!'.format(user.get_full_name() or user.username))

                    next = request.GET.get('next', 'main:dashboard')
                    return redirect(next)
                else:
                    messages.warning(request, 'Akunmu belum aktif. Silakan cek email untuk verifikasi.')
                    # return redirect('authentication:signin')
            else:
                messages.warning(request, 'Mohon periksa kembali username dan password Anda.')
                # return redirect('authentication:signin')
        else:
            if '__all__' in context['formsignin'].errors.get_json_data():
                messages.error(request, context['formsignin'].errors.get_json_data()['__all__'][0]['message'])
            else:
                messages.error(request, context['formsignin'].get_errors())


    return render(request, 'authentication/signin.html', context)



@logout_required('main:dashboard')
def signup(request):
    context = {}
    context['formsignup']       = FormSignUp(request.POST or None)
    context['formsignupprofile']= FormSignUpProfile(request.POST or None)

    if request.POST:
        if context['formsignup'].is_valid():
            if context['formsignupprofile'].is_valid():

                if User.objects.filter(email=request.POST.get('email')).exists():
                    messages.error(request, 'Email sudah terdaftar, silakan gunakan email lain.')
                    return redirect('authentication:signup')

                if username_in_cas(request.POST.get('username')):
                    messages.warning(request, 'Username yang Anda gunakan terdaftar di sistem CAS. Silakan gunakan username lain.')
                    return redirect('authentication:signup')

                user = context['formsignup'].save(commit=False)
                # user.is_active = False
                user.save()

                context['formsignupprofile'] = FormSignUpProfile(request.POST or None, instance=user.profile)
                context['formsignupprofile'].save()

                if hasattr(settings,'EMAIL_HOST_USER') and hasattr(settings,'EMAIL_HOST_PASSWORD') and settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    # ===[SEND EMAIL VERIFICATION]===
                    try:
                        send_otp_by_email(request, user, 'authentication:verify')
                        messages.success(request, 'Mohon konfirmasi email Anda untuk mengaktifkan akun.')
                        return redirect('authentication:signin')
                    except Exception as e :
                        print('[ERROR] : ', e)
                        messages.error(request, 'Gagal mengirim notifikasi ke email. Silakan hubungi Admin atau IT Support')
                        return redirect('authentication:signup')
                else:
                    # messages.success(request, 'Selamat! Akun Anda berhasil dibuat. Silakan hubungi Admin atau IT Support untuk mengaktifkan akun Anda.')
                    messages.success(request, 'Selamat! Akun Anda berhasil dibuat. Silakan masukkan username dan password anda untuk masuk ke sistem.')
                    return redirect('authentication:signin')

            else:
                messages.error(request, context['formsignupprofile'].get_errors())
        else:
            messages.error(request, context['formsignup'].get_errors())

    return render(request, 'authentication/signup.html', context)



@logout_required('main:dashboard')
def forgot(request):
    if request.POST:
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Mohon masukkan email Anda.')
            return redirect('authentication:forgot')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email tidak ditemukan dalam sistem kami.')
            return redirect('authentication:forgot')

        try:
            send_otp_by_email(request, user, 'authentication:reset_password')
            messages.success(request, 'OTP sudah dikirim ke email Anda. Silakan periksa email untuk melanjutkan proses reset password.')
            return redirect('authentication:forgot')
        except Exception as e:
            print('[ERROR] : ', e)
            messages.error(request, 'Gagal mengirim OTP ke email Anda. Silakan coba lagi atau hubungi Admin/IT Support.')
            return redirect('authentication:forgot')

    context = {}
    return render(request, 'authentication/forgot.html', context)



def reset_password(request):
    context = {}
    context['email']    = request.GET.get('email', '')
    context['otp']      = request.GET.get('otp', '')
    context['formresetpassword'] = FormResetPassword(request.POST or None, request.FILES or None)


    if request.POST:
        if context['formresetpassword'].is_valid():
            context['formresetpassword'].save()
            messages.success(request, 'Password berhasil direset. Silakan login dengan password baru Anda.')
            return redirect('authentication:signin')
        else:
            messages.error(request, context['formresetpassword'].get_errors())


    return render(request, 'authentication/reset_password.html', context)



# =====================================================================================================
#                                                SERVICE
# =====================================================================================================

def signout(request):
    logout(request)

    storage = messages.get_messages(request)
    if storage:
        for message in storage:
            messages.warning(request, message)
    else:
        messages.success(request, 'Success Signout')

    return redirect('authentication:signin')



def verify(request):
    if request.GET:
        if request.GET.get('email') and request.GET.get('otp'):
            try:
                user = User.objects.get(email=request.GET.get('email'), profile__otp=request.GET.get('otp'))
                user.is_active = True
                user.profile.otp = None
                user.save()
                messages.success(request, 'Email berhasil diverifikasi! Silakan login.')
            except User.DoesNotExist:
                messages.warning(request, 'Email atau OTP tidak sesuai. Silakan coba lagi.')
        else:
            messages.warning(request, "Link tidak lengkap. Silakan periksa email Anda untuk link verifikasi yang benar.")
    else:
        messages.warning(request, 'Mohon gunakan link verifikasi dari email Anda.')


    return redirect('authentication:signin')