from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        )
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )