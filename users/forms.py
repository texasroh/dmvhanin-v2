from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as PWValidationError

from . import models


class LoginForm(forms.Form):
    # class Meta:
    #     model = models.User
    #     fields = ("email", "password")
    #     widgets = {
    #         "email": forms.EmailInput(attrs={"placeholder": "Email"}),
    #         "password": forms.PasswordInput(attrs={"placeholder": "Password"}),
    #     }

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean_email(self):
        return self.cleaned_data.get("email").lower()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if not user.check_password(password):
                self.add_error("password", forms.ValidationError("잘못된 비밀번호 입니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 계정입니다."))
        return super().clean()


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "nickname", "password")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
            "nickname": forms.TextInput(attrs={"placeholder": "닉네임"}),
            "password": forms.PasswordInput(attrs={"placeholder": "비밀번호"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_email(self):
        return self.cleaned_data.get("email").lower()

    def clean(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except PWValidationError as errors:
            self.add_error("password", forms.ValidationError(errors))

        password1 = self.cleaned_data.get("password1")
        if password != password1:
            self.add_error(
                "password1",
                forms.ValidationError("비밀번호가 일치하지 않습니다."),
            )
        return super().clean()

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        nickname = self.cleaned_data.get("nickname")
        user = models.User.objects.create_user(email, password, nickname=nickname)
        return user
        # user = super().save(commit=False)
        # user.set_password(password)
        # user.save()


class NicknameForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("nickname",)

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        try:
            models.User.objects.get(nickname=nickname)
            raise forms.ValidationError("이미 존재하는 닉네임입니다.")
        except models.User.DoesNotExist:
            pass
        return nickname


class PasswordForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("password",)
        widgets = {"password": forms.PasswordInput(attrs={"placeholder": "현재 비밀번호"})}

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "새 비밀번호"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not authenticate()
