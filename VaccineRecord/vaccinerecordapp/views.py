from collections import Counter
from os import name
from django.forms.widgets import DateTimeBaseInput
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from VaccineRecord.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template
from xhtml2pdf import pisa
from .filters import RecordFilter
from django.views.generic import View
from django.utils import timezone
# Create your views here.

def home(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            if user.groups.filter(name="Staff") or user.groups.filter(name="Doctor"):
                form1 = UserForm(request.POST)
                form2 = PatientForm(request.POST)
                patients = User.objects.filter(groups__name="Patient")
                if user.groups.filter(name="Doctor"):
                    appointments = Appointment.objects.filter(doctor = Doctor.objects.get(user_id = request.user.id).id)
                    count = appointments.count()
                    print(user)
                    data = {"form1":form1, "form2":form2, "patients":patients,"appointments":appointments,"count":count}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
                if user.groups.filter(name="Staff"):
                    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
                    count = appointments.count()
                    data = {"form1":form1, "form2":form2, "patients":patients,"appointments":appointments,"count":count}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
                else:
                    print(user)
                    data = {"form1":form1, "form2":form2, "patients":patients}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
            else:
                print(user)
                record = PatientRecord.objects.get(user = request.user)
                data = {'record':record}
                return render(request, 'vaccinerecordapp/patient-landing.html',data)
        else:
            messages.error(request,"Invalid Email or Password")
    form = LoginForm()
    data = {"form":form}
        
    return render(request, 'vaccinerecordapp/home.html',data)


@login_required(login_url='/home')
def dashboard(request):
    appointments = Appointment.objects.all()
    count = appointments.count()

    if request.user.groups.filter(name="Doctor") or request.user.groups.filter(name="Staff"):
        appointments = Appointment.objects.filter(doctor = Doctor.objects.get(user_id = request.user.id).id)
        count = appointments.count()
    else:
        appointments = Appointment.objects.filter(user = request.user)
        count = appointments.count()
    data = {'appointments' : appointments,
            'count': count}
    return render(request,'vaccinerecordapp/dashboard.html', data)

def create_record(request,username):
    form = PatientRecordForm()
    patients = PatientRecord.objects.all()
    if(request.method == "POST"):  
        user = User.objects.get(username=username)
        form = PatientRecordForm({'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'),
                                        'middle_name':request.POST.get('middle_name'), 'suffix':request.POST.get('suffix'), 'nick_name':request.POST.get('nick_name'),
                                        'doctor_assigned':request.POST.get('doctor_assigned'), 'gender':request.POST.get('gender'), 'bday':request.POST.get('bday'),
                                        'age':request.POST.get('age'), 'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
                                        'email':request.POST.get('email'), 'home_no':request.POST.get('home_no'), 'brgy':request.POST.get('brgy'), 
                                        'city':request.POST.get('city'),'province':request.POST.get('province'), 'region':request.POST.get('region'),
                                        'zip_code':request.POST.get('zip_code'), 'lname_mom':request.POST.get('lname_mom'),'fname_mom':request.POST.get('fname_mom'),
                                        'contact_mom':request.POST.get('contact_mom'),'email_mom':request.POST.get('email_mom'),'lname_dad':request.POST.get('lname_dad'),
                                        'fname_dad':request.POST.get('fname_dad'),'contact_dad':request.POST.get('contact_dad'), 'email_dad':request.POST.get('email_dad'),
                                        'lname_e1':request.POST.get('lname_e1'),'fname_e1':request.POST.get('fname_e1'),'relation_e1':request.POST.get('relation_e1'),
                                        'contact_e1':request.POST.get('contact_e1'),'lname_e2':request.POST.get('lname_e2'),'fname_e2':request.POST.get('fname_e2'),'relation_e2':request.POST.get('relation_e2'),
                                        'contact_e2':request.POST.get('contact_e2')})
        if(form.is_valid()):
            print('is valid')
            form.save()
            print("nagsave")
            messages.success(request, "Patient was created for " +
                             form.cleaned_data.get("first_name") + form.cleaned_data.get("last_name"))
            return redirect('/search-patient')
        else:
            print(form.errors)
    else:
        messages.error(request, "Something was wrong with the input, please try again and make sure every field is filled is filled correctly.")
    data = {"form":form, "patients":patients,"username":username}
    return render(request, 'vaccinerecordapp/account-creation/create-patient-record.html',data)

def update_patient_profile(request,pk):
    patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
    form = UpdatePatientRecordForm(instance = patient)
    record = PatientRecord.objects.get(id = pk)
    if(request.method=="POST"):   
        user = User.objects.get(username=request.user.username)
        form = PatientRecordForm({ 'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'),
                                        'middle_name':request.POST.get('middle_name'), 'suffix':request.POST.get('suffix'), 'nick_name':request.POST.get('nick_name'),
                                        'doctor_assigned':request.POST.get('doctor_assigned'), 'gender':request.POST.get('gender'), 'bday':request.POST.get('bday'),
                                        'age':request.POST.get('age'), 'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
                                        'email':request.POST.get('email'), 'home_no':request.POST.get('home_no'), 'brgy':request.POST.get('brgy'), 
                                        'city':request.POST.get('city'),'province':request.POST.get('province'), 'region':request.POST.get('region'),
                                        'zip_code':request.POST.get('zip_code'), 'lname_mom':request.POST.get('lname_mom'),'fname_mom':request.POST.get('fname_mom'),
                                        'contact_mom':request.POST.get('contact_mom'),'email_mom':request.POST.get('email_mom'),'lname_dad':request.POST.get('lname_dad'),
                                        'fname_dad':request.POST.get('fname_dad'),'contact_dad':request.POST.get('contact_dad'), 'email_dad':request.POST.get('email_dad'),
                                        'lname_e1':request.POST.get('lname_e1'),'fname_e1':request.POST.get('fname_e1'),'relation_e1':request.POST.get('relation_e1'),
                                        'contact_e1':request.POST.get('contact_e1'),'lname_e2':request.POST.get('lname_e2'),'fname_e2':request.POST.get('fname_e2'),'relation_e2':request.POST.get('relation_e2'),
                                        'contact_e2':request.POST.get('contact_e2')}, instance = patient)
        if(form.is_valid()):
            form.save()
            record = PatientRecord.objects.get(id = pk)
            data = {"record":record}
            return render(request, "vaccinerecordapp/patient-landing.html",data)
    data = {"form":form,"record":record}
    return render(request, "vaccinerecordapp/update-patient-profile.html", data)

