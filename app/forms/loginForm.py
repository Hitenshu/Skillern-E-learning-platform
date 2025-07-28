from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(required = True)
    password = forms.CharField(required = True)
