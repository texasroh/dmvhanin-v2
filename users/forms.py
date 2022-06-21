from django import forms

from . import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "password")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password"}),
        }


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "email",
            "nickname",
        )
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "nickname": forms.TextInput(attrs={"placeholder": "Nickname"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