def update_profile(request,pk):
    patient = PatientRecord.objects.get(id = pk).user
    profile = PatientRecord.objects.get(user=patient)
    form = UpdatePatientRecordForm(instance = profile)
    record = PatientRecord.objects.get(id = pk)
    if(request.method=="POST"):   
        user = User.objects.get(username=patient)
        form = PatientRecordForm({ 'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'),
                                        'middle_name':request.POST.get('middle_name'), 'suffix':request.POST.get('suffix'), 'nick_name':request.POST.get('nick_name'),
                                        'doctor_assigned':request.POST.get('doctor_assigned'), 'gender':request.POST.get('gender'), 'bday':request.POST.get('bday'),
                                        'age':request.POST.get('age'), 'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
                                        'email':request.POST.get('email'), 'home_no':request.POST.get('home_no'), 'brgy':request.POST.get('brgy'), 
                                        'city':request.POST.get('city'),'province':request.POST.get('province'), 'region':request.POST.get('region'),
                                        'zip_code':request.POST.get('zip_code'), 'lname_mom':request.POST.get('lname_mom'),'fname_mom':request.POST.get('fname_mom'),
                                        'contact_mom':request.POST.get('contact_mom'),'email_mom':request.POST.get('email_mom'),'lname_dad':request.POST.get('lname_dad'),
                                        'fname_dad':request.POST.get('fname_dad'),'contact_dad':request.POST.get('contact_dad'), 'email_dad':request.POST.get('email_dad'),
                                        'lname_e1':request.POST.get('lname_e1'),'fname_e1':request.POST.get('fname_e1'),'relation_e1':request.POST.get('relation_e1'),
                                        'contact_e1':request.POST.get('contact_e1'),'lname_e2':request.POST.get('lname_e2'),'fname_e2':request.POST.get('fname_e2'),'relation_e2':request.POST.get('relation_e2'),
                                        'contact_e2':request.POST.get('contact_e2')}, instance = profile)
        if(form.is_valid()):
            form.save()
            record = PatientRecord.objects.get(id = pk)
            data = {"record":record}
            return render(request, "vaccinerecordapp/search-patient.html",data)
    data = {"form":form,"record":record}
    return render(request, "vaccinerecordapp/update-profile.html", data)

def create_patient(request):
    form1 = UserForm()
    form2 = PatientForm()
    
    if(request.method == "POST"):
        form1 = UserForm(request.POST)
        form2 = PatientForm(request.POST)
        try:
            user_exists = User.objects.get(username=request.POST['username'])
            messages.error(request, "Username is already taken, please choose another.")
            form1 = UserForm()
            form2 = PatientForm()
            data = {"form1":form1, "form2":form2}
            return render(request, 'vaccinerecordapp/portal.html',data)
        except User.DoesNotExist:
            try:
                email_exists = User.objects.get(email=request.POST['email'])
                messages.error(request, "This email is already in use. If you forgot your password, kindly click forgot password upon login.")
                form1 = UserForm()
                form2 = PatientForm()
                data = {"form1":form1, "form2":form2}
                return render(request, 'vaccinerecordapp/portal.html',data)
            except User.DoesNotExist:
                if(form1.is_valid()):
                    if(request.POST['password1']!=request.POST['password2']):
                        messages.error(request, "The passwords do not match. Please try again.")
                        form1 = UserForm()
                        form2 = PatientForm()
                        data = {"form1":form1, "form2":form2}
                        return render(request, 'vaccinerecordapp/portal.html',data)
                    else:
                        form1.save()
                        user = User.objects.get(username = form1.cleaned_data.get("username"))
                        print(user)
                        lname = user.last_name
                        fname = user.first_name
                        form2 = PatientForm({'user':user, 'last_name': lname, 'first_name': fname, 'relationship':request.POST.get('relationship')})
                if(form2.is_valid()):
                    form2.save()
                    vaccineform = VaccineForm()
                    if(vaccineform.is_valid()):
                        print("valid naman sha")
                        vaccineform.save()
                    messages.success(request, "Account was created for " +
                                    form1.cleaned_data.get("username"))
                    group = Group.objects.get(name="patient")
                    user = User.objects.get(username = form1.cleaned_data.get("username"))
                    user.groups.add(group) 
                    username = form1.cleaned_data.get("username")
                    return create_record(request,username)


    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/portal.html',data)

def register_patient(request):
    form1 = UserForm()
    form2 = PatientForm()
    
    if(request.method == "POST"):
        form1 = UserForm(request.POST)
        form2 = PatientForm(request.POST)
        if(form1.is_valid()):
            form1.save()
            user = User.objects.get(username = form1.cleaned_data.get("username"))
            print(user)
            lname = user.last_name
            fname = user.first_name
            form2 = PatientForm({'user':user, 'last_name': lname, 'first_name': fname, 'relationship':request.POST.get('relationship')})
        else:
            data = {"form1":form1, "form2":form2}
            return render(request, 'vaccinerecordapp/register-patient.html',data)
        if(form2.is_valid()):
            form2.save()
            vaccineform = VaccineForm({'user':User.objects.get(username = form1.cleaned_data.get("username"))})
            if vaccineform.is_valid():
                vaccineform.save()
            messages.success(request, "Account was created for " +
                            form1.cleaned_data.get("username"))
            group = Group.objects.get(name="patient")
            user = User.objects.get(username = form1.cleaned_data.get("username"))
            user.groups.add(group) 
            username = form1.cleaned_data.get("username")
            return create_record(request,username)


    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/register-patient.html',data)

