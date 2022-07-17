import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView, View

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"{user.nickname}님 안녕하세요.")

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next", reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.save()
        # email = form.cleaned_data.get("email")
        # password = form.cleaned_data.get("password")
        # user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"{user.nickname}님 환영합니다.")
            user.verify_email()

        return super().form_valid(form)


# class ProfileView(mixins.LoggedInOnlyView, View):
#     def get(self, request):
#         nickname_form = forms.NicknameForm(initial={"nickname": request.user.nickname})
#         return render(request, "auth/profile.html", {"form": nickname_form})

#     def post(self, request):
#         action = request.POST.get("action")
#         if action == "nickname":
#             nickname_form = forms.NicknameForm(request.POST)
#             if nickname_form.is_valid():
#                 request.user.nickname = nickname_form.cleaned_data.get("nickname")
#                 request.user.save()
#                 messages.success(request, "닉네임 변경 완료")
#                 return redirect(reverse("users:profile"))
#         elif action == "password":
#             pass
#         return render(request, "auth/profile.html", {"form": nickname_form})


class ProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    template_name = "auth/profile.html"
    # fields = ("nickname",)
    success_message = "닉네임 변경 완료"
    success_url = reverse_lazy("users:profile")
    form_class = forms.NicknameForm

    def get_object(self):
        return models.User.objects.get(pk=self.request.user.pk)


class PasswordUpdateView(
    mixins.LoggedInOnlyView,
    mixins.HasUsablePasswordOnly,
    SuccessMessageMixin,
    PasswordChangeView,
):
    success_message = "비밀번호 변경 완료"
    template_name = "auth/password-update.html"
    success_url = reverse_lazy("users:profile")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재 비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새 비밀번호"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "비밀번호 확인"}
        return form


@mixins.login_only
def send_email_verification(request):
    request.user.verify_email()
    return HttpResponse(status=201)


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
        login(request, user)
        messages.success(request, "이메일 인증 완료.")
    except models.User.DoesNotExist:
        messages.error(request, "이메일 인증 실패")

    return redirect(reverse("users:profile"))


def google_login(request):
    CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    REDIRECT_URI = os.environ.get("DOMAIN") + reverse("users:google-callback")
    next = request.GET.get("next", None)
    url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    if next:
        url += f"&state={next}"
    return redirect(url)


class GoogleException(Exception):
    pass


def google_callback(request):
    try:
        if "error" in request.GET:
            raise GoogleException("에러 발생")
            # messages.error('에러 발생')
            # return redirect(reverse('core:home'))
        code = request.GET.get("code")
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.environ.get("DOMAIN") + reverse("users:google-callback")
        token_request = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_json = token_request.json()
        if "error" in token_json:
            raise GoogleException("에러 발생")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        id = profile_json.get("id")
        try:
            user = models.User.objects.get(google_id=id)
        except models.User.DoesNotExist:
            email = profile_json.get("email")
            try:
                user = models.User.objects.get(email=email)
                user.google_id = id
                user.email_verified = True
                user.email_secret = None
                user.save()
            except models.User.DoesNotExist:
                user = models.User.objects.create_user(
                    email, None, google_id=id, email_verified=True
                )
                user.set_unusable_password()
                user.save()
                nickname = profile_json.get("name")
                try:
                    user.nickname = nickname
                    user.save()
                except IntegrityError:
                    user.nickname = None

        login(request, user)
        if user.nickname:
            messages.success(request, f"{user.nickname}님 안녕하세요.")

            state = request.GET.get("state")
            if state:
                return redirect(state)
            return redirect(reverse("core:home"))
        messages.info(request, "닉네임을 설정해주세요")
        return redirect(reverse("users:profile"))
    except GoogleException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


@mixins.logout_required
def kakao_login(request):
    REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
    REDIRECT_URI = os.environ.get("DOMAIN") + reverse("users:kakao-callback")
    next = request.GET.get("next", None)
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&scope=account_email"
    if next:
        url += f"&state={next}"
    return redirect(url)


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
        id = profile_json.get("id")
        try:
            user = models.User.objects.get(kakao_id=id)
        except models.User.DoesNotExist:
            email = profile_json.get("kakao_account").get("email")
            try:
                user = models.User.objects.get(email=email)
                user.kakao_id = id
                user.email_verified = True
                user.email_secret = None
                user.save()
            except models.User.DoesNotExist:
                user = models.User.objects.create_user(
                    email,
                    None,
                    kakao_id=id,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
                try:
                    nickname = profile_json.get("properties").get("nickname")
                    user.nickname = nickname
                    user.save()
                except IntegrityError:
                    user.nickname = None

        login(request, user)
        if user.nickname:
            messages.success(request, f"{user.nickname}님 안녕하세요.")
            state = request.GET.get("state")
            if state:
                return redirect(state)
            return redirect(reverse("core:home"))
        messages.info(request, "닉네임을 설정해주세요")
        return redirect(reverse("users:profile"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
