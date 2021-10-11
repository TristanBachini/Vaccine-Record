from django import forms
from django.db import models
from django.db.models import fields
from django.forms import ModelForm, TextInput, PasswordInput, CharField, HiddenInput, NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import widgets
from django.forms.widgets import Select
from .models import *
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    attrs = {'class': 'form-control', 'id': 'floatingInput',
             'placeholder': 'Enter Password', 'required': True}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))

    class Meta:
        User = get_user_model()
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'aria-label': 'Username', 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': True}),
        }

class LoginForm(AuthenticationForm):
    attrs = {'class': 'form-control', 'id': 'floatingInput',
             'placeholder': 'Enter Password', 'required': True}
    username = forms.CharField(label='Email / Username',widget=TextInput(attrs={'placeholder':'Email'}))
    password = CharField(widget=PasswordInput(attrs=attrs))