def create_staff(request):
    form1 = UserForm()
    form2 = DoctorForm()

    if(request.method == "POST"):
        form1 = UserForm(request.POST)
        form2 = DoctorForm(request.POST)
        if(form1.is_valid()):
            form1.save()
            user = User.objects.get(username = form1.cleaned_data.get("username"))
            form2 = DoctorForm({'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'), 'contact':request.POST.get('contact'),'prefix':request.POST.get('prefix'),
            'title':request.POST.get('title'),'type':request.POST.get('type'),'end_date':request.POST.get('end_date'),
            'can_register':request.POST.get('can_register')})
            print("yea this worked")
        if(form2.is_valid()):
            form2.save()
            messages.success(request, "Account was created for " +
                             form1.cleaned_data.get("username"))
            print(form2.cleaned_data.get("can_register"))
            if(form2.cleaned_data.get("can_register")==True):
                group = Group.objects.get(name="staff")
                user = User.objects.get(username = form1.cleaned_data.get("username"))
                user.groups.add(group) 
            else:
                group = Group.objects.get(name="doctor")
                user = User.objects.get(username = form1.cleaned_data.get("username"))
                user.groups.add(group) 
            
            return redirect('/dashboard')
        else:
            print(form2.errors)
    else:
        messages.error(request, "Something was wrong with the input, please try again and make sure every field is filled correctly.")

    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/tool/staff.html',data)

def display_vaccine_record(request,pk):
    form = VaccineForm(request.POST)
    record = PatientRecord.objects.get(id = pk)
    vac = PatientRecord.objects.get(id = pk).user
    #vac =  User.objects.get(user=PatientRecord.objects.get(user=PatientRecord.objects.get(id=pk).user).user).username
    #vac = Vaccine.objects.get(user=PatientRecord.objects.get(user=Patient.objects.get(user=User.objects.get(id=pk).id).id).user)
    print(vac)
    if Vaccine.objects.filter(user=vac).exists():
        vaccine = Vaccine.objects.get(user=vac)
        data = {"record":record, "vaccine":vaccine, "form":form}
        return render(request, 'vaccinerecordapp/display-vaccine.html',data)
    else:
        return create_vaccine_record(request,pk)

def create_vaccine_record(request,pk):
    form = VaccineForm(request.POST)
    record = PatientRecord.objects.get(id=pk)
    data = {"form":form,"record":record}
    return render(request,'vaccinerecordapp/vaccine-record.html',data)

