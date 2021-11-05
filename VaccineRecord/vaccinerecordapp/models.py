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

LOCATION = (
    ('R THIGH', 'R thigh'),
    ('L THIGH', 'L thigh'),
    ('R ARM', 'R arm'),
    ('L ARM', 'L arm'),
    ('R BUTTOCKS', 'R buttocks'),
    ('L BUTTOCKS', 'L buttocks')
)

STATUS = (
    ('CONFIRMED', 'Confirmed'),
    ('UNCONFIRMED', 'Unconfirmed'),
    ('POSTPONED', 'Postponed')
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
    
class Vaccine(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    patient_no = models.IntegerField(null=True,blank=True, unique=True)

    bcg_brand = models.CharField(max_length=100, blank=True, null=True)
    bcg_date = models.DateField(blank=True, null=True)
    bcg_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    bcg_rem = models.CharField(max_length=100, blank=True, null=True)

    hepb1_brand = models.CharField(max_length=100, blank=True, null=True)
    hepb1_date = models.DateField(blank=True, null=True)
    hepb1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hepb1_rem = models.CharField(max_length=100, blank=True, null=True)

    hepb2_brand = models.CharField(max_length=100, blank=True, null=True)
    hepb2_date = models.DateField(blank=True, null=True)
    hepb2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hepb2_rem = models.CharField(max_length=100, blank=True, null=True)

    hepb3_brand = models.CharField(max_length=100, blank=True, null=True)
    hepb3_date = models.DateField(blank=True, null=True)
    hepb3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hepb3_rem = models.CharField(max_length=100, blank=True, null=True)

    dtap1_brand = models.CharField(max_length=100, blank=True, null=True)
    dtap1_date = models.DateField(blank=True, null=True)
    dtap1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    dtap1_rem = models.CharField(max_length=100, blank=True, null=True)

    dtap2_brand = models.CharField(max_length=100, blank=True, null=True)
    dtap2_date = models.DateField(blank=True, null=True)
    dtap2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    dtap2_rem = models.CharField(max_length=100, blank=True, null=True)

    dtap3_brand = models.CharField(max_length=100, blank=True, null=True)
    dtap3_date = models.DateField(blank=True, null=True)
    dtap3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    dtap3_rem = models.CharField(max_length=100, blank=True, null=True)

    dtap4_brand = models.CharField(max_length=100, blank=True, null=True)
    dtap4_date = models.DateField(blank=True, null=True)
    dtap4_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    dtap4_rem = models.CharField(max_length=100, blank=True, null=True)

    dtap5_brand = models.CharField(max_length=100, blank=True, null=True)
    dtap5_date = models.DateField(blank=True, null=True)
    dtap5_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    dtap5_rem = models.CharField(max_length=100, blank=True, null=True)

    hib1_brand = models.CharField(max_length=100, blank=True, null=True)
    hib1_date = models.DateField(blank=True, null=True)
    hib1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hib1_rem = models.CharField(max_length=100, blank=True, null=True)

    hib2_brand = models.CharField(max_length=100, blank=True, null=True)
    hib2_date = models.DateField(blank=True, null=True)
    hib2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hib2_rem = models.CharField(max_length=100, blank=True, null=True)

    hib3_brand = models.CharField(max_length=100, blank=True, null=True)
    hib3_date = models.DateField(blank=True, null=True)
    hib3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hib3_rem = models.CharField(max_length=100, blank=True, null=True)

    hib4_brand = models.CharField(max_length=100, blank=True, null=True)
    hib4_date = models.DateField(blank=True, null=True)
    hib4_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hib4_rem = models.CharField(max_length=100, blank=True, null=True)

    hpv11_brand = models.CharField(max_length=100, blank=True, null=True)
    hpv11_date = models.DateField(blank=True, null=True)
    hpv11_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hpv11_rem = models.CharField(max_length=100, blank=True, null=True)

    hpv12_brand = models.CharField(max_length=100, blank=True, null=True)
    hpv12_date = models.DateField(blank=True, null=True)
    hpv12_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hpv12_rem = models.CharField(max_length=100, blank=True, null=True)

    hpv21_brand = models.CharField(max_length=100, blank=True, null=True)
    hpv21_date = models.DateField(blank=True, null=True)
    hpv21_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hpv21_rem = models.CharField(max_length=100, blank=True, null=True)

    hpv22_brand = models.CharField(max_length=100, blank=True, null=True)
    hpv22_date = models.DateField(blank=True, null=True)
    hpv22_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hpv22_rem = models.CharField(max_length=100, blank=True, null=True)

    hpv23_brand = models.CharField(max_length=100, blank=True, null=True)
    hpv23_date = models.DateField(blank=True, null=True)
    hpv23_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hpv23_rem = models.CharField(max_length=100, blank=True, null=True)

    hepa1_brand = models.CharField(max_length=100, blank=True, null=True)
    hepa1_date = models.DateField(blank=True, null=True)
    hepa1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hepa1_rem = models.CharField(max_length=100, blank=True, null=True)

    hepa2_brand = models.CharField(max_length=100, blank=True, null=True)
    hepa2_date = models.DateField(blank=True, null=True)
    hepa2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    hepa2_rem = models.CharField(max_length=100, blank=True, null=True)

    inf1_brand = models.CharField(max_length=100, blank=True, null=True)
    inf1_date = models.DateField(blank=True, null=True)
    inf1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    inf1_rem = models.CharField(max_length=100, blank=True, null=True)

    inf2_brand = models.CharField(max_length=100, blank=True, null=True)
    inf2_date = models.DateField(blank=True, null=True)
    inf2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    inf2_rem = models.CharField(max_length=100, blank=True, null=True)

    anf_brand = models.CharField(max_length=100, blank=True, null=True)
    anf_date = models.DateField(blank=True, null=True)
    anf_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    anf_rem = models.CharField(max_length=100, blank=True, null=True)

    ipv1_brand = models.CharField(max_length=100, blank=True, null=True)
    ipv1_date = models.DateField(blank=True, null=True)
    ipv1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    ipv1_rem = models.CharField(max_length=100, blank=True, null=True)

    ipv2_brand = models.CharField(max_length=100, blank=True, null=True)
    ipv2_date = models.DateField(blank=True, null=True)
    ipv2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    ipv2_rem = models.CharField(max_length=100, blank=True, null=True)

    ipv3_brand = models.CharField(max_length=100, blank=True, null=True)
    ipv3_date = models.DateField(blank=True, null=True)
    ipv3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    ipv3_rem = models.CharField(max_length=100, blank=True, null=True)

    ipv4_brand = models.CharField(max_length=100, blank=True, null=True)
    ipv4_date = models.DateField(blank=True, null=True)
    ipv4_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    ipv4_rem = models.CharField(max_length=100, blank=True, null=True)

    ipv5_brand = models.CharField(max_length=100, blank=True, null=True)
    ipv5_date = models.DateField(blank=True, null=True)
    ipv5_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    ipv5_rem = models.CharField(max_length=100, blank=True, null=True)

    japb1_brand = models.CharField(max_length=100, blank=True, null=True)
    japb1_date = models.DateField(blank=True, null=True)
    japb1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    japb1_rem = models.CharField(max_length=100, blank=True, null=True)

    japb2_brand = models.CharField(max_length=100, blank=True, null=True)
    japb2_date = models.DateField(blank=True, null=True)
    japb2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    japb2_rem = models.CharField(max_length=100, blank=True, null=True)

    msl_brand = models.CharField(max_length=100, blank=True, null=True)
    msl_date = models.DateField(blank=True, null=True)
    msl_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    msl_rem = models.CharField(max_length=100, blank=True, null=True)

    men_brand = models.CharField(max_length=100, blank=True, null=True)
    men_date = models.DateField(blank=True, null=True)
    men_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    men_rem = models.CharField(max_length=100, blank=True, null=True)

    mmr1_brand = models.CharField(max_length=100, blank=True, null=True)
    mmr1_date = models.DateField(blank=True, null=True)
    mmr1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    mmr1_rem = models.CharField(max_length=100, blank=True, null=True)

    mmr2_brand = models.CharField(max_length=100, blank=True, null=True)
    mmr2_date = models.DateField(blank=True, null=True)
    mmr2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    mmr2_rem = models.CharField(max_length=100, blank=True, null=True)

    pcv1_brand = models.CharField(max_length=100, blank=True, null=True)
    pcv1_date = models.DateField(blank=True, null=True)
    pcv1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    pcv1_rem = models.CharField(max_length=100, blank=True, null=True)

    pcv2_brand = models.CharField(max_length=100, blank=True, null=True)
    pcv2_date = models.DateField(blank=True, null=True)
    pcv2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    pcv2_rem = models.CharField(max_length=100, blank=True, null=True)

    pcv3_brand = models.CharField(max_length=100, blank=True, null=True)
    pcv3_date = models.DateField(blank=True, null=True)
    pcv3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    pcv3_rem = models.CharField(max_length=100, blank=True, null=True)

    pcv4_brand = models.CharField(max_length=100, blank=True, null=True)
    pcv4_date = models.DateField(blank=True, null=True)
    pcv4_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    pcv4_rem = models.CharField(max_length=100, blank=True, null=True)

    rota1_brand = models.CharField(max_length=100, blank=True, null=True)
    rota1_date = models.DateField(blank=True, null=True)
    rota1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    rota1_rem = models.CharField(max_length=100, blank=True, null=True)

    rota2_brand = models.CharField(max_length=100, blank=True, null=True)
    rota2_date = models.DateField(blank=True, null=True)
    rota2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    rota2_rem = models.CharField(max_length=100, blank=True, null=True)

    rota3_brand = models.CharField(max_length=100, blank=True, null=True)
    rota3_date = models.DateField(blank=True, null=True)
    rota3_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    rota3_rem = models.CharField(max_length=100, blank=True, null=True)

    td_brand = models.CharField(max_length=100, blank=True, null=True)
    td_date = models.DateField(blank=True, null=True)
    td_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    td_rem = models.CharField(max_length=100, blank=True, null=True)

    typ_brand = models.CharField(max_length=100, blank=True, null=True)
    typ_date = models.DateField(blank=True, null=True)
    typ_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    typ_rem = models.CharField(max_length=100, blank=True, null=True)

    var1_brand = models.CharField(max_length=100, blank=True, null=True)
    var1_date = models.DateField(blank=True, null=True)
    var1_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    var1_rem = models.CharField(max_length=100, blank=True, null=True)

    var2_brand = models.CharField(max_length=100, blank=True, null=True)
    var2_date = models.DateField(blank=True, null=True)
    var2_loc = models.CharField(choices=LOCATION,max_length=100, blank=True, null=True)
    var2_rem = models.CharField(max_length=100, blank=True, null=True)

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
    stat = models.CharField(choices=STATUS, max_length=11)

   