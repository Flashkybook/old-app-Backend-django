# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    """The UserManager subclasses the BaseUserManager and overrides the methods create_user and create_superuser. 
    These custom methods are needed because the default methods expect a username to be provided. 
    The admin app and manage.py will call these methods."""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)  # required by the admin.

    # used by the PermissionsMixin to grant all permissions.
    is_superuser = models.BooleanField(default=False)

    # indicates whether the user is considered “active”.
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # The name of the field that will serve as unique identifier (which will be the email field for us).
    USERNAME_FIELD = 'email'

    # The name of the field that will be returned when get_email_field_name() is called on a User instance.
    EMAIL_FIELD = 'email'

    # Required fields besides the password and USERNAME_FIELD when signing up.
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
