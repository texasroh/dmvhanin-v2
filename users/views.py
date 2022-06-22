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
        username = models.User.objects.get(username=email)
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.nickname}")

        return super().form_valid(form)


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "auth/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        username = models.User.objects.get(username=email)
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.nickname}")

        return super().form_valid(form)


def log_out(request):
    messages.info(request, f"See you later, {request.user.nickname}")
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
