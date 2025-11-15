from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="Ім’я")
    last_name = forms.CharField(max_length=150, required=False, label="Прізвище")
    email = forms.EmailField(max_length=254, required=False, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
