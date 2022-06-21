from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView

from . import forms, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/signup.html"
    form_class = forms.SignUpForm


def log_out(request):
    messages.info(request, f"See you later {request.user.nick_name}")
    logout(request)
    return redirect(reverse("core:home"))


def verify(request, secret):
    pass


def google_login(request):
    pass


def google_callback(request):
    pass


def kakao_login(request):
    pass


def kakao_callback(request):
    pass