def vaccine_record(request):
    #form = PatientRecordForm(request.POST)
    #record = PatientRecord.objects.get(id=pk)
    form = VaccineForm()
    
    if(request.method == "POST"):
        form = VaccineForm(request.POST)
        print("pumasok post")
        username = request.POST.get('username')
        print('username')        
        user = User.objects.get(username=username)
        form = VaccineForm({'user':user, 
                                'bcg_brand':request.POST.get('bcg_brand'),'bcg_date':request.POST.get('bcg_date'),'bcg_loc':request.POST.get('bcg_loc'),'bcg_rem':request.POST.get('bcg_rem'),
                                
                                'hepb1_brand':request.POST.get('hepb1_brand'),'hepb1_date':request.POST.get('hepb1_date'),'hepb1_loc':request.POST.get('hepb1_loc'),'hepb1_rem':request.POST.get('hepb1_rem'),
                                'hepb2_brand':request.POST.get('hepb2_brand'),'hepb2_date':request.POST.get('hepb2_date'),'hepb2_loc':request.POST.get('hepb2_loc'),'hepb2_rem':request.POST.get('hepb2_rem'),
                                'hepb3_brand':request.POST.get('hepb3_brand'),'hepb3_date':request.POST.get('hepb3_date'),'hepb3_loc':request.POST.get('hepb3_loc'),'hepb3_rem':request.POST.get('hepb3_rem'),
                                
                                'dtap1_brand':request.POST.get('dtap1_brand'),'dtap1_date':request.POST.get('dtap1_date'),'dtap1_loc':request.POST.get('dtap1_loc'),'dtap1_rem':request.POST.get('dtap1_rem'),
                                'dtap2_brand':request.POST.get('dtap2_brand'),'dtap2_date':request.POST.get('dtap2_date'),'dtap2_loc':request.POST.get('dtap2_loc'),'dtap2_rem':request.POST.get('dtap2_rem'),
                                'dtap3_brand':request.POST.get('dtap3_brand'),'dtap3_date':request.POST.get('dtap3_date'),'dtap3_loc':request.POST.get('dtap3_loc'),'dtap3_rem':request.POST.get('dtap3_rem'),
                                'dtap4_brand':request.POST.get('dtap4_brand'),'dtap4_date':request.POST.get('dtap4_date'),'dtap4_loc':request.POST.get('dtap4_loc'),'dtap4_rem':request.POST.get('dtap4_rem'),
                                'dtap5_brand':request.POST.get('dtap5_brand'),'dtap5_date':request.POST.get('dtap5_date'),'dtap5_loc':request.POST.get('dtap5_loc'),'dtap5_rem':request.POST.get('dtap5_rem'),

                                'hib1_brand':request.POST.get('hib1_brand'),'hib1_date':request.POST.get('hib1_date'),'hib1_loc':request.POST.get('hib1_loc'),'hib1_rem':request.POST.get('hib1_rem'),
                                'hib2_brand':request.POST.get('hib2_brand'),'hib2_date':request.POST.get('hib2_date'),'hib2_loc':request.POST.get('hib2_loc'),'hib2_rem':request.POST.get('hib2_rem'),
                                'hib3_brand':request.POST.get('hib3_brand'),'hib3_date':request.POST.get('hib3_date'),'hib3_loc':request.POST.get('hib3_loc'),'hib3_rem':request.POST.get('hib3_rem'),
                                'hib4_brand':request.POST.get('hib4_brand'),'hib4_date':request.POST.get('hib4_date'),'hib4_loc':request.POST.get('hib4_loc'),'hib4_rem':request.POST.get('hib4_rem'),

                                'hpv11_brand':request.POST.get('hpv11_brand'),'hpv11_date':request.POST.get('hpv11_date'),'hpv11_loc':request.POST.get('hpv11_loc'),'hpv11_rem':request.POST.get('hpv11_rem'),
                                'hpv12_brand':request.POST.get('hpv12_brand'),'hpv12_date':request.POST.get('hpv12_date'),'hpv12_loc':request.POST.get('hpv12_loc'),'hpv12_rem':request.POST.get('hpv12_rem'),

                                'hpv21_brand':request.POST.get('hpv21_brand'),'hpv21_date':request.POST.get('hpv21_date'),'hpv21_loc':request.POST.get('hpv21_loc'),'hpv21_rem':request.POST.get('hpv21_rem'),
                                'hpv22_brand':request.POST.get('hpv22_brand'),'hpv22_date':request.POST.get('hpv22_date'),'hpv22_loc':request.POST.get('hpv22_loc'),'hpv22_rem':request.POST.get('hpv22_rem'),
                                'hpv23_brand':request.POST.get('hpv23_brand'),'hpv23_date':request.POST.get('hpv23_date'),'hpv23_loc':request.POST.get('hpv23_loc'),'hpv23_rem':request.POST.get('hpv23_rem'),

                                'hepa1_brand':request.POST.get('hepa1_brand'),'hepa1_date':request.POST.get('hepa1_date'),'hepa1_loc':request.POST.get('hepa1_loc'),'hepa1_rem':request.POST.get('hepa1_rem'),
                                'hepa2_brand':request.POST.get('hepa2_brand'),'hepa2_date':request.POST.get('hepa2_date'),'hepa2_loc':request.POST.get('hepa2_loc'),'hepa2_rem':request.POST.get('hepa2_rem'),

                                'inf1_brand':request.POST.get('inf1_brand'),'inf1_date':request.POST.get('inf1_date'),'inf1_loc':request.POST.get('inf1_loc'),'inf1_rem':request.POST.get('inf1_rem'),
                                'inf2_brand':request.POST.get('inf2_brand'),'inf2_date':request.POST.get('inf2_date'),'inf2_loc':request.POST.get('inf2_loc'),'inf2_rem':request.POST.get('inf2_rem'),

                                'anf_brand':request.POST.get('anf_brand'),'anf_date':request.POST.get('anf_date'),'anf_loc':request.POST.get('anf_loc'),'anf_rem':request.POST.get('anf_rem'),

                                'ipv1_brand':request.POST.get('ipv1_brand'),'ipv1_date':request.POST.get('ipv1_date'),'ipv1_loc':request.POST.get('ipv1_loc'),'ipv1_rem':request.POST.get('ipv1_rem'),
                                'ipv2_brand':request.POST.get('ipv2_brand'),'ipv2_date':request.POST.get('ipv2_date'),'ipv2_loc':request.POST.get('ipv2_loc'),'ipv2_rem':request.POST.get('ipv2_rem'),
                                'ipv3_brand':request.POST.get('ipv3_brand'),'ipv3_date':request.POST.get('ipv3_date'),'ipv3_loc':request.POST.get('ipv3_loc'),'ipv3_rem':request.POST.get('ipv3_rem'),
                                'ipv4_brand':request.POST.get('ipv4_brand'),'ipv4_date':request.POST.get('ipv4_date'),'ipv4_loc':request.POST.get('ipv4_loc'),'ipv4_rem':request.POST.get('ipv4_rem'),
                                'ipv5_brand':request.POST.get('ipv5_brand'),'ipv5_date':request.POST.get('ipv5_date'),'ipv5_loc':request.POST.get('ipv5_loc'),'ipv5_rem':request.POST.get('ipv5_rem'),
                                
                                'japb1_brand':request.POST.get('japb1_brand'),'japb1_date':request.POST.get('japb1_date'),'japb1_loc':request.POST.get('japb1_loc'),'japb1_rem':request.POST.get('japb1_rem'),
                                'japb2_brand':request.POST.get('japb2_brand'),'japb2_date':request.POST.get('japb2_date'),'japb2_loc':request.POST.get('japb2_loc'),'japb2_rem':request.POST.get('japb2_rem'),

                                'msl_brand':request.POST.get('msl_brand'),'msl_date':request.POST.get('msl_date'),'msl_loc':request.POST.get('msl_loc'),'msl_rem':request.POST.get('msl_rem'),
                                
                                'men_brand':request.POST.get('men_brand'),'men_date':request.POST.get('men_date'),'men_loc':request.POST.get('men_loc'),'men_rem':request.POST.get('men_rem'),

                                'mmr1_brand':request.POST.get('mmr1_brand'),'mmr1_date':request.POST.get('mmr1_date'),'mmr1_loc':request.POST.get('mmr1_loc'),'mmr1_rem':request.POST.get('mmr1_rem'),
                                'mmr2_brand':request.POST.get('mmr2_brand'),'mmr2_date':request.POST.get('mmr2_date'),'mmr2_loc':request.POST.get('mmr2_loc'),'mmr2_rem':request.POST.get('mmr2_rem'),
                                
                                'pcv1_brand':request.POST.get('pcv1_brand'),'pcv1_date':request.POST.get('pcv1_date'),'pcv1_loc':request.POST.get('pcv1_loc'),'pcv1_rem':request.POST.get('pcv1_rem'),
                                'pcv2_brand':request.POST.get('pcv2_brand'),'pcv2_date':request.POST.get('pcv2_date'),'pcv2_loc':request.POST.get('pcv2_loc'),'pcv2_rem':request.POST.get('pcv2_rem'),
                                'pcv3_brand':request.POST.get('pcv3_brand'),'pcv3_date':request.POST.get('pcv3_date'),'pcv3_loc':request.POST.get('pcv3_loc'),'pcv3_rem':request.POST.get('pcv3_rem'),
                                'pcv4_brand':request.POST.get('pcv4_brand'),'pcv4_date':request.POST.get('pcv4_date'),'pcv4_loc':request.POST.get('pcv4_loc'),'pcv4_rem':request.POST.get('pcv4_rem'),
                                
                                'rota1_brand':request.POST.get('rota1_brand'),'rota1_date':request.POST.get('rota1_date'),'rota1_loc':request.POST.get('rota1_loc'),'rota1_rem':request.POST.get('rota1_rem'),
                                'rota2_brand':request.POST.get('rota2_brand'),'rota2_date':request.POST.get('rota2_date'),'rota2_loc':request.POST.get('rota2_loc'),'rota2_rem':request.POST.get('rota2_rem'),
                                'rota3_brand':request.POST.get('rota3_brand'),'rota3_date':request.POST.get('rota3_date'),'rota3_loc':request.POST.get('rota3_loc'),'rota3_rem':request.POST.get('rota3_rem'),
                                
                                'td_brand':request.POST.get('td_brand'),'td_date':request.POST.get('td_date'),'td_loc':request.POST.get('td_loc'),'td_rem':request.POST.get('td_rem'),
                                
                                'typ_brand':request.POST.get('typ_brand'),'typ_date':request.POST.get('typ_date'),'typ_loc':request.POST.get('typ_loc'),'typ_rem':request.POST.get('typ_rem'),
                                
                                'var1_brand':request.POST.get('var1_brand'),'var1_date':request.POST.get('var1_date'),'var1_loc':request.POST.get('var1_loc'),'var1_rem':request.POST.get('var1_rem'),
                                'var2_brand':request.POST.get('var2_brand'),'var2_date':request.POST.get('var2_date'),'var2_loc':request.POST.get('var2_loc'),'var2_rem':request.POST.get('var2_rem'),
                            
                                })
        if(form.is_valid()):
            print('is valid')
            form.save()
            print("nagsave")
            messages.success(request, "Vaccine Record updated" )
            return redirect('/search-patient')
        else:
            print(form.errors)
    else:
        messages.error(request, "Something was wrong with the input, please try again and make sure every field is filled correctly.")
    data = {"form":form,}
    return render(request, 'vaccinerecordapp/vaccine-record.html',data)

