from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from users.utils.send_email import send_activation_email, send_password_reset_email
from users.models import User
from django.core.exceptions import ValidationError



class CustomAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        print(user)
        if user is None:
            raise ValidationError('Email ou mot de passe incorrect')
        
        if not user.is_active:
            send_activation_email(user)
            raise ValidationError("Votre compte n'est pas actif,"
                                " Consultez votre email pour l'activer.")

        return self.cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(required=True, help_text='Ce champ est requis')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ce email exist deja')
        return email


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Entrez votre email', max_length=255)


    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Pas d'utilisateur enregistre avec cet email")
        return email