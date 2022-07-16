from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("send-verification", views.send_email_verification, name="send-verification"),
    path("verify/<str:secret>", views.complete_verification, name="verify"),
    path("login/google", views.google_login, name="google-login"),
    path("login/google/callback", views.google_callback, name="google-callback"),
    path("login/kakao", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("password", views.PasswordUpdateView.as_view(), name="password"),
]