def update_vaccine(request,pk):
    record = PatientRecord.objects.get(id = pk)
    vac = PatientRecord.objects.get(id = pk).user
    vaccine = Vaccine.objects.get(user=vac)
    form = UpdateVaccineForm(instance = vaccine)

    if(request.method=="POST"):   
        user = User.objects.get(username=vac)
        form = VaccineForm({'user':user, 
                                'bcg_brand':request.POST.get('bcg_brand'),'bcg_date':request.POST.get('bcg_date'),'bcg_loc':request.POST.get('bcg_loc'),'bcg_rem':request.POST.get('bcg_rem'),
                                
                                'hepb1_brand':request.POST.get('hepb1_brand'),'hepb1_date':request.POST.get('hepb1_date'),'hepb1_loc':request.POST.get('hepb1_loc'),'hepb1_rem':request.POST.get('hepb1_rem'),
                                'hepb2_brand':request.POST.get('hepb2_brand'),'hepb2_date':request.POST.get('hepb2_date'),'hepb2_loc':request.POST.get('hepb2_loc'),'hepb2_rem':request.POST.get('hepb2_rem'),
                                'hepb3_brand':request.POST.get('hepb3_brand'),'hepb3_date':request.POST.get('hepb3_date'),'hepb3_loc':request.POST.get('hepb3_loc'),'hepb3_rem':request.POST.get('hepb3_rem'),
                                
                                'dtap1_brand':request.POST.get('dtap1_brand'),'dtap1_date':request.POST.get('dtap1_date'),'dtap1_loc':request.POST.get('dtap1_loc'),'dtap1_rem':request.POST.get('dtap1_rem'),
                                'dtap2_brand':request.POST.get('dtap2_brand'),'dtap2_date':request.POST.get('dtap2_date'),'dtap2_loc':request.POST.get('dtap2_loc'),'dtap2_rem':request.POST.get('dtap2_rem'),
                                'dtap3_brand':request.POST.get('dtap3_brand'),'dtap3_date':request.POST.get('dtap3_date'),'dtap3_loc':request.POST.get('dtap3_loc'),'dtap3_rem':request.POST.get('dtap3_rem'),
                                'dtap4_brand':request.POST.get('dtap4_brand'),'dtap4_date':request.POST.get('dtap4_date'),'dtap4_loc':request.POST.get('dtap4_loc'),'dtap4_rem':request.POST.get('dtap4_rem'),
                                'dtap5_brand':request.POST.get('dtap5_brand'),'dtap5_date':request.POST.get('dtap5_date'),'dtap5_loc':request.POST.get('dtap5_loc'),'dtap5_rem':request.POST.get('dtap5_rem'),

                                'hib1_brand':request.POST.get('hib1_brand'),'hib1_date':request.POST.get('hib1_date'),'hib1_loc':request.POST.get('hib1_loc'),'hib1_rem':request.POST.get('hib1_rem'),
                                'hib2_brand':request.POST.get('hib2_brand'),'hib2_date':request.POST.get('hib2_date'),'hib2_loc':request.POST.get('hib2_loc'),'hib2_rem':request.POST.get('hib2_rem'),
                                'hib3_brand':request.POST.get('hib3_brand'),'hib3_date':request.POST.get('hib3_date'),'hib3_loc':request.POST.get('hib3_loc'),'hib3_rem':request.POST.get('hib3_rem'),
                                'hib4_brand':request.POST.get('hib4_brand'),'hib4_date':request.POST.get('hib4_date'),'hib4_loc':request.POST.get('hib4_loc'),'hib4_rem':request.POST.get('hib4_rem'),

                                'hpv11_brand':request.POST.get('hpv11_brand'),'hpv11_date':request.POST.get('hpv11_date'),'hpv11_loc':request.POST.get('hpv11_loc'),'hpv11_rem':request.POST.get('hpv11_rem'),
                                'hpv12_brand':request.POST.get('hpv12_brand'),'hpv12_date':request.POST.get('hpv12_date'),'hpv12_loc':request.POST.get('hpv12_loc'),'hpv12_rem':request.POST.get('hpv12_rem'),

                                'hpv21_brand':request.POST.get('hpv21_brand'),'hpv21_date':request.POST.get('hpv21_date'),'hpv21_loc':request.POST.get('hpv21_loc'),'hpv21_rem':request.POST.get('hpv21_rem'),
                                'hpv22_brand':request.POST.get('hpv22_brand'),'hpv22_date':request.POST.get('hpv22_date'),'hpv22_loc':request.POST.get('hpv22_loc'),'hpv22_rem':request.POST.get('hpv22_rem'),
                                'hpv23_brand':request.POST.get('hpv23_brand'),'hpv23_date':request.POST.get('hpv23_date'),'hpv23_loc':request.POST.get('hpv23_loc'),'hpv23_rem':request.POST.get('hpv23_rem'),

                                'hepa1_brand':request.POST.get('hepa1_brand'),'hepa1_date':request.POST.get('hepa1_date'),'hepa1_loc':request.POST.get('hepa1_loc'),'hepa1_rem':request.POST.get('hepa1_rem'),
                                'hepa2_brand':request.POST.get('hepa2_brand'),'hepa2_date':request.POST.get('hepa2_date'),'hepa2_loc':request.POST.get('hepa2_loc'),'hepa2_rem':request.POST.get('hepa2_rem'),

                                'inf1_brand':request.POST.get('inf1_brand'),'inf1_date':request.POST.get('inf1_date'),'inf1_loc':request.POST.get('inf1_loc'),'inf1_rem':request.POST.get('inf1_rem'),
                                'inf2_brand':request.POST.get('inf2_brand'),'inf2_date':request.POST.get('inf2_date'),'inf2_loc':request.POST.get('inf2_loc'),'inf2_rem':request.POST.get('inf2_rem'),

                                'anf_brand':request.POST.get('anf_brand'),'anf_date':request.POST.get('anf_date'),'anf_loc':request.POST.get('anf_loc'),'anf_rem':request.POST.get('anf_rem'),

                                'ipv1_brand':request.POST.get('ipv1_brand'),'ipv1_date':request.POST.get('ipv1_date'),'ipv1_loc':request.POST.get('ipv1_loc'),'ipv1_rem':request.POST.get('ipv1_rem'),
                                'ipv2_brand':request.POST.get('ipv2_brand'),'ipv2_date':request.POST.get('ipv2_date'),'ipv2_loc':request.POST.get('ipv2_loc'),'ipv2_rem':request.POST.get('ipv2_rem'),
                                'ipv3_brand':request.POST.get('ipv3_brand'),'ipv3_date':request.POST.get('ipv3_date'),'ipv3_loc':request.POST.get('ipv3_loc'),'ipv3_rem':request.POST.get('ipv3_rem'),
                                'ipv4_brand':request.POST.get('ipv4_brand'),'ipv4_date':request.POST.get('ipv4_date'),'ipv4_loc':request.POST.get('ipv4_loc'),'ipv4_rem':request.POST.get('ipv4_rem'),
                                'ipv5_brand':request.POST.get('ipv5_brand'),'ipv5_date':request.POST.get('ipv5_date'),'ipv5_loc':request.POST.get('ipv5_loc'),'ipv5_rem':request.POST.get('ipv5_rem'),
                                
                                'japb1_brand':request.POST.get('japb1_brand'),'japb1_date':request.POST.get('japb1_date'),'japb1_loc':request.POST.get('japb1_loc'),'japb1_rem':request.POST.get('japb1_rem'),
                                'japb2_brand':request.POST.get('japb2_brand'),'japb2_date':request.POST.get('japb2_date'),'japb2_loc':request.POST.get('japb2_loc'),'japb2_rem':request.POST.get('japb2_rem'),

                                'msl_brand':request.POST.get('msl_brand'),'msl_date':request.POST.get('msl_date'),'msl_loc':request.POST.get('msl_loc'),'msl_rem':request.POST.get('msl_rem'),
                                
                                'men_brand':request.POST.get('men_brand'),'men_date':request.POST.get('men_date'),'men_loc':request.POST.get('men_loc'),'men_rem':request.POST.get('men_rem'),

                                'mmr1_brand':request.POST.get('mmr1_brand'),'mmr1_date':request.POST.get('mmr1_date'),'mmr1_loc':request.POST.get('mmr1_loc'),'mmr1_rem':request.POST.get('mmr1_rem'),
                                'mmr2_brand':request.POST.get('mmr2_brand'),'mmr2_date':request.POST.get('mmr2_date'),'mmr2_loc':request.POST.get('mmr2_loc'),'mmr2_rem':request.POST.get('mmr2_rem'),
                                
                                'pcv1_brand':request.POST.get('pcv1_brand'),'pcv1_date':request.POST.get('pcv1_date'),'pcv1_loc':request.POST.get('pcv1_loc'),'pcv1_rem':request.POST.get('pcv1_rem'),
                                'pcv2_brand':request.POST.get('pcv2_brand'),'pcv2_date':request.POST.get('pcv2_date'),'pcv2_loc':request.POST.get('pcv2_loc'),'pcv2_rem':request.POST.get('pcv2_rem'),
                                'pcv3_brand':request.POST.get('pcv3_brand'),'pcv3_date':request.POST.get('pcv3_date'),'pcv3_loc':request.POST.get('pcv3_loc'),'pcv3_rem':request.POST.get('pcv3_rem'),
                                'pcv4_brand':request.POST.get('pcv4_brand'),'pcv4_date':request.POST.get('pcv4_date'),'pcv4_loc':request.POST.get('pcv4_loc'),'pcv4_rem':request.POST.get('pcv4_rem'),
                                
                                'rota1_brand':request.POST.get('rota1_brand'),'rota1_date':request.POST.get('rota1_date'),'rota1_loc':request.POST.get('rota1_loc'),'rota1_rem':request.POST.get('rota1_rem'),
                                'rota2_brand':request.POST.get('rota2_brand'),'rota2_date':request.POST.get('rota2_date'),'rota2_loc':request.POST.get('rota2_loc'),'rota2_rem':request.POST.get('rota2_rem'),
                                'rota3_brand':request.POST.get('rota3_brand'),'rota3_date':request.POST.get('rota3_date'),'rota3_loc':request.POST.get('rota3_loc'),'rota3_rem':request.POST.get('rota3_rem'),
                                
                                'td_brand':request.POST.get('td_brand'),'td_date':request.POST.get('td_date'),'td_loc':request.POST.get('td_loc'),'td_rem':request.POST.get('td_rem'),
                                
                                'typ_brand':request.POST.get('typ_brand'),'typ_date':request.POST.get('typ_date'),'typ_loc':request.POST.get('typ_loc'),'typ_rem':request.POST.get('typ_rem'),
                                
                                'var1_brand':request.POST.get('var1_brand'),'var1_date':request.POST.get('var1_date'),'var1_loc':request.POST.get('var1_loc'),'var1_rem':request.POST.get('var1_rem'),
                                'var2_brand':request.POST.get('var2_brand'),'var2_date':request.POST.get('var2_date'),'var2_loc':request.POST.get('var2_loc'),'var2_rem':request.POST.get('var2_rem'),
                            
                                }, instance=vaccine)
        if(form.is_valid()):
            form.save()
            record = PatientRecord.objects.get(id = pk)
            data = {"record":record}
            return render(request, "vaccinerecordapp/search-patient.html",data)
    data = {"form":form,"record":record}
    return render(request, "vaccinerecordapp/update-vaccine.html", data) 

