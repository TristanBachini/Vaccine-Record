from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser, User
# Create your models here.

PREFIX = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.')
)

TITLE = (
    ('MD', 'MD'),
    ('RN', 'RN')
)

TYPE = (
    ('D', 'Doctor'),
    ('N', 'Nurse'),
    ('S', 'Secretary')
)

GENDER = (
    ('MALE','Male'),
    ('FEMALE','Female')
)

STATUS = (
    ('C', 'Confirmed'),
    ('UC', 'Unconfirmed'),
    ('P', 'Postponed')
)

class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
class Doctor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    prefix = models.CharField(choices=PREFIX, max_length=3)
    title = models.CharField(choices=TITLE, max_length=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    contact = models.CharField(max_length=100)
    type = models.CharField(choices=TYPE, max_length=2)
    can_register = models.BooleanField(default=False)

    def __str__(self):
        return "Dr. "+self.user.last_name




class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
    
    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("patient-profile", kwargs={
            "pk" : self.pk
        
        })

class PatientRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=100, blank=True, null=True)
    nick_name = models.CharField(max_length=100,  blank=True, null=True)
    doctor_assigned = ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    gender = models.CharField(choices=GENDER,max_length=11, null=True)
    bday = models.DateField(null=True)
    age = models.IntegerField(null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    landline = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(max_length=100,  blank=True, null=True) 
    home_no = models.CharField(max_length=100, blank=True, null=True)
    brgy = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    province = models.CharField(max_length=250, blank=True, null=True)
    region = models.CharField(max_length=250, blank=True, null=True)
    zip_code = models.CharField(max_length=4, blank=True, null=True)
    lname_mom = models.CharField(max_length=100, blank=True, null=True)
    fname_mom = models.CharField(max_length=100, blank=True, null=True)
    contact_mom = models.CharField(max_length=100, blank=True, null=True)
    email_mom = models.EmailField(max_length=100, blank=True, null=True)
    lname_dad = models.CharField(max_length=100,blank=True, null=True)
    fname_dad = models.CharField(max_length=100, blank=True, null=True)
    contact_dad = models.CharField(max_length=100, blank=True, null=True)
    email_dad = models.EmailField(max_length=100, blank=True, null=True)
    lname_e1 = models.CharField(max_length=100, blank=True, null=True)
    fname_e1 = models.CharField(max_length=100, blank=True, null=True)
    relation_e1 = models.CharField(max_length=100, blank=True, null=True)
    contact_e1 = models.CharField(max_length=100, blank=True, null=True)
    lname_e2 = models.CharField(max_length=100, blank=True, null=True)
    fname_e2 = models.CharField(max_length=100, blank=True, null=True)
    relation_e2 = models.CharField(max_length=100, blank=True, null=True)
    contact_e2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.last_name + "," + self.first_name

class Time(models.Model):
    time = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.time
class Visit(models.Model):
    visit = models.CharField(max_length=100,null = True)

    def __str__(self):
        return self.visit

class Location(models.Model):
    location = models.CharField(max_length=100,null = True)

    def __str__(self):
        return self.location

class Appointment(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)
    patient_username = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(null=True)
    time = models.ForeignKey(Time,on_delete=models.CASCADE,null=True)
    visit = models.ForeignKey(Visit,on_delete=models.CASCADE,null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    stat = models.CharField(choices=STATUS, max_length=2, default="UC")
