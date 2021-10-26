from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.query import QuerySet
from django.forms import ModelForm, TextInput, PasswordInput, CharField, HiddenInput, NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import widgets, ModelForm
from django.forms.fields import BooleanField, ChoiceField
from django.forms.widgets import DateInput, Select
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

        

class DateInput(forms.DateInput):
    input_type = 'date'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
            'end_date': DateInput(),
        }


    # prefix = forms.CharField(widget=forms.TextInput(attrs={
    #     'prefix': 'form-control',
    #     'placeholder': 'Prefix'
    # }))
    # title = forms.CharField(widget=forms.TextInput(attrs={
    #     'title': 'form-control',
    #     'placeholder': 'Title'
    # }))
    # contact = forms.CharField(required=True, max_length=11, widget=forms.NumberInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': '09xxxxxxxxx'
    # }))
    # can_register = forms.BooleanField(required=True,initial=False,label='Can register')

class PatientForm(forms.ModelForm):
    attrs = {'class': 'form-control', 'id':'relationship',
             'placeholder': 'Relationship', 'required': True}
    relationship = CharField(widget=TextInput(attrs=attrs))
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
        }
class UpdatePatientRecordForm(forms.ModelForm):
    class Meta:
            model = PatientRecord
            fields = "__all__"
            widgets = {
                'bday': DateInput({'class': 'form-control'}),
                'gender': Select({'class': 'form-control'}),
                'username': HiddenInput(attrs={'type': 'hidden'}),
                'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
                'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
                'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle name', 'aria-label': 'Middle name', 'required': False}),
                'suffix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Suffix', 'aria-label': 'Suffix', 'required': False}),
                'nick_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname', 'aria-label': 'Nickname', 'required': False}),
                'doctor_assigned': HiddenInput(attrs={'type': 'hidden'}),
                'user': HiddenInput(attrs={'type': 'hidden'}),
                'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'age': TextInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'aria-label': 'Age', 'required': False}),
                'landline': TextInput(attrs={'class': 'form-control', 'placeholder': 'Landline', 'aria-label': 'Landline', 'required': False}),
                'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'home_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Unit No./Street', 'aria-label': 'House/Unit No./Street', 'required': False}),
                'brgy': TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay', 'aria-label': 'Barangay', 'required': False}),
                'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'aria-label': 'City', 'required': False}),
                'province': TextInput(attrs={'class': 'form-control', 'placeholder': 'Province', 'aria-label': 'Province', 'required': False}),
                'region': TextInput(attrs={'class': 'form-control', 'placeholder': 'Region', 'aria-label': 'Region', 'required': False}),
                'zip_code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code', 'aria-label': 'Zip Code', 'required': False}),
                'lname_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'contact_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'email_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'lname_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'email_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'contact_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'lname_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'relation_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship', 'aria-label': 'Relationship', 'required': False}),
                'contact_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'lname_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'relation_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship', 'aria-label': 'Relationship', 'required': False}),
                'contact_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
            }

class PatientRecordForm(forms.ModelForm):
    class Meta:
            model = PatientRecord
            fields = "__all__"
            widgets = {
                'bday': DateInput({'class': 'form-control'}),
                'gender': Select({'class': 'form-control'}),
                'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
                'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
                'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
                'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle name', 'aria-label': 'Middle name', 'required': False}),
                'suffix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Suffix', 'aria-label': 'Suffix', 'required': False}),
                'nick_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname', 'aria-label': 'Nickname', 'required': False}),
                'doctor_assigned': Select({'class': 'form-control'}),
                'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'age': TextInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'aria-label': 'Age', 'required': False}),
                'landline': TextInput(attrs={'class': 'form-control', 'placeholder': 'Landline', 'aria-label': 'Landline', 'required': False}),
                'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'home_no': TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Unit No./Street', 'aria-label': 'House/Unit No./Street', 'required': False}),
                'brgy': TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay', 'aria-label': 'Barangay', 'required': False}),
                'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'aria-label': 'City', 'required': False}),
                'province': TextInput(attrs={'class': 'form-control', 'placeholder': 'Province', 'aria-label': 'Province', 'required': False}),
                'region': TextInput(attrs={'class': 'form-control', 'placeholder': 'Region', 'aria-label': 'Region', 'required': False}),
                'zip_code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code', 'aria-label': 'Zip Code', 'required': False}),
                'lname_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'contact_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'email_mom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'lname_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'email_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': False}),
                'contact_dad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'lname_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'relation_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship', 'aria-label': 'Relationship', 'required': False}),
                'contact_e1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'lname_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': False}),
                'fname_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': False}),
                'relation_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship', 'aria-label': 'Relationship', 'required': False}),
                'contact_e2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
            }

class LoginForm(AuthenticationForm):
    attrs = {'class': 'form-control', 'id': 'floatingInput',
             'placeholder': 'Enter Password', 'required': True}
    username = forms.CharField(label='Email / Username',widget=TextInput(attrs={'placeholder':'Email'}))
    password = CharField(widget=PasswordInput(attrs=attrs))