@login_required(login_url='/')
def search_patient(request):
    user = User.objects.get(username=request.user.username)
    
    if user.groups.filter(name="Doctor"):
        doc = Doctor.objects.get(user = user)
        notExist = ""
        patients = PatientRecord.objects.filter(doctor_assigned = doc)
        myFilter = RecordFilter(request.GET, queryset=patients)
        patients = myFilter.qs
        if patients.count()==0:
            notExist = "The patient does not exist."
        data = {"patients":patients, 'myFilter':myFilter,'notExist':notExist}
        return render(request, 'vaccinerecordapp/search-patient.html',data)
    else: 
        patients = PatientRecord.objects.all()
        notExist = ""
        myFilter = RecordFilter(request.GET, queryset=patients)
        patients = myFilter.qs
        if patients.count()==0:
            notExist = "The patient does not exist."
        data = {"patients":patients, 'myFilter':myFilter,'notExist':notExist}
        return render(request, 'vaccinerecordapp/search-patient.html',data)

@login_required(login_url='/')
def appointment(request,pk):
    record = PatientRecord.objects.get(id = pk)
    form = AppointmentForm(request.POST)
    user = User.objects.get(username=request.user.username)
    appointments = Appointment.objects.filter(user = record.user)
    count = appointments.count()
    if(request.method == "POST"):
        if user.groups.filter(name='patient').exists():
            form = AppointmentForm({ 'user':record.user, 
            'patient_username': record.user.username,
            'date': request.POST.get('date'),
            'time': request.POST.get('time'),
            'doctor': record.doctor_assigned,
            'visit': request.POST.get('visit'),
            'location': request.POST.get('location'),
            'stat': 'UNCONFIRMED'})
        else:
            form = AppointmentForm({ 'user':record.user, 
            'patient_username': record.user.username,
            'date': request.POST.get('date'),
            'time': request.POST.get('time'),
            'doctor': record.doctor_assigned,
            'visit': request.POST.get('visit'),
            'location': request.POST.get('location'),
            'stat': 'CONFIRMED'})

        if (form.is_valid()):
            form.save()
            if request.user.groups.filter(name="patient"):
                record = PatientRecord.objects.get(user = request.user)
                data = {'record':record}
                return render(request, 'vaccinerecordapp/patient-landing.html', data)
        else:
            if request.user.groups.filter(name="patient"):
                patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
                data = {'patient':patient}
                return render(request, 'vaccinerecordapp/patient-landing.html', data)
        
        appointments = Appointment.objects.filter(user = record.user)
        count = appointments.count()
        data = {'appointments':appointments,'count':count,'record':record,'form':form}
        return render(request, 'vaccinerecordapp/appointment.html',data)
    data = {"form":form, "appointments": appointments, "count": count,"record":record}
    return render(request, 'vaccinerecordapp/appointment.html',data)                          
    
