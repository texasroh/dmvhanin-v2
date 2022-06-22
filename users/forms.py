from django import forms
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

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean_email(self):
        return self.cleaned_data.get("email").lower()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != "email":
                raise forms.ValidationError("Login with google or kakao")
            if not user.check_password(password):
                self.add_error("password", forms.ValidationError("Wrong password"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
        return super().clean()


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "nickname", "password")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "nickname": forms.TextInput(attrs={"placeholder": "Nickname"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password"}),
        }

    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    # )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        return self.cleaned_data.get("email").lower()

    def clean(self):
        password = self.cleaned_data.get("password")
        # validate_password(password)
        try:
            validate_password(password)
        except PWValidationError as errors:
            self.add_error("password", forms.ValidationError(errors))

        password1 = self.cleaned_data.get("password1")
        if password != password1:
            self.add_error(
                "password1",
                forms.ValidationError("Password confirmation does not match"),
            )
        return super().clean()

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        # user.email = email.lower()
        user.username = email
        user.set_password(password)
        user.save()
