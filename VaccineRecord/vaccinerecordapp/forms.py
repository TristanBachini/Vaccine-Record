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
from django.contrib.auth.models import Group
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
    input_formats = settings.DATE_INPUT_FORMATS

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
            'prefix':  Select(attrs={'class': 'form-control'}),
            'type':  Select(attrs={'class': 'form-control'}),
            'title':  Select(attrs={'class': 'form-control','required': False}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
            'contact': TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number', 'aria-label': 'Contact Number', 'required': True}),
        }

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
            # 'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
            # 'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
            'prefix':  Select(attrs={'class': 'form-control'}),
            'type':  Select(attrs={'class': 'form-control'}),
            'title':  Select(attrs={'class': 'form-control','required': False}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
            'contact': TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number', 'aria-label': 'Contact Number', 'required': True}),
        }

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
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        doctor = User.objects.filter(groups__name='doctor')
        fields = "__all__"
        widgets = {
            'user':HiddenInput(attrs={'type': 'hidden'}),
            'patient_username': HiddenInput(attrs={'type': 'hidden'}),
            'status': HiddenInput(attrs={'type': 'hidden'}),
            'date': DateInput(attrs={'class': 'form-control'}),
            'time':Select(attrs={'class': 'form-control'}),
            'doctor':Select(attrs={'class': 'form-control'}),
            'visit':Select(attrs={'class': 'form-control'}),
            'location':Select(attrs={'class': 'form-control'})
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
                'username': HiddenInput(attrs={'type': 'hidden'}),
                'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
                'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
                'middle_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle name', 'aria-label': 'Middle name', 'required': False}),
                'suffix': TextInput(attrs={'class': 'form-control', 'placeholder': 'Suffix', 'aria-label': 'Suffix', 'required': False}),
                'nick_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname', 'aria-label': 'Nickname', 'required': False}),
                'doctor_assigned': Select({'class': 'form-control'}),
                'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile', 'aria-label': 'Mobile', 'required': False}),
                'age': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'aria-label': 'Age', 'required': False}),
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

class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = "__all__"
        widgets = {
            'bcg_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'bcg_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'bcg_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'bcg_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepb1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepb2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'hepb3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap5_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap5_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap5_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap5_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hib1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hib2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hib3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hib4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv11_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv11_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv11_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv11_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hpv12_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv12_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv12_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv12_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv21_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv21_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv21_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv21_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv22_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv22_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv22_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv22_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'hpv23_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv23_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv23_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv23_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepa1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepa1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepa1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepa1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepa2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepa2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepa2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepa2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'inf1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'inf1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'inf1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'inf1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'inf2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'inf2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'inf2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'inf2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'anf_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'anf_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'anf_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'anf_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv5_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv5_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv5_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv5_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'japb1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'japb1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'japb1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'japb1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'japb2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'japb2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'japb2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'japb2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'msl_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'msl_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'msl_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'msl_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'men_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'men_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'men_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'men_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'mmr1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'mmr1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'mmr1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'mmr1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'mmr2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'mmr2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'mmr2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'mmr2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'pcv1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'pcv2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'pcv3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'pcv4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'td_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'td_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'td_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'td_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'typ_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'typ_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'typ_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'typ_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'var1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'var1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'var1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'var1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'var2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'var2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'var2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'var2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        }

class UpdateVaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),

            'bcg_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'bcg_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'bcg_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'bcg_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepb1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepb2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'hepb3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepb3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepb3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepb3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'dtap5_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'dtap5_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'dtap5_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'dtap5_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hib1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hib2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hib3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hib4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hib4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hib4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hib4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv11_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv11_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv11_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv11_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        
            'hpv12_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv12_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv12_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv12_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv21_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv21_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv21_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv21_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hpv22_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv22_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv22_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv22_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'hpv23_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hpv23_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hpv23_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hpv23_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepa1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepa1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepa1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepa1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'hepa2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'hepa2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'hepa2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'hepa2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'inf1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'inf1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'inf1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'inf1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'inf2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'inf2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'inf2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'inf2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'anf_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'anf_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'anf_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'anf_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'ipv5_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'ipv5_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'ipv5_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'ipv5_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'japb1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'japb1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'japb1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'japb1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'japb2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'japb2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'japb2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'japb2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'msl_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'msl_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'msl_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'msl_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'men_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'men_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'men_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'men_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'mmr1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'mmr1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'mmr1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'mmr1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'mmr2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'mmr2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'mmr2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'mmr2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'pcv1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'pcv2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'pcv3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'pcv4_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'pcv4_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'pcv4_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'pcv4_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'rota3_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'rota3_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'rota3_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'rota3_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'td_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'td_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'td_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'td_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'typ_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'typ_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'typ_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'typ_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
            
            'var1_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'var1_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'var1_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'var1_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),

            'var2_brand':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand', 'required': False}),
            'var2_date':  DateInput(attrs={'class': 'form-control', 'required': False}),
            'var2_loc':  Select(attrs={'class': 'form-control', 'required': False}),
            'var2_rem':  TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks', 'required': False}),
        }


# class DueVaccineForm(forms.Form):
#     date = forms.DateField( )
