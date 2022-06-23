from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:secret>", views.complete_verification, name="verify"),
    path("login/google", views.google_login, name="google-login"),
    path("login/google/callback", views.google_callback, name="google-callback"),
    path("login/kakao", views.kakao_callback, name="kakao-callback"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
]
