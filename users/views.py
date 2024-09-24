from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import CreateView, View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout

from users.models import User
from users.forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordResetForm
from .utils.send_email import send_activation_email, send_password_reset_email


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class CustomUserCreationView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        with transaction.atomic():
            user= form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user)
        messages.success(
            self.request,
            ("Votre compte compte a ete cree, consulter "
                "votre boite email pour activer votre compte")
        )
        return redirect(self.success_url)
    

class UserActivationView(View):
    login_url = reverse_lazy('login')

    def get(self, request, uid, token):
        print('Starting...')
        id = urlsafe_base64_decode(uid)
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return render(request, 'registration/activation_invalid.html')
        print('activation...')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                self.request,
                'Votre compte a ete active. Vous pouvez vous connecter.'
            )
            return redirect(self.login_url)
        
        return render(request, 'registration/activation_invalid.html')



class LogoutView(View):
    login_url = reverse_lazy('login')

    def get(self, request):
        logout(request)
        messages.success(
            self.request,
            'Votre compte a ete deconnecte.'
        )
        return redirect(self.login_url)
    

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # Customize the template
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset')
    email_template_name = 'registration/password_reset_email.html'
    
    def form_valid(self, form):
            # Send password reset email
            response = super().form_valid(form)
            
            # Add success message to inform the user
            messages.success(self.request, ("An email has been sent to reset your password."))
            
            return response


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'  # Custom template
