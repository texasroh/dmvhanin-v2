import os

from core import models as core_models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import IntegrityError, models
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags


class UserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        # email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, core_models.TimeStampModel):

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    nickname = models.CharField(max_length=50, unique=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, null=True, unique=True)
    google_id = models.CharField(max_length=100, null=True, unique=True)
    kakao_id = models.CharField(max_length=100, null=True, unique=True)

    objects = UserManager()

    def verify_email(self):
        if self.email_verified:
            return

        while True:
            try:
                secret = get_random_string(32)
                self.email_secret = secret
                self.save()
                break
            except IntegrityError:
                print("Integrity Error June")
        html_message = render_to_string(
            "emails/verify_email.html",
            {
                "secret": secret,
                "domain": os.environ.get("DOMAIN", "http://127.0.0.1:8000"),
            },
        )
        send_mail(
            "Verify your account",
            strip_tags(html_message),
            settings.EMAIL_FROM,
            [self.email],
            fail_silently=False,
            html_message=html_message,
        )
