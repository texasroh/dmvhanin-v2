from functools import wraps

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def handle_no_permission(self):
        messages.error(self.request, "Login required")
        return super().handle_no_permission()


def logout_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404()
        return func(request, *args, **kwargs)

    return wrapper
