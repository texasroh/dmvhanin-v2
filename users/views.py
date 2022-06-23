import os

import requests
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
            messages.success(self.request, f"{user.nickname}님 안녕하세요.")

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


@mixins.logout_required
def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.environ.get("DOMAIN") + reverse("users:kakao-callback")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_REST_API_KEY")
        redirect_uri = os.environ.get("DOMAIN") + reverse("users:kakao-callback")
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        )
        token_json = token_request.json()
        if "error" in token_json:
            raise KakaoException("카카오 로그인 할 수 없습니다.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer ${access_token}",
            },
        )
        profile_json = profile_request.json()
        id = f"{models.User.LOGIN_KAKAO}_{profile_json.get('id')}"

        try:
            user = models.User.objects.get(username=id)
        except models.User.DoesNotExist:
            email = profile_json.get("kakao_account").get("email")
            nickname = profile_json.get("properties").get("nickname")
            user = models.User(
                username=id,
                email=email,
                nickname=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True if email else False,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, f"{user.nickname}님 안녕하세요.")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