@login_required(login_url='/')
def certificate(request,pk):
    record = PatientRecord.objects.get(id=pk)
    data = {"record":record}
    return render(request, 'vaccinerecordapp/vaccine-certificate.html',data )

@login_required(login_url='/')
def patient_profile(request,pk):
    form = PatientRecordForm(request.POST)
    record = PatientRecord.objects.get(id=pk)
    # username = User.objects.get(id=User.objects.get(id=pk).id)
    # print(username)
    # record = PatientRecord.objects.get(user=PatientRecord.objects.get(user=username).user)
    data = {"form":form, "record":record}
    return render(request, 'vaccinerecordapp/patient-profile.html',data )

@login_required(login_url='/')
def create_patient_record(request):
    form = PatientRecordForm(request.POST)
    data = {"form":form}
    return render(request,'vaccinerecordapp/account-creation/create-patient-record.html',data)


@login_required(login_url='/')
def tool(request): 
    return render(request, 'vaccinerecordapp/tool/tool.html')

@login_required(login_url='/')
def staff(request): 
    form1 = UserForm()
    form2 = DoctorForm()
    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/tool/staff.html',data)

@login_required(login_url='/')
def patient_landing(request):
    current_user = request.user
    if current_user.groups.filter(name = "Patient"):
        patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
    data = {'patient':patient}
    return render(request, 'vaccinerecordapp/patient-landing.html',data)
    

@login_required(login_url='/')
def portal(request): 
    form1 = UserForm(request.POST)
    form2 = PatientForm(request.POST)
    patients = User.objects.filter(groups__name="Patient")
    data = {"form1":form1, "form2":form2, "patients":patients}
    return render(request, 'vaccinerecordapp/portal.html',data)

def passwordReset(request): 
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "vaccinerecordapp/reset-password/password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Vaccine Records',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        message = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, message, EMAIL_HOST_USER , [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect ("done/")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="vaccinerecordapp/reset-password/password-reset.html", context={"password_reset_form":password_reset_form})

@login_required(login_url='/')
def confirm_appointments(request):
    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
    count = appointments.count()
    data = {'appointments':appointments, 'count':count}
    return render(request,'vaccinerecordapp/confirm-appointment.html',data)

@login_required(login_url='/')
def confirm_appointment(request,pk):
    appointment = Appointment.objects.get(id = pk)
    appointment.stat = "CONFIRMED"
    appointment.save()
    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
    count = appointments.count()
    data = {'appointments':appointments, 'count':count}
    return render(request,'vaccinerecordapp/confirm-appointment.html',data)

@login_required(login_url='/')
def reject_appointment(request,pk):
    appointment = Appointment.objects.get(id = pk)
    appointment.delete()
    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
    count = appointments.count()
    data = {'appointments':appointments, 'count':count}
    return render(request,'vaccinerecordapp/confirm-appointment.html',data)

