from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings



def send_activation_email(user):
    subject = "Activation email"
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    message = render_to_string(
        'registration/activate_email.html',
        {
        'user': user,
        'uid': uid,
        'token': token,
        'domain': settings.DOMAIN_URL
        }
    )
    send_mail(
        subject, message,
        'kamanalphonse@gmail.com',
        [user.email],
        fail_silently=True
    )

def send_password_reset_email(user):
    subject = "Activation email"
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    message = render_to_string(
        'registration/password_reset_email.html',
        {
        'user': user,
        'uid': uid,
        'token': token,
        'domain': settings.DOMAIN_URL
        }
    )
    send_mail(
        subject, message,
        'kamanalphonse@gmail.com',
        [user.email],
        fail_silently=True
    )

