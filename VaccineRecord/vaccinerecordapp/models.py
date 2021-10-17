from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey
import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
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
        return self.user.username




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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    suffix = models.CharField(max_length=100, null=True)
    nick_name = models.CharField(max_length=100, null=True)
    doctor_assigned = ForeignKey(Doctor, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER,max_length=11, null=True)
    bday = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField(null=True)
    mobile = models.CharField(max_length=11, null=True)
    landline = models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=100, null=True) 
    home_no = models.CharField(max_length=100)
    brgy = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    province = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=4, null=True)
    lname_mom = models.CharField(max_length=100)
    fname_mom = models.CharField(max_length=100)
    contact_mom = models.CharField(max_length=100)
    email_mom = models.EmailField(max_length=100)
    lname_dad = models.CharField(max_length=100)
    fname_dad = models.CharField(max_length=100)
    contact_dad = models.CharField(max_length=100)
    email_dad = models.EmailField(max_length=100)
    lname_e1 = models.CharField(max_length=100)
    fname_e1 = models.CharField(max_length=100)
    relation_e1 = models.CharField(max_length=100)
    contact_e1 = models.CharField(max_length=100)
    name_e2 = models.CharField(max_length=100)
    fname_e2 = models.CharField(max_length=100)
    relation_e2 = models.CharField(max_length=100)
    contact_e2 = models.CharField(max_length=100)

    def __str__(self):
        return self.last_name + "," + self.first_name