# for generating pdf
from io import BytesIO
from django.template.loader import get_template
import os

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GeneratePDF(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            record = PatientRecord.objects.get(id=pk)
        except:
            return HttpResponse("505 Not Found")
        curr_date = datetime.date.today()
        data = {
            'first_name': record.first_name,
            'middle_name': record.middle_name,
            'last_name': record.last_name,
            'age': record.age,
            'city': record.city,
            'doctor_assigned': record.doctor_assigned,
            'date': curr_date,
        }
        pdf = render_to_pdf('vaccinerecordapp/certificate-pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='/')
def report(request):
    return render(request,'vaccinerecordapp/tool/report.html')

@login_required(login_url='/')
def update_staff(request):
    user = User.objects.get(username=request.user.username)
    
    staffs = Doctor.objects.all
    notExist = ""
    # myFilter = RecordFilter(request.GET, queryset=patients)
    # patients = myFilter.qs
    # if patients.count()==0:
        # notExist = "The patient does not exist."
    data = {"staffs":staffs}  
    return render(request,'vaccinerecordapp/tool/update-staff.html',data)

@login_required(login_url='/')
def reminder(request):
    vaccines = Vaccine.objects.all()
    patients = PatientRecord.objects.all()
    remind = []
    for patient in patients:
        vaccine = Vaccine.objects.get(user = patient.user)
        if(vaccine.bcg_date is None):
            remind.append(patient)
            break
        #dtap1
        if((datetime.date.today()-patient.bday).days > 42):
            remind.append(patient)
            break
        #dtap2
        if(vaccine.dtap1_date is not None):
            if((datetime.date.today()-vaccine.dtap1_date).days > 28): 
                remind.append(patient)
                break
        #dtap3
        if(vaccine.dtap2_date is not None):
            if((datetime.date.today()-vaccine.dtap2_date).days > 28): 
                remind.append(patient)
                break
        #dtap booster 1
        if((datetime.date.today()-patient.bday).days > 350):
            remind.append(patient)
            break
        #dtap booster 2
        if((datetime.date.today()-patient.bday).days > 1400):
            remind.append(patient)
            break
        #hepb1
        if(vaccine.hepb1_date is None):
            remind.append(patient)
            break
        #hepb2
        if((datetime.date.today()-patient.bday).days > 30):
            remind.append(patient)
            break
        #hepb3
        if((datetime.date.today()-patient.bday).days > 180):
            remind.append(patient)
            break
        #hib1
        if((datetime.date.today()-vaccine.hepb3_date).days > 42):
            remind.append(patient)
            break
        #hib2
        if((datetime.date.today()-vaccine.hib1_date).days > 28):
            remind.append(patient)
            break
        #hib3
        if((datetime.date.today()-vaccine.hib2_date).days > 28):
            remind.append(patient)
            break
        #hib booster1
        if((datetime.date.today()-vaccine.hib3_date).days > 180):
            remind.append(patient)
            break
        #hpv11
        # if((datetime.date.today()-patient.bday).days > 180):
        #     remind.append(patient)
        #     break
        # #hpv12
        # if((datetime.date.today()-patient.bday).days > 180):
        #     remind.append(patient)
        #     break
        #hpv21

        #hpv22

        #hpv3

        #inactivehepa1
        if((datetime.date.today()-patient.bday).days > 360):
            remind.append(patient)
            break
        #inactivehepa2
        if((datetime.date.today()-vaccine.hepa1_date).days > 180):
            remind.append(patient)
            break
        #inf1
        if((datetime.date.today()-patient.bday).days > 180):
            remind.append(patient)
            break
        #inf2
        if((datetime.date.today()-vaccine.inf1_date).days > 28):
            remind.append(patient)
            break
        #annual flu
        # if((datetime.date.today()-patient.bday).days > 180):
        #     remind.append(patient)
        #     break
        #ipv/opv1
        if((datetime.date.today()-patient.bday).days > 42):
            remind.append(patient)
            break
        #ipv/opv2
        if((datetime.date.today()-patient.ipv1_date).days > 28):
            remind.append(patient)
            break
        #ipv/opv3
        if((datetime.date.today()-patient.ipv2_date).days > 28):
            remind.append(patient)
            break
        #ipv/opv booster 1
        if((datetime.date.today()-patient.bday).days > 360):
            remind.append(patient)
            break
        #ipv/opv booster 2
        if((datetime.date.today()-patient.bday).days > 1440):
            remind.append(patient)
            break
        #japencb1
        if((datetime.date.today()-patient.bday).days > 270):
            remind.append(patient)
            break
        #japencb2
        if(360 < (datetime.date.today()-vaccine.japb1_date).days <= 720):
            remind.append(patient)
            break
        #msl
            #note: sakop two cases either way ; needs fixing
        if(((datetime.date.today()-patient.bday).days > 180) | 
            ((datetime.date.today()-patient.bday).days > 270)):
            remind.append(patient)
            break
        #meninggo vax

        #mmr1
        if((datetime.date.today()-patient.bday).days > 360):
            remind.append(patient)
            break
        #mmr2
        if((1440 < (datetime.date.today()-patient.bday).days <= 2160) |
            ((datetime.date.today()-vaccine.mmr1_date).days > 28)):
            remind.append(patient)
            break
        #pcv1
        if(1440 < (datetime.date.today()-patient.bday).days > 42):
            remind.append(patient)
            break
        #pcv2
        if((datetime.date.today()-vaccine.pcv1_date).days > 28):
            remind.append(patient)
            break
        #pcv3
        if((datetime.date.today()-vaccine.pcv2_date).days > 28):
            remind.append(patient)
            break
        #pcv booster1
        if((datetime.date.today()-patient.pcv3_date).days > 180):
            remind.append(patient)
            break
        #rota1
        if((datetime.date.today()-patient.bday).days > 42):
            remind.append(patient)
            break
        #rota2
        if((datetime.date.today()-vaccine.rota3_date).days > 28):
            remind.append(patient)
            break
        #rota3
        if((datetime.date.today()-vaccine.rota2_date).days > 28):
            remind.append(patient)
            break
        #td

        #typ

        #var1
        if((datetime.date.today()-patient.bday).days > 360):
            remind.append(patient)
            break
        #var2


    print(remind)
    return render(request, 'vaccinerecordapp/tool/reminder.html')

