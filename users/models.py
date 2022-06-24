import os

from core import models as core_models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags


class User(AbstractUser, core_models.TimeStampModel):

    email = models.EmailField("email address", unique=True, null=True)
    nickname = models.CharField(max_length=50, unique=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, null=True, unique=True)
    google_id = models.CharField(max_length=100, null=True, unique=True)
    kakao_id = models.CharField(max_length=100, null=True, unique=True)

    def verify_email(self):
        if self.email_verified or not self.email:
            return

        secret = get_random_string(32)
        self.email_secret = secret
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
        self.save()
