from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have a valid email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True    # is_superuser is an attribute of PermissionMixin class
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateField(default=timezone.now)
    username = None

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['firt_name', 'last_name']

    objects = UserManager()     # Link to your custom user manager

    def __str__(self):
        return self.email