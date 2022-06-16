from core import models as core_models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, core_models.TimeStampModel):

    LOGIN_KAKAO = "kakao"
    LOGIN_GOOGLE = "google"
    LOGIN_EMAIL = "email"
    LOGIN_CHOICES = (
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_EMAIL, "Email"),
    )

    nickname = models.CharField(max_length=20, default="")
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        choices=LOGIN_CHOICES, max_length=10, default=LOGIN_EMAIL
    )
