from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"{user.nickname}님 어서오세요")

        return super().form_valid(form)


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"{user.nickname}님 환영합니다.")
            user.verify_email()

        return super().form_valid(form)


def log_out(request):
    messages.info(request, "다음에 또 봐요.")
    logout(request)
    return redirect(reverse("core:home"))


def complete_verification(request, secret):
    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = None
        user.save()
        messages.success(request, "이메일 인증 완료. 로그인 해주세요.")
    except models.User.DoesNotExist:
        messages.error(request, "이메일 인증 실패")

    return redirect(reverse("core:home"))


def google_login(request):
    pass


def google_callback(request):
    pass


def kakao_login(request):
    pass


def kakao_callback(request):
    pass
