from collections import Counter
from datetime import date
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
from dateutil.relativedelta import relativedelta
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
                    appointments = Appointment.objects.filter(doctor = Doctor.objects.get(user_id = request.user.id).id,date=datetime.date.today())
                    count = appointments.count()
                    print(user)
                    data = {"form1":form1, "form2":form2, "patients":patients,"appointments":appointments,"count":count}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
                if user.groups.filter(name="Staff"):
                    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
                    cappointments = Appointment.objects.filter(stat = "CONFIRMED")
                    count = appointments.count()
                    ccount = cappointments.count()
                    data = {"form1":form1, "form2":form2, "patients":patients,"appointments":appointments,"cappointments":cappointments,"count":count,"ccount":ccount}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
                else:
                    data = {"form1":form1, "form2":form2, "patients":patients}
                    return render(request, 'vaccinerecordapp/dashboard.html',data)
            else:
                record = PatientRecord.objects.get(user = request.user)
                age = relativedelta(datetime.date.today(),record.bday)
                days = age.days
                months = age.months
                weeks = age.weeks
                years = age.years
                data = {'record':record,'days':days,'months':months,'years':years, 'weeks':weeks}
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

    if request.user.groups.filter(name="Doctor"):
        appointments = Appointment.objects.filter(doctor = Doctor.objects.get(user_id = request.user.id).id, date = datetime.date.today())
        count = appointments.count()
        data = {'appointments' : appointments,
            'count': count}
        return render(request,'vaccinerecordapp/dashboard.html', data)
    else:
        appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
        cappointments = Appointment.objects.filter(stat = "CONFIRMED")
        count = appointments.count()
        ccount = cappointments.count()
        data = {"appointments":appointments,"cappointments":cappointments,"count":count,"ccount":ccount}
        return render(request, 'vaccinerecordapp/dashboard.html',data)

def create_record(request,username):
    form = PatientRecordForm()
    patients = PatientRecord.objects.all()
    if(request.method == "POST"):  
        user = User.objects.get(username=username)
        form = PatientRecordForm({'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'),
                                        'middle_name':request.POST.get('middle_name'), 'suffix':request.POST.get('suffix'), 'nick_name':request.POST.get('nick_name'),
                                        'doctor_assigned':request.POST.get('doctor_assigned'), 'gender':request.POST.get('gender'), 'bday':request.POST.get('bday'),
                                        'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
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
    data = {"form":form, "patients":patients,"username":username, }
    return render(request, 'vaccinerecordapp/account-creation/create-patient-record.html',data)

def update_patient_profile(request,pk):
    patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
    form = UpdatePatientRecordForm(instance = patient)
    record = PatientRecord.objects.get(id = pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    weeks = age.weeks
    # weeks = (days/7)
    months = age.months
    years = age.years
    if(request.method=="POST"):   
        user = User.objects.get(username=request.user.username)
        form = PatientRecordForm({ 'user':user, 'last_name':request.POST.get('last_name'), 'first_name':request.POST.get('first_name'),
                                        'middle_name':request.POST.get('middle_name'), 'suffix':request.POST.get('suffix'), 'nick_name':request.POST.get('nick_name'),
                                        'doctor_assigned':request.POST.get('doctor_assigned'), 'gender':request.POST.get('gender'), 'bday':request.POST.get('bday'),
                                        'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
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
            age = relativedelta(datetime.date.today(),record.bday)
            days = age.days
            months = age.months
            weeks = age.weeks
            years = age.years
            data = {'record':record,'days':days,'months':months,'years':years,'weeks':weeks, 'age': f"{years} years, {months} months, {weeks} weeks",}
            return render(request, "vaccinerecordapp/patient-landing.html",data)
    
    data = {'record':record,'days':days,'months':months,'years':years,'form':form, 'weeks':weeks, 'age': f"{years} years, {months} months, {weeks} weeks",}
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
                                        'mobile':request.POST.get('mobile'), 'landline':request.POST.get('landline'),
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
            age = relativedelta(datetime.date.today(),record.bday)
            days = age.days
            months = age.months
            weeks = age.weeks
            years = age.years
            data = {'record':record,'days':days,'months':months,'years':years, 'weeks':weeks, 'age': f"{years} years, {months} months, {weeks} weeks",}
            return render(request, "vaccinerecordapp/search-patient.html",data)
    record = PatientRecord.objects.get(id = pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years
    data = {'record':record,'days':days,'months':months,'years':years,'form':form, 'weeks':weeks, 'age': f"{years} years, {months} months, {weeks} weeks",}
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

            appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
            cappointments = Appointment.objects.filter(stat = "CONFIRMED")
            count = appointments.count()
            ccount = cappointments.count()
            data = {"form1":form1, "form2":form2, "appointments":appointments,"cappointments":cappointments,"count":count,"ccount":ccount}
            
            return render(request, 'vaccinerecordapp/dashboard.html',data)
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
        age = relativedelta(datetime.date.today(),record.bday)
        days = age.days
        months = age.months
        weeks = age.weeks
        years = age.years
        data = {"record":record, "vaccine":vaccine, "form":form,'days':days,'months':months,'years':years, 'weeks':weeks}
        return render(request, 'vaccinerecordapp/display-vaccine.html',data)
    else:
        return create_vaccine_record(request,pk)

def create_vaccine_record(request,pk):
    form = VaccineForm(request.POST)
    record = PatientRecord.objects.get(id=pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years
    data = {"record":record, "form":form,'days':days,'months':months,'years':years, 'weeks':weeks}
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
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years

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
            data = {"record":record,'days':days,'months':months,'years':years, 'weeks':weeks}
            return redirect('search-patient')

    data = {"record":record, "form":form,'days':days,'months':months,'years':years, 'weeks':weeks}
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
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years
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
                age = relativedelta(datetime.date.today(),record.bday)
                days = age.days
                months = age.months
                weeks = age.weeks
                years = age.years
                data = {"record":record,'days':days,'months':months,'years':years, 'weeks':weeks}
                return render(request, 'vaccinerecordapp/patient-landing.html', data)
        else:
            if request.user.groups.filter(name="patient"):
                record = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
                age = relativedelta(datetime.date.today(),record.bday)
                days = age.days
                months = age.months
                weeks = age.weeks
                years = age.years
                data = {"record":record,'days':days,'months':months,'years':years, 'weeks':weeks}
                return render(request, 'vaccinerecordapp/patient-landing.html', data)
        
        appointments = Appointment.objects.filter(user = record.user)
        count = appointments.count()
        data = {'appointments':appointments,'count':count,'record':record,'form':form,'days':days,'months':months,'years':years, 'weeks':weeks}
        return render(request, 'vaccinerecordapp/appointment.html',data)
    data = {"form":form, "appointments": appointments, "count": count,"record":record,'days':days,'months':months,'years':years, 'weeks':weeks}
    return render(request, 'vaccinerecordapp/appointment.html',data)                          

@login_required(login_url='/')
def patient_profile(request,pk):
    form = PatientRecordForm(request.POST)
    record = PatientRecord.objects.get(id=pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    weeks = age.weeks
    months = age.months
    years = age.years

    data = {"record":record,'days':days,'months':months,'years':years,'form':form,'weeks':weeks, 'age': f"{years} years, {months} months, {weeks} weeks",}
    # username = User.objects.get(id=User.objects.get(id=pk).id)
    # print(username)
    # record = PatientRecord.objects.get(user=PatientRecord.objects.get(user=username).user)
    return render(request, 'vaccinerecordapp/patient-profile.html',data )

@login_required(login_url='/')
def staff_profile(request,pk):
    form = DoctorForm(request.POST)
    record = Doctor.objects.get(id=pk)
    data = {"record":record,'form':form}
    # username = User.objects.get(id=User.objects.get(id=pk).id)
    # print(username)
    # record = PatientRecord.objects.get(user=PatientRecord.objects.get(user=username).user)
    return render(request, 'vaccinerecordapp/tool/staff-profile.html',data )

@login_required(login_url='/')
def create_patient_record(request):
    form = PatientRecordForm(request.POST)
    data = {"form":form}
    return render(request,'vaccinerecordapp/account-creation/create-patient-record.html',data)


@login_required(login_url='/')
def tool(request): 
    patients = PatientRecord.objects.all()

    from_str = request.GET.get("from")
    to_str = request.GET.get("to")
    print(from_str)
    print(to_str)

    

    bcg_con = 0 
    bcg_not = 0
    bcg_no = 0
    hepb_con = 0
    hepb_not = 0
    hepb_no = 0
    dtap_con = 0
    dtap_not = 0
    dtap_no = 0
    opv_con = 0
    opv_not = 0
    opv_no = 0
    hib_con = 0
    hib_not = 0
    hib_no = 0
    pcv_con = 0
    pcv_not = 0
    pcv_no = 0
    rota_con = 0
    rota_not = 0
    rota_no = 0
    msl_con = 0
    msl_not = 0
    msl_no = 0
    mmr_con = 0
    mmr_not = 0
    mmr_no = 0
    var_con = 0
    var_not = 0
    var_no = 0
    inf_con = 0
    inf_not = 0
    inf_no = 0
    jap_con = 0
    jap_not = 0
    jap_no = 0
    hepaa_con = 0
    hepaa_not = 0
    hepaa_no = 0
    mcc_con = 0
    mcc_not = 0
    mcc_no = 0
    typ_con = 0
    typ_not = 0
    typ_no = 0
    tdap_con = 0
    tdap_not = 0
    tdap_no = 0
    hpv_con = 0
    hpv_not = 0
    hpv_no = 0
    flu_con = 0
    flu_not = 0
    flu_no = 0
    
    for patient in patients:

        age = relativedelta(datetime.date.today(),patient.bday)
        days = age.days
        months = age.months
        years = age.years

        print(patient.user)
        vaccine = Vaccine.objects.get(user = patient.user)
        print("bcg")

        if(vaccine.bcg_date is None):
                print("no appt")
                if(Appointment.objects.filter(user = patient.user).count() == 0):
                    bcg_no += 1
                    print("+noo")  
                else:
                    print("yes appt")
                    appt = Appointment.objects.filter(user=patient.user)
                    print("pumasok filter")
                    print(appt)
                    for app in appt:
                        print("pumasok loop")
                        curr_date = datetime.date.today()
                        print(curr_date)
                        print(app.date)
                        print(app.stat)
                        if ((app.date - curr_date).days > 0):
                                    print("hi")
                                    if (app.stat == "CONFIRMED"):
                                        bcg_con += 1
                                        print("+con")
                                        continue
                                    elif (app.stat == "UNCONFIRMED"):
                                        bcg_not += 1
                                        print("+not")
                                        continue
                                    else:
                                        bcg_no += 1
                                        print("+no")
                                        continue
            #dtap1
        print("dtap1")
        if((datetime.date.today()-patient.bday).days > 42):
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            dtap_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            dtap_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            dtap_no += 1
                                            print("+no")
                                            continue
            #dtap2
        
        if(vaccine.dtap1_date is not None):
            if(vaccine.dtap2_date is None):
                print("dtap2")
                if((datetime.date.today()-vaccine.dtap1_date).days > 28): 
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            dtap_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            dtap_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            dtap_no += 1
                                            print("+no")
                                            continue
            #dtap3
        if(vaccine.dtap2_date is not None):
            if(vaccine.dtap3_date is None):
                print("dtap3")
                if((datetime.date.today()-vaccine.dtap2_date).days > 28): 
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            dtap_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            dtap_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            dtap_no += 1
                                            print("+no")
                                            continue
            #dtap booster 1
        if(vaccine.dtap3_date is not None):
            if(vaccine.dtap4_date is None):
                if((datetime.date.today()-patient.bday).days > 350):
                        print("dtapboost1")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            dtap_no += 1
                            print("+noo")
                            
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
            #dtap booster 2
        if(vaccine.dtap4_date is not None):
            if(vaccine.dtap5_date is None):
                if((datetime.date.today()-patient.bday).days > 1400):
                        print("dtapboost2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            dtap_no += 1
                            print("+noo")
                            
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
                    
            #hepb1
        
        if(vaccine.hepb1_date is None):
                    print("hepb1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hepb_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            hepb_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            hepb_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            hepb_no += 1
                                            print("+no")
                                            continue
            #hepb2
        if(vaccine.hepb1_date is not None):
            if(vaccine.hepb2_date is None):
                if((datetime.date.today()-patient.bday).days > 30):
                        print("hepb2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hepb_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hepb_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hepb_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hepb_no += 1
                                                print("+no")
                                                continue
            #hepb3
        if(vaccine.hepb2_date is not None):
            if(vaccine.hepb3_date is None):
                if((datetime.date.today()-patient.bday).days > 180):
                        print("hepb3")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hepb_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hepb_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hepb_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hepb_no += 1
                                                print("+no")
                                                continue
            #hib1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("hib1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hib_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            hib_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            hib_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            hib_no += 1
                                            print("+no")
                                            continue
                    
            #hib2
        if(vaccine.hib1_date is not None):
            if(vaccine.hib2_date is None):
                if((datetime.date.today()-vaccine.hib1_date).days > 28):
                            print("hib2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hib_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hib_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hib_no += 1
                                                    print("+no")
                                                    continue
                #hib3
        if(vaccine.hib2_date is not None):   
            if(vaccine.hib3_date is None):     
                if((datetime.date.today()-vaccine.hib2_date).days > 28):
                            print("hib3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hib_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hib_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hib_no += 1
                                                    print("+no")
                                                    continue
                #hib booster1
        if(vaccine.hib3_date is not None):
            if(vaccine.hib4_date is None):
                if((datetime.date.today()-vaccine.hib3_date).days > 180):
                            print("hib4")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hib_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hib_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hib_no += 1
                                                    print("+no")
                                                    continue
            #hpv11
        if(8<years<15):
            if(vaccine.hpv11_date is None):
                        print("hpv11")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hpv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hpv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hpv_no += 1
                                                print("+no")
                                                continue
        #hpv12
        if(vaccine.hpv11_date is not None):
            if(vaccine.hpv12_date is None):
                if(9<years<15):
                    if ((datetime.date.today()-vaccine.hpv11_date).days > 180):
                        print("hpv12")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hpv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hpv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hpv_no += 1
                                                print("+no")
                                                continue
        #hpv21
        if(years>=15):
            if(vaccine.hpv11_date is None):
                if(vaccine.hpv21_date is None):
                        print("hpv21")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hpv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hpv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hpv_no += 1
                                                print("+no")
                                                continue
        #hpv22
        if(vaccine.hpv21_date is not None):
            if(vaccine.hpv22_date is None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv21_date).days > 120):
                        print("hpv22")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hpv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hpv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hpv_no += 1
                                                print("+no")
                                                continue
        #hpv3
        if(vaccine.hpv22_date is not None):
            if(vaccine.hpv23_date is None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv22_date).days > 180):
                        print("hpv23")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hpv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hpv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hpv_no += 1
                                                print("+no")
                                                continue
 
            #inactivehepa1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("hepaa1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hepaa_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            hepaa_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            hepaa_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            hepaa_no += 1
                                            print("+no")
                                            continue
            #inactivehepa2
        if(vaccine.hepa1_date is not None):
            if(vaccine.hepa2_date is None):
                if((datetime.date.today()-vaccine.hepa1_date).days > 180):
                            print("hepaa2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hepaa_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hepaa_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hepaa_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hepaa_no += 1
                                                    print("+no")
                                                    continue
            #inf1
        if((datetime.date.today()-patient.bday).days > 180):
                    print("inf1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        inf_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            inf_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            inf_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            inf_no += 1
                                            print("+no")
                                            continue
            #inf2
        if(vaccine.inf1_date is not None):
            if(vaccine.inf2_date is None):
                if((datetime.date.today()-vaccine.inf1_date).days > 28):
                            print("inf2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                inf_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    inf_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    inf_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    inf_no += 1
                                                    print("+no")
                                                    continue
            #annual flu
        if(vaccine.anf_date is None):
                if((datetime.date.today()-patient.bday).days > 360):
                    print("flu")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        flu_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            flu_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            flu_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            flu_no += 1
                                            print("+no")
                                            continue
        if(vaccine.anf_date is not None):        
                if((datetime.date.today()-vaccine.anf_date).days > 360):
                    date = (datetime.date.today()-vaccine.anf_date).days
                    print("flu")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        flu_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            flu_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            flu_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            flu_no += 1
                                            print("+no")
                                            continue
            #ipv/opv1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("opv1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        opv_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            opv_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            opv_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            opv_no += 1
                                            print("+no")
                                            continue
            #ipv/opv2
        if(vaccine.ipv1_date is not None):
            if(vaccine.ipv2_date is None):
                if((datetime.date.today()-patient.ipv1_date).days > 28):
                            print("ipv2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                opv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    opv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    opv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    opv_no += 1
                                                    print("+no")
                                                    continue
                #ipv/opv3
        if(vaccine.ipv2_date is not None):
            if(vaccine.ipv3_date is None):
                if((datetime.date.today()-patient.ipv2_date).days > 28):
                            print("ipbv3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                opv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    opv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    opv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    opv_no += 1
                                                    print("+no")
                                                    continue
            #ipv/opv booster 1
        if(vaccine.ipv3_date is not None):
            if(vaccine.ipv4_date is None):
                if((datetime.date.today()-patient.bday).days > 360):
                        print("ipv boost1")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            opv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                opv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                opv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                opv_no += 1
                                                print("+no")
                                                continue
            #ipv/opv booster 2
        if(vaccine.ipv4_date is not None):
            if(vaccine.ipv5_date is None):
                if((datetime.date.today()-patient.bday).days > 1440):
                        print("hepaa boost 2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            opv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                opv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                opv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                opv_no += 1
                                                print("+no")
                                                continue
            #japencb1
        if((datetime.date.today()-patient.bday).days > 270):
                    print("jap1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        jap_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            jap_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            jap_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            jap_no += 1
                                            print("+no")
                                            continue
            #japencb2
        if(vaccine.japb1_date is not None):
            if(vaccine.japb2_date is None):
                if(360 < (datetime.date.today()-vaccine.japb1_date).days <= 720):
                            print("jap2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                jap_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    jap_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    jap_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    jap_no += 1
                                                    print("+no")
                                                    continue
            #msl
                #note: sakop two cases either way ; needs fixing
        if(((datetime.date.today()-patient.bday).days > 180) | 
                ((datetime.date.today()-patient.bday).days > 270)):
                    print("msl1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        msl_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            msl_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            msl_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            msl_no += 1
                                            print("+no")
                                            continue
            #meninggo vax
        if(1<years<56):
            if(vaccine.men_date is None):
                if(((datetime.date.today()-patient.bday).days > 720) and ((datetime.date.today()-patient.bday).days < 19800)):
                    print("mcc1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        mcc_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            mcc_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            mcc_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            msl_no += 1
                                            print("+no")
                                            continue

            #mmr1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("mmr1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        mmr_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            mmr_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            mmr_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            mmr_no += 1
                                            print("+no")
                                            continue
            #mmr2
        if(vaccine.mmr1_date is not None):
            if(vaccine.mmr2_date is None):
                if((1440 < (datetime.date.today()-patient.bday).days <= 2160) |
                        ((datetime.date.today()-vaccine.mmr1_date).days > 28)):
                            print("mmr2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                mmr_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    mmr_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    mmr_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    mmr_no += 1
                                                    print("+no")
                                                    continue
            #pcv1
        if(1440 < (datetime.date.today()-patient.bday).days > 42):
                    print("pcv1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        pcv_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            pcv_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            pcv_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            pcv_no += 1
                                            print("+no")
                                            continue
            #pcv2
        if(vaccine.pcv1_date is not None):
            if(vaccine.pcv2_date is None):
                if((datetime.date.today()-vaccine.pcv1_date).days > 28):
                            print("pcv2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    pcv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    pcv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    pcv_no += 1
                                                    print("+no")
                                                    continue
                #pcv3
        if(vaccine.pcv2_date is not None):
            if(vaccine.pcv3_date is None):        
                if((datetime.date.today()-vaccine.pcv2_date).days > 28):
                            print("pcv3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    pcv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    pcv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    pcv_no += 1
                                                    print("+no")
                                                    continue
                #pcv booster1
        if(vaccine.pcv3_date is not None):
            if(vaccine.pcv4_date is None):
                if((datetime.date.today()-patient.pcv3_date).days > 180):
                            print("pcvboost")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    pcv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    pcv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    pcv_no += 1
                                                    print("+no")
                                                    continue
            #rota1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("rota1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        rota_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            rota_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            rota_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            rota_no += 1
                                            print("+no")
                                            continue
            #rota2
        if(vaccine.rota1_date is not None):
            if(vaccine.rota2_date is None):
                if((datetime.date.today()-vaccine.rota1_date).days > 28):
                            print("rota2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                rota_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    rota_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    rota_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    rota_no += 1
                                                    print("+no")
                                                    continue
                #rota3
        if(vaccine.rota2_date is not None):      
            if(vaccine.rota3_date is None):  
                if((datetime.date.today()-vaccine.rota2_date).days > 28):
                            print("rota3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                rota_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    rota_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    rota_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    rota_no += 1
                                                    print("+no")
                                                    continue
            #td
        if(3240 < (datetime.date.today()-patient.bday).days <= 5400):
                    print("td")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        tdap_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            tdap_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            tdap_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            tdap_no += 1
                                            print("+no")
                                            continue
            #typ
        if(vaccine.typ_date is None):
                if((datetime.date.today()-patient.bday).days > 720):
                    print("typ1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        typ_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            typ_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            typ_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            typ_no += 1
                                            print("+no")
                                            continue
                                            
        if(vaccine.typ_date is not None):                                    
                if(720 < (datetime.date.today()-vaccine.typ_date).days <= 1080):
                    date = (datetime.date.today()-vaccine.typ_date).days
                    vaccine.typ_date = date
                    print("typ2")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        typ_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            typ_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            typ_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            typ_no += 1
                                            print("+no")
                                            continue
            #var1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("var1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        var_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            var_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            var_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            var_no += 1
                                            print("+no")
                                            continue
            #var2
        if(vaccine.var1_date is not None):
            if(vaccine.var2_date is None):
                if((1440 < (datetime.date.today()-patient.bday).days <= 2160) |    
                        ((datetime.date.today()-vaccine.var1_date).days > 90)):
                            print("var2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                var_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    var_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    var_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    var_no += 1
                                                    print("+no")
                                                    continue
        
    bcg_total = bcg_no + bcg_con + bcg_not
    hepb_total = hepb_no + hepb_con + hepb_not
    dtap_total = dtap_no + dtap_con + dtap_not
    opv_total = opv_no + opv_con + opv_not
    hib_total = hib_no + hib_con + hib_not
    pcv_total = pcv_no + pcv_con + pcv_not
    rota_total = rota_no + rota_con + rota_not
    msl_total = msl_no + msl_con + msl_not
    mmr_total = mmr_no + mmr_con + mmr_not
    var_total = var_no + var_con + var_not
    inf_total = inf_no + inf_con + inf_not
    jap_total = jap_no + jap_con + jap_not
    hepaa_total = hepaa_no + hepaa_con + hepaa_not
    mcc_total = mcc_no + mcc_con + mcc_not
    typ_total = typ_no + typ_con + typ_not
    tdap_total = tdap_no + tdap_con + tdap_not
    hpv_total = hpv_no + hpv_con + hpv_not
    flu_total = flu_no + flu_con + flu_not    

    data = {"bcg_con":bcg_con,"bcg_no":bcg_no, "bcg_not":bcg_not,"bcg_total":bcg_total, 
                "hepb_con":hepb_con,"hepb_no":hepb_no, "hepb_not":hepb_not,"hepb_total":hepb_total,
                "dtap_con":dtap_con,"dtap_no":dtap_no, "dtap_not":dtap_not,"dtap_total":dtap_total,
                "opv_con":opv_con,"opv_no":opv_no, "opv_not":opv_not,"opv_total":opv_total,
                "hib_con":hib_con,"hib_no":hib_no, "hib_not":hib_not,"hib_total":hib_total,
                "pcv_con":pcv_con,"pcv_no":pcv_no, "pcv_not":pcv_not,"pcv_total":pcv_total,
                "rota_con":rota_con,"rota_no":rota_no, "rota_not":rota_not,"rota_total":rota_total,
                "msl_con":msl_con,"msl_no":msl_no, "msl_not":msl_not,"msl_total":msl_total,
                "mmr_con":mmr_con,"mmr_not":mmr_not, "mmr_no":mmr_no,"mmr_total":mmr_total,
                "var_con":var_con,"var_not":var_not, "var_no":var_no,"var_total":var_total,
                "inf_con":inf_con,"inf_no":inf_no, "inf_not":inf_not,"inf_total":inf_total,
                "jap_con":jap_con,"jap_no":jap_no, "jap_not":jap_not,"jap_total":jap_total,
                "hepaa_con":hepaa_con,"hepaa_no":hepaa_no, "hepaa_not":hepaa_not,"hepaa_total":hepaa_total,
                "mcc_con":mcc_con,"mcc_not":mcc_not, "mcc_no":mcc_no,"mcc_total":mcc_total,
                "typ_con":typ_con,"typ_not":typ_not, "typ_no":typ_no,"typ_total":typ_total,
                "tdap_con":tdap_con,"tdap_not":tdap_not, "tdap_no":tdap_no,"tdap_total":tdap_total,
                "hpv_con":hpv_con,"hpv_not":hpv_not, "hpv_no":hpv_no,"hpv_total":hpv_total,
                "flu_con":flu_con,"flu_not":flu_not, "flu_no":flu_no,"flu_total":flu_total}

    return render(request, 'vaccinerecordapp/tool/tool.html', data) 

@login_required(login_url='/')
def staff(request): 
    form1 = UserForm()
    form2 = DoctorForm()
    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/tool/staff.html',data)

@login_required(login_url='/')
def patient_landing(request, pk):
    patients = PatientRecord.objects.all()
    record = PatientRecord.objects.get(id = pk)
    appt = Appointment.objects.get(user=patient.user)
    data = {'patients':patients, "record":record, "appt":appt}
    return render(request, 'vaccinerecordapp/patient-landing.html',data)
    

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
    email = appointment.user.email
    username = appointment.user.username
    subject = "Appointment update: "
    message = "<h1>Hello " + username +", good day!</h1> <br><br>This is to inform you that your request for an appointment has been denied. Please contact your doctor to set a valid time, date, and location for your appointment. Thank you!"
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [email]
    # send_mail(subject, message, from_email, recepient_list)
    email = EmailMessage(
        subject,
        message,
        from_email,
        recepient_list
    )
    email.content_subtype = 'html'
    email.send()
    appointment.delete()
    appointments = Appointment.objects.filter(stat = "UNCONFIRMED")
    count = appointments.count()
    data = {'appointments':appointments, 'count':count}
    return render(request,'vaccinerecordapp/confirm-appointment.html',data)

@login_required(login_url='/')
def reschedule_appointment(request,pk):
    appointment = Appointment.objects.get(id = pk)
    form = AppointmentForm(instance=appointment)
    if(request.method == 'POST'):
        record = PatientRecord.objects.get(user = appointment.user)
        age = relativedelta(datetime.date.today(),record.bday)
        days = age.days
        months = age.months
        weeks = age.weeks
        years = age.years
        form = AppointmentForm({ 'user':record.user, 
            'patient_username': record.user.username,
            'date': request.POST.get('date'),
            'time': request.POST.get('time'),
            'doctor': record.doctor_assigned,
            'visit': request.POST.get('visit'),
            'location': request.POST.get('location'),
            'stat': 'UNCONFIRMED'},instance=appointment)
        if(form.is_valid):
            form.save()
        appointments = Appointment.objects.filter(user = record.user)
        count = appointments.count()
        data = {'appointments':appointments,'count':count,'record':record,'form':form,'days':days,'months':months,'years':years, 'weeks':weeks}
        return render(request, 'vaccinerecordapp/appointment.html',data)
    data = {'form':form, 'pk':pk}
    return render(request,'vaccinerecordapp/reschedule-appointment.html',data)

# certificate tab

@login_required(login_url='/')
def certificate_md(request,pk):
    record = PatientRecord.objects.get(id=pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years
    curr_date = datetime.date.today()
    data = {"record":record,'days':days,'months':months,'years':years, 'date':curr_date, 'weeks':weeks}
    return render(request, 'vaccinerecordapp/vaccine-certificate-md.html',data )

@login_required(login_url='/')
def certificate_pt(request,pk):
    record = PatientRecord.objects.get(id=pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    weeks = age.weeks
    years = age.years
    data = {"record":record,'days':days,'months':months,'years':years, 'weeks':weeks}
    return render(request, 'vaccinerecordapp/vaccine-certificate-pt.html',data )

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

class GeneratePDF_MD(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            record = PatientRecord.objects.get(id=pk)
            patients = PatientRecord.objects.all()
            for patient in patients:
                vaccine = Vaccine.objects.get(user = patient.user)
            username = PatientRecord.objects.get(id=pk).user
            vaccine = Vaccine.objects.get(user = username)
            age = relativedelta(datetime.date.today(),record.bday)
            days = age.days
            months = age.months
            weeks = age.weeks
            years = age.years
        except:
            return HttpResponse("505 Not Found")
        curr_date = datetime.date.today()
        data = {
            'first_name': record.first_name,
            'middle_name': record.middle_name,
            'last_name': record.last_name,
            'age': f"{years} years, {months} months, {weeks} weeks",
            'gender': record.gender,
            'city': record.city,
            'doctor_assigned': record.doctor_assigned,
            'date': curr_date,
            'username': username,
            'patients': patients,
            'patient': patient,
            'vaccine':vaccine,
        }
        pdf = render_to_pdf('vaccinerecordapp/certificate-pdf-pt.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class GeneratePDF_PT(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            record = PatientRecord.objects.get(id=pk)
            patients = PatientRecord.objects.all()
            for patient in patients:
                vaccine = Vaccine.objects.get(user = patient.user)
            username = PatientRecord.objects.get(id=pk).user
            vaccine = Vaccine.objects.get(user = username)
            age = relativedelta(datetime.date.today(),record.bday)
            days = age.days
            months = age.months
            weeks = age.weeks
            years = age.years
        except:
            return HttpResponse("505 Not Found")
        data = {
            'first_name': record.first_name,
            'middle_name': record.middle_name,
            'last_name': record.last_name,
            'age': f"{years} years, {months} months, {weeks} weeks",
            'gender': record.gender,
            'city': record.city,
            'doctor_assigned': record.doctor_assigned,
            'username': username,
            'patients': patients,
            'patient': patient,
            'vaccine':vaccine,
        }
        pdf = render_to_pdf('vaccinerecordapp/certificate-pdf-pt.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='/')
def report(request): 
    patients = PatientRecord.objects.all()

    from_str = request.GET.get("from")
    to_str = request.GET.get("to")
    print(from_str)
    print(to_str)

    from_obj = datetime.datetime.strptime(from_str, '%m/%d/%Y')
    to_obj = datetime.datetime.strptime(to_str, '%m/%d/%Y')
    print(from_obj)
    print(to_obj)

    from_date = from_obj.date()
    to_date = to_obj.date()
    print(from_date)
    print(to_date)

    bcg_con = 0 
    bcg_not = 0
    bcg_no = 0
    hepb_con = 0
    hepb_not = 0
    hepb_no = 0
    dtap_con = 0
    dtap_not = 0
    dtap_no = 0
    opv_con = 0
    opv_not = 0
    opv_no = 0
    hib_con = 0
    hib_not = 0
    hib_no = 0
    pcv_con = 0
    pcv_not = 0
    pcv_no = 0
    rota_con = 0
    rota_not = 0
    rota_no = 0
    msl_con = 0
    msl_not = 0
    msl_no = 0
    mmr_con = 0
    mmr_not = 0
    mmr_no = 0
    var_con = 0
    var_not = 0
    var_no = 0
    inf_con = 0
    inf_not = 0
    inf_no = 0
    jap_con = 0
    jap_not = 0
    jap_no = 0
    hepaa_con = 0
    hepaa_not = 0
    hepaa_no = 0
    mcc_con = 0
    mcc_not = 0
    mcc_no = 0
    typ_con = 0
    typ_not = 0
    typ_no = 0
    tdap_con = 0
    tdap_not = 0
    tdap_no = 0
    hpv_con = 0
    hpv_not = 0
    hpv_no = 0
    flu_con = 0
    flu_not = 0
    flu_no = 0
    
    for patient in patients:

        age = relativedelta(datetime.date.today(),patient.bday)
        days = age.days
        months = age.months
        years = age.years

        print(patient.user)
        vaccine = Vaccine.objects.get(user = patient.user)
        print("bcg")

        if(vaccine.bcg_date is None):
                print("no appt")
                if(Appointment.objects.filter(user = patient.user).count() == 0):
                    bcg_no += 1
                    print("+noo")  
                else:
                    print("yes appt")
                    appt = Appointment.objects.filter(user=patient.user)
                    print("pumasok filter")
                    print(appt)
                    for app in appt:
                        print("pumasok loop")
                        if( from_date <= app.date <= to_date):
                            curr_date = datetime.date.today()
                            print(curr_date)
                            print(app.date)
                            print(app.stat)
                            if ((app.date - curr_date).days > 0):
                                        print("hi")
                                        if (app.stat == "CONFIRMED"):
                                            bcg_con += 1
                                            print("+con")
                                            continue
                                        elif (app.stat == "UNCONFIRMED"):
                                            bcg_not += 1
                                            print("+not")
                                            continue
                                        else:
                                            bcg_no += 1
                                            print("+no")
                                            continue
            #dtap1
        print("dtap1")
        if((datetime.date.today()-patient.bday).days > 42):
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
            #dtap2
        
        if(vaccine.dtap1_date is not None):
            if(vaccine.dtap2_date is None):
                print("dtap2")
                if((datetime.date.today()-vaccine.dtap1_date).days > 28): 
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if(from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
            #dtap3
        if(vaccine.dtap2_date is not None):
            if(vaccine.dtap3_date is None):
                print("dtap3")
                if((datetime.date.today()-vaccine.dtap2_date).days > 28): 
                    print("check vacc")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
            #dtap booster 1
        if(vaccine.dtap3_date is not None):
            if(vaccine.dtap4_date is None):
                if((datetime.date.today()-patient.bday).days > 350):
                    print("dtapboost1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        dtap_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                dtap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                dtap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                dtap_no += 1
                                                print("+no")
                                                continue
            #dtap booster 2
        if(vaccine.dtap4_date is not None):
            if(vaccine.dtap5_date is None):
                if((datetime.date.today()-patient.bday).days > 1400):
                        print("dtapboost2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            dtap_no += 1
                            print("+noo")
                            
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    dtap_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    dtap_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    dtap_no += 1
                                                    print("+no")
                                                    continue
                    
            #hepb1
        
        if(vaccine.hepb1_date is None):
                    print("hepb1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hepb_no += 1
                        print("+noo")
                        
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hepb_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hepb_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hepb_no += 1
                                                print("+no")
                                                continue
            #hepb2
        if(vaccine.hepb1_date is not None):
            if(vaccine.hepb2_date is None):
                if((datetime.date.today()-patient.bday).days > 30):
                        print("hepb2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hepb_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hepb_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hepb_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hepb_no += 1
                                                    print("+no")
                                                    continue
            #hepb3
        if(vaccine.hepb2_date is not None):
            if(vaccine.hepb3_date is None):
                if((datetime.date.today()-patient.bday).days > 180):
                        print("hepb3")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hepb_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hepb_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hepb_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hepb_no += 1
                                                    print("+no")
                                                    continue
            #hib1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("hib1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hib_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hib_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hib_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hib_no += 1
                                                print("+no")
                                                continue
                    
            #hib2
        if(vaccine.hib1_date is not None):
            if(vaccine.hib2_date is None):
                if((datetime.date.today()-vaccine.hib1_date).days > 28):
                            print("hib2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        hib_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        hib_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        hib_no += 1
                                                        print("+no")
                                                        continue
                #hib3
        if(vaccine.hib2_date is not None):
            if(vaccine.hib3_date is None):        
                if((datetime.date.today()-vaccine.hib2_date).days > 28):
                            print("hib3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        hib_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        hib_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        hib_no += 1
                                                        print("+no")
                                                        continue
                #hib booster1
        if(vaccine.hib3_date is not None):
            if(vaccine.hib4_date is None):
                if((datetime.date.today()-vaccine.hib3_date).days > 180):
                            print("hib4")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hib_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        hib_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        hib_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        hib_no += 1
                                                        print("+no")
                                                        continue
            #hpv11
        if(8<years<15):
            if(vaccine.hpv11_date is None):
                        print("hpv11")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hpv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hpv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hpv_no += 1
                                                    print("+no")
                                                    continue
        #hpv12
        if(vaccine.hpv11_date is not None):
            if(vaccine.hpv12_date is None):
                if(9<years<15):
                    if ((datetime.date.today()-vaccine.hpv11_date).days > 180):
                        print("hpv12")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hpv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hpv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hpv_no += 1
                                                    print("+no")
                                                    continue
        #hpv21
        if(years>=15):
            if(vaccine.hpv11_date is None):
                if(vaccine.hpv21_date is None):
                        print("hpv21")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hpv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hpv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hpv_no += 1
                                                    print("+no")
                                                    continue
        #hpv22
        if(vaccine.hpv21_date is not None):
            if(vaccine.hpv22_date is None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv21_date).days > 120):
                        print("hpv22")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hpv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hpv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hpv_no += 1
                                                    print("+no")
                                                    continue
        #hpv3
        if(vaccine.hpv22_date is not None):
            if(vaccine.hpv23_date is None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv22_date).days > 180):
                        print("hpv23")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            hpv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    hpv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    hpv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    hpv_no += 1
                                                    print("+no")
                                                    continue
 
            #inactivehepa1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("hepaa1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        hepaa_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                hepaa_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                hepaa_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                hepaa_no += 1
                                                print("+no")
                                                continue
            #inactivehepa2
        if(vaccine.hepa1_date is not None):
            if(vaccine.hepa2_date is None):
                if((datetime.date.today()-vaccine.hepa1_date).days > 180):
                            print("hepaa2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                hepaa_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        hepaa_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        hepaa_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        hepaa_no += 1
                                                        print("+no")
                                                        continue
            #inf1
        if((datetime.date.today()-patient.bday).days > 180):
                    print("inf1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        inf_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                inf_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                inf_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                inf_no += 1
                                                print("+no")
                                                continue
            #inf2
        if(vaccine.inf1_date is not None):
            if(vaccine.inf2_date is None):
                if((datetime.date.today()-vaccine.inf1_date).days > 28):
                            print("inf2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                inf_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        inf_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        inf_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        inf_no += 1
                                                        print("+no")
                                                        continue
            #annual flu
        if(vaccine.anf_date is None):
                if((datetime.date.today()-patient.bday).days > 360):
                    print("flu")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        flu_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                flu_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                flu_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                flu_no += 1
                                                print("+no")
                                                continue
        if(vaccine.anf_date is not None):        
                if((datetime.date.today()-vaccine.anf_date).days > 360):
                    date = (datetime.date.today()-vaccine.anf_date).days
                    print("flu")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        flu_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                flu_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                flu_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                flu_no += 1
                                                print("+no")
                                                continue
            #ipv/opv1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("opv1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        opv_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                opv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                opv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                opv_no += 1
                                                print("+no")
                                                continue
            #ipv/opv2
        if(vaccine.ipv1_date is not None):
            if(vaccine.ipv2_date is None):
                if((datetime.date.today()-patient.ipv1_date).days > 28):
                            print("ipv2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                opv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        opv_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        opv_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        opv_no += 1
                                                        print("+no")
                                                        continue
                #ipv/opv3
        if(vaccine.ipv2_date is not None):
            if(vaccine.ipv3_date is None):
                if((datetime.date.today()-patient.ipv2_date).days > 28):
                            print("ipbv3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                opv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        opv_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        opv_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        opv_no += 1
                                                        print("+no")
                                                        continue
            #ipv/opv booster 1
        if(vaccine.ipv3_date is not None):
            if(vaccine.ipv4_date is None):
                if((datetime.date.today()-patient.bday).days > 360):
                        print("ipv boost1")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            opv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    opv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    opv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    opv_no += 1
                                                    print("+no")
                                                    continue
            #ipv/opv booster 2
        if(vaccine.ipv4_date is not None):
            if(vaccine.ipv5_date is None):
                if((datetime.date.today()-patient.bday).days > 1440):
                        print("hepaa boost 2")
                        if(Appointment.objects.filter(user = patient.user).count() == 0):
                            print("no appt")
                            opv_no += 1
                            print("+noo")
                        else:
                            print("yes appt")
                            appt = Appointment.objects.filter(user=patient.user)
                            print("pumasok filter")
                            print(appt)
                            for app in appt:
                                print("pumasok loop")
                                if( from_date <= app.date <= to_date):
                                    curr_date = datetime.date.today()
                                    print(curr_date)
                                    print(app.date)
                                    print(app.stat)
                                    if ((app.date - curr_date).days > 0):
                                                print("hi")
                                                if (app.stat == "CONFIRMED"):
                                                    opv_con += 1
                                                    print("+con")
                                                    continue
                                                elif (app.stat == "UNCONFIRMED"):
                                                    opv_not += 1
                                                    print("+not")
                                                    continue
                                                else:
                                                    opv_no += 1
                                                    print("+no")
                                                    continue
            #japencb1
        if((datetime.date.today()-patient.bday).days > 270):
                    print("jap1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        jap_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                jap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                jap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                jap_no += 1
                                                print("+no")
                                                continue
            #japencb2
        if(vaccine.japb1_date is not None):
            if(vaccine.japb2_date is None):
                if(360 < (datetime.date.today()-vaccine.japb1_date).days <= 720):
                            print("jap2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                jap_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        jap_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        jap_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        jap_no += 1
                                                        print("+no")
                                                        continue
            #msl
                #note: sakop two cases either way ; needs fixing
        if(((datetime.date.today()-patient.bday).days > 180) | 
                ((datetime.date.today()-patient.bday).days > 270)):
                    print("msl1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        msl_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                msl_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                msl_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                msl_no += 1
                                                print("+no")
                                                continue
            #meninggo vax
        if(1<years<56):
            if(vaccine.men_date is None):
                 if(((datetime.date.today()-patient.bday).days > 720) and ((datetime.date.today()-patient.bday).days < 19800)):
                    print("mcc1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        mcc_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                mcc_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                mcc_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                msl_no += 1
                                                print("+no")
                                                continue

            #mmr1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("mmr1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        mmr_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                mmr_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                mmr_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                mmr_no += 1
                                                print("+no")
                                                continue
            #mmr2
        if(vaccine.mmr1_date is not None):
            if(vaccine.mmr2_date is None):
                if((1440 < (datetime.date.today()-patient.bday).days <= 2160) |
                        ((datetime.date.today()-vaccine.mmr1_date).days > 28)):
                            print("mmr2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                mmr_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        mmr_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        mmr_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        mmr_no += 1
                                                        print("+no")
                                                        continue
            #pcv1
        if(1440 < (datetime.date.today()-patient.bday).days > 42):
                    print("pcv1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        pcv_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                pcv_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                pcv_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                pcv_no += 1
                                                print("+no")
                                                continue
            #pcv2
        if(vaccine.pcv1_date is not None):
            if(vaccine.pcv2_date is None):
                if((datetime.date.today()-vaccine.pcv1_date).days > 28):
                            print("pcv2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        pcv_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        pcv_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        pcv_no += 1
                                                        print("+no")
                                                        continue
                #pcv3
        if(vaccine.pcv2_date is not None):
            if(vaccine.pcv3_date is None):        
                if((datetime.date.today()-vaccine.pcv2_date).days > 28):
                            print("pcv3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        pcv_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        pcv_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        pcv_no += 1
                                                        print("+no")
                                                        continue
                #pcv booster1
        if(vaccine.pcv3_date is not None):
            if(vaccine.pcv4_date is None):
                if((datetime.date.today()-patient.pcv3_date).days > 180):
                            print("pcvboost")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                pcv_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        pcv_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        pcv_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        pcv_no += 1
                                                        print("+no")
                                                        continue
            #rota1
        if((datetime.date.today()-patient.bday).days > 42):
                    print("rota1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        rota_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                rota_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                rota_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                rota_no += 1
                                                print("+no")
                                                continue
            #rota2
        if(vaccine.rota1_date is not None):
            if(vaccine.rota2_date is None):
                if((datetime.date.today()-vaccine.rota1_date).days > 28):
                            print("rota2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                rota_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        rota_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        rota_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        rota_no += 1
                                                        print("+no")
                                                        continue
                #rota3
        if(vaccine.rota2_date is not None):
            if(vaccine.rota3_date is None):        
                if((datetime.date.today()-vaccine.rota2_date).days > 28):
                            print("rota3")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                rota_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        rota_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        rota_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        rota_no += 1
                                                        print("+no")
                                                        continue
            #td
        if(3240 < (datetime.date.today()-patient.bday).days <= 5400):
                    print("td")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        tdap_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                tdap_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                tdap_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                tdap_no += 1
                                                print("+no")
                                                continue
            #typ
        if(vaccine.typ_date is None):
                if((datetime.date.today()-patient.bday).days > 720):
                    print("typ1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        typ_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                typ_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                typ_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                typ_no += 1
                                                print("+no")
                                                continue
                                            
        if(vaccine.typ_date is not None):                                    
                if(720 < (datetime.date.today()-vaccine.typ_date).days <= 1080):
                    date = (datetime.date.today()-vaccine.typ_date).days
                    vaccine.typ_date = date
                    print("typ2")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        typ_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                typ_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                typ_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                typ_no += 1
                                                print("+no")
                                                continue
            #var1
        if((datetime.date.today()-patient.bday).days > 360):
                    print("var1")
                    if(Appointment.objects.filter(user = patient.user).count() == 0):
                        print("no appt")
                        var_no += 1
                        print("+noo")
                    else:
                        print("yes appt")
                        appt = Appointment.objects.filter(user=patient.user)
                        print("pumasok filter")
                        print(appt)
                        for app in appt:
                            print("pumasok loop")
                            if( from_date <= app.date <= to_date):
                                curr_date = datetime.date.today()
                                print(curr_date)
                                print(app.date)
                                print(app.stat)
                                if ((app.date - curr_date).days > 0):
                                            print("hi")
                                            if (app.stat == "CONFIRMED"):
                                                var_con += 1
                                                print("+con")
                                                continue
                                            elif (app.stat == "UNCONFIRMED"):
                                                var_not += 1
                                                print("+not")
                                                continue
                                            else:
                                                var_no += 1
                                                print("+no")
                                                continue
            #var2
        if(vaccine.var1_date is not None):
            if(vaccine.var2_date is None):
                if((1440 < (datetime.date.today()-patient.bday).days <= 2160) |    
                        ((datetime.date.today()-vaccine.var1_date).days > 90)):
                            print("var2")
                            if(Appointment.objects.filter(user = patient.user).count() == 0):
                                print("no appt")
                                var_no += 1
                                print("+noo")
                            else:
                                print("yes appt")
                                appt = Appointment.objects.filter(user=patient.user)
                                print("pumasok filter")
                                print(appt)
                                for app in appt:
                                    print("pumasok loop")
                                    if( from_date <= app.date <= to_date):
                                        curr_date = datetime.date.today()
                                        print(curr_date)
                                        print(app.date)
                                        print(app.stat)
                                        if ((app.date - curr_date).days > 0):
                                                    print("hi")
                                                    if (app.stat == "CONFIRMED"):
                                                        var_con += 1
                                                        print("+con")
                                                        continue
                                                    elif (app.stat == "UNCONFIRMED"):
                                                        var_not += 1
                                                        print("+not")
                                                        continue
                                                    else:
                                                        var_no += 1
                                                        print("+no")
                                                        continue
        
    bcg_total = bcg_no + bcg_con + bcg_not
    hepb_total = hepb_no + hepb_con + hepb_not
    dtap_total = dtap_no + dtap_con + dtap_not
    opv_total = opv_no + opv_con + opv_not
    hib_total = hib_no + hib_con + hib_not
    pcv_total = pcv_no + pcv_con + pcv_not
    rota_total = rota_no + rota_con + rota_not
    msl_total = msl_no + msl_con + msl_not
    mmr_total = mmr_no + mmr_con + mmr_not
    var_total = var_no + var_con + var_not
    inf_total = inf_no + inf_con + inf_not
    jap_total = jap_no + jap_con + jap_not
    hepaa_total = hepaa_no + hepaa_con + hepaa_not
    mcc_total = mcc_no + mcc_con + mcc_not
    typ_total = typ_no + typ_con + typ_not
    tdap_total = tdap_no + tdap_con + tdap_not
    hpv_total = hpv_no + hpv_con + hpv_not
    flu_total = flu_no + flu_con + flu_not    

    data = {"bcg_con":bcg_con,"bcg_no":bcg_no, "bcg_not":bcg_not,"bcg_total":bcg_total, 
                "hepb_con":hepb_con,"hepb_no":hepb_no, "hepb_not":hepb_not,"hepb_total":hepb_total,
                "dtap_con":dtap_con,"dtap_no":dtap_no, "dtap_not":dtap_not,"dtap_total":dtap_total,
                "opv_con":opv_con,"opv_no":opv_no, "opv_not":opv_not,"opv_total":opv_total,
                "hib_con":hib_con,"hib_no":hib_no, "hib_not":hib_not,"hib_total":hib_total,
                "pcv_con":pcv_con,"pcv_no":pcv_no, "pcv_not":pcv_not,"pcv_total":pcv_total,
                "rota_con":rota_con,"rota_no":rota_no, "rota_not":rota_not,"rota_total":rota_total,
                "msl_con":msl_con,"msl_no":msl_no, "msl_not":msl_not,"msl_total":msl_total,
                "mmr_con":mmr_con,"mmr_not":mmr_not, "mmr_no":mmr_no,"mmr_total":mmr_total,
                "var_con":var_con,"var_not":var_not, "var_no":var_no,"var_total":var_total,
                "inf_con":inf_con,"inf_no":inf_no, "inf_not":inf_not,"inf_total":inf_total,
                "jap_con":jap_con,"jap_no":jap_no, "jap_not":jap_not,"jap_total":jap_total,
                "hepaa_con":hepaa_con,"hepaa_no":hepaa_no, "hepaa_not":hepaa_not,"hepaa_total":hepaa_total,
                "mcc_con":mcc_con,"mcc_not":mcc_not, "mcc_no":mcc_no,"mcc_total":mcc_total,
                "typ_con":typ_con,"typ_not":typ_not, "typ_no":typ_no,"typ_total":typ_total,
                "tdap_con":tdap_con,"tdap_not":tdap_not, "tdap_no":tdap_no,"tdap_total":tdap_total,
                "hpv_con":hpv_con,"hpv_not":hpv_not, "hpv_no":hpv_no,"hpv_total":hpv_total,
                "flu_con":flu_con,"flu_not":flu_not, "flu_no":flu_no,"flu_total":flu_total}
 

    return render(request,'vaccinerecordapp/tool/report.html',data)

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
def update_staff_profile(request,pk):
    doctor = Doctor.objects.get(id=pk).user
    profile = Doctor.objects.get(user=doctor)
    form = UpdateDoctorForm(instance = profile)
    record = Doctor.objects.get(id=pk)
    # print(profile.prefix)
    if(request.method=="POST"):   
        user = User.objects.get(username=doctor)
        form = DoctorForm({ 'user':user, 'first_name':request.POST.get('first_name'), 'last_name':request.POST.get('last_name'),
                            'prefix':request.POST.get('prefix'), 'type':request.POST.get('type'), 'title':request.POST.get('title'),
                            'end_date':request.POST.get('end_date'),'contact':request.POST.get('contact')}, instance = profile)
    print(form.errors)
    if(form.is_valid()):
            form.save()
            print("valid")
            profile = Doctor.objects.get(user=doctor)
            data = {"record":record,'form':form}
            return redirect('update-staff')
    data = {"record":record,'form':form}
    return render(request, "vaccinerecordapp/tool/update-staff-profile.html",data)

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
            age = relativedelta(datetime.date.today(),record.bday)
            days = age.days
            months = age.months
            years = age.years
            data = {'record':record,'days':days,'months':months,'years':years}
            return redirect('search-patient')
    record = PatientRecord.objects.get(id = pk)
    age = relativedelta(datetime.date.today(),record.bday)
    days = age.days
    months = age.months
    years = age.years
    data = {'record':record,'days':days,'months':months,'years':years,'form':form}
    return render(request, "vaccinerecordapp/update-profile.html", data)


@login_required(login_url='/')
def reminder(request):
    patients = PatientRecord.objects.all()
    remind = []
    for patient in patients: 
        age = relativedelta(datetime.date.today(),patient.bday)
        years = age.years
        vaccine = Vaccine.objects.get(user = patient.user)
        if(vaccine.bcg_date is None):
            remind.append(patient)
            continue
        #dtap1
        if(vaccine.dtap1_date is None):
            if((datetime.date.today()-patient.bday).days > 42):
                remind.append(patient)
                continue
        #dtap2
        if(vaccine.dtap2_date is None):
            if(vaccine.dtap1_date is not None):
                if((datetime.date.today()-vaccine.dtap1_date).days > 28): 
                    remind.append(patient)
                    continue
        #dtap3
        if(vaccine.dtap3_date is None):
            if(vaccine.dtap2_date is not None):
                if((datetime.date.today()-vaccine.dtap2_date).days > 28): 
                    remind.append(patient)
                    continue
        #dtap booster 1
        if(vaccine.dtap4_date is None):
            if((datetime.date.today()-patient.bday).days > 350):
                remind.append(patient)
                continue
        #dtap booster 2
        if(vaccine.dtap5_date is None):
            if((datetime.date.today()-patient.bday).days > 1400):
                remind.append(patient)
                continue
        #hepb1
        if(vaccine.hepb1_date is None):
            remind.append(patient)
            continue
        #hepb2
        if(vaccine.hepb2_date is None):
            if((datetime.date.today()-patient.bday).days > 30):
                remind.append(patient)
                continue
        #hepb3
        if(vaccine.hepb3_date is None):
            if((datetime.date.today()-patient.bday).days > 180):
                remind.append(patient)
                continue
        #hib1
        if(vaccine.hib1_date is None):
            if(vaccine.hepb3_date is not None):
                if((datetime.date.today()-vaccine.hepb3_date).days > 42):
                    remind.append(patient)
                    continue
        #hib2
        if(vaccine.hib2_date is None):
            if(vaccine.hib1_date is not None):
                if((datetime.date.today()-vaccine.hib1_date).days > 28):
                    remind.append(patient)
                    continue
        #hib3
        if(vaccine.hib3_date is None):
            if(vaccine.hib2_date is not None):
                if((datetime.date.today()-vaccine.hib2_date).days > 28):
                    remind.append(patient)
                    continue
        #hib booster1
        if(vaccine.hib4_date is None):
            if(vaccine.hib3_date is not None):
                if((datetime.date.today()-vaccine.hib3_date).days > 180):
                    remind.append(patient)
                    continue
        #hpv11
        if(vaccine.hpv11_date is None):
            if (vaccine.hpv11_date is None):
                remind.append(patient)
                continue
        #hpv12
        if(vaccine.hpv12_date is None):
            if(vaccine.hpv11_date is not None):
                if(9<years<15):
                    if ((datetime.date.today()-vaccine.hpv11_date).days > 180):
                        remind.append(patient)
                        continue
        #hpv21
        if(vaccine.hpv21_date is None):
            if (vaccine.hpv21_date is None):
                remind.append(patient)
                continue
        #hpv22
        if(vaccine.hpv22_date is None): 
            if(vaccine.hpv21_date is not None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv21_date).days > 120):
                        remind.append(patient)
                        continue
        #hpv3
        if(vaccine.hpv3_date is None):
            if(vaccine.hpv22_date is not None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv22_date).days > 180):
                        remind.append(patient)
                        continue
        #inactivehepa1
        if(vaccine.hepa1_date is None):
            if((datetime.date.today()-patient.bday).days > 360):
                remind.append(patient)
                continue
        #inactivehepa2
        if(vaccine.hepa2_date is None):
            if(vaccine.hepa1_date is not None):
                if((datetime.date.today()-vaccine.hepa1_date).days > 180):
                    remind.append(patient)
                    continue
        #inf1
        if(vaccine.inf1_date is None):
            if((datetime.date.today()-patient.bday).days > 180):
                remind.append(patient)
                continue
        #inf2
        if(vaccine.inf2_date is None):
            if(vaccine.inf1_date is not None):
                if((datetime.date.today()-vaccine.inf1_date).days > 28):
                    remind.append(patient)
                    continue
        #annual flu
        if(vaccine.anf_date is None):
            remind.append(patient)
            continue
        else:
            if((datetime.date.today()-vaccine.anf_date).days > 360):
                remind.append(patient)
                continue
        #ipv/opv1
        if(vaccine.ipv1_date is None):
            if((datetime.date.today()-patient.bday).days > 42):
                remind.append(patient)
                continue
        #ipv/opv2
        if(vaccine.ipv2_date is None):
            if(vaccine.ipv1_date is not None):
                if((datetime.date.today()-vaccine.ipv1_date).days > 28):
                    remind.append(patient)
                    continue
        #ipv/opv3
        if(vaccine.ipv3_date is None):
            if(vaccine.ipv2_date is not None):
                if((datetime.date.today()-vaccine.ipv2_date).days > 28):
                    remind.append(patient)
                    continue
        #ipv/opv booster 1
        if(vaccine.ipv4_date is None):
            if((datetime.date.today()-patient.bday).days > 360):
                remind.append(patient)
                continue
        #ipv/opv booster 2
        if(vaccine.ipv5_date is None):
            if((datetime.date.today()-patient.bday).days > 1440):
                remind.append(patient)
                continue
        #japencb1
        if(vaccine.japb1_date is None):
            if((datetime.date.today()-patient.bday).days > 270):
                remind.append(patient)
                continue
        #japencb2
        if(vaccine.japb2_date is None):
            if(vaccine.japb1_date is not None):
                if(360 < (datetime.date.today()-vaccine.japb1_date).days <= 720):
                    remind.append(patient)
                    continue
        #msl
        if(vaccine.msl_date is None):
            if((datetime.date.today()-patient.bday).days > 180):
                remind.append(patient)
                continue
        #meninggo
        #2 to 55 years old, single dose
        #men
        if(vaccine.men_date is None):
            if(720< (datetime.date.today()-patient.bday).days < 19800):
                remind.append(patient)
                continue
        #mmr1
        if(vaccine.mmr1_date is None):
            if((datetime.date.today()-patient.bday).days > 360):
                remind.append(patient)
                continue
        #mmr2
        if(vaccine.mmr2_date is None):
            if(vaccine.mmr1_date is not None):
                if(((datetime.date.today()-patient.bday).days > 1440) |
                        ((datetime.date.today()-vaccine.mmr1_date).days > 28)):
                        remind.append(patient)
                        continue
        #pcv1
        if(vaccine.pcv1_date is None):
            if((datetime.date.today()-patient.bday).days > 42):
                remind.append(patient)
                continue
        #pcv2
        if(vaccine.pcv2_date is None):
            if(vaccine.pcv1_date is not None):
                if((datetime.date.today()-vaccine.pcv1_date).days > 28):
                    remind.append(patient)
                    continue
        #pcv3
        if(vaccine.pcv3_date is None):
            if(vaccine.pcv2_date is not None):
                if((datetime.date.today()-vaccine.pcv2_date).days > 28):
                    remind.append(patient)
                    continue
        #pcv booster1
        if(vaccine.pcv4_date is None):
            if(vaccine.pcv3_date is not None):
                if((datetime.date.today()-vaccine.pcv3_date).days > 180):
                    remind.append(patient)
                    continue
        #rota1
        if(vaccine.rota1_date is None):
            if((datetime.date.today()-patient.bday).days > 42):
                remind.append(patient)
                continue
        #rota2
        if(vaccine.rota2_date is None):
            if(vaccine.rota1_date is not None):
                if((datetime.date.today()-vaccine.rota1_date).days > 28):
                    remind.append(patient)
                    continue
        #rota3
        if(vaccine.rota3_date is None):
            if(vaccine.rota2_date is not None):
                if((datetime.date.today()-vaccine.rota2_date).days > 28):
                    remind.append(patient)
                    continue
        #td
        if(vaccine.td_date is None):
            if(3240 < (datetime.date.today()-patient.bday).days <= 5400):
                remind.append(patient)
                continue
        #typ
        if(vaccine.typ_date is None):
            if((datetime.date.today()-patient.bday).days > 720):
                remind.append(patient)
                continue
        else:
            if(720 < (datetime.date.today()-vaccine.typ_date).days <= 1080):
                remind.append(patient)
                continue

        #var1
        if(vaccine.var1_date is None):
            if((datetime.date.today()-patient.bday).days > 360):
                remind.append(patient)
                continue
        #var2
        if(vaccine.var2_date is None):
            if(vaccine.var1_date is not None):
                if(((datetime.date.today()-patient.bday).days > 1440 ) |
                ((datetime.date.today()-vaccine.var1_date).days > 90)):
                    remind.append(patient)
                    continue

    q=[]
    user = User.objects.get(username=request.user.username)
    if user.groups.filter(name="Doctor"):
        doc = Doctor.objects.get(user = user)
        due_vax_result = PatientRecord.objects.filter(doctor_assigned = doc)
        notExist = ""

    else:
        due_vax_result =  PatientRecord.objects.none()
        notExist = ""

    for patient in patients:
        #for due vaccine part
        q = []
        if request.method == 'POST':
            date = request.POST.get('date')
            date = datetime.date.fromisoformat(date)
            # age = date - patient.bday
            vaccine = Vaccine.objects.get(user = patient.user)
            # print(age)
            # print(patient.bday)
            if(vaccine.bcg_date is None):
                q.append("bcg")
            #dtap1
            if(vaccine.dtap1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("dtap #1")
            #dtap2
            if(vaccine.dtap2_date is None):
                if(vaccine.dtap1_date is not None):
                    if((date-vaccine.dtap1_date).days > 28): 
                        q.append("dtap #2")
                        #dtap3
            if(vaccine.dtap3_date is None):
                if(vaccine.dtap2_date is not None):
                    if((date-vaccine.dtap2_date).days > 28): 
                        q.append("dtap #3")
            #dtap booster 1
            if(vaccine.dtap4_date is None):
                if((date-patient.bday).days > 350):
                    q.append("dtap booster #1")
            #dtap booster 2
            if(vaccine.dtap5_date is None):
                if((date-patient.bday).days > 1400):
                    q.append("dtap booster #2")
            #hepb1
            if(vaccine.hepb1_date is None):
                q.append("hepb #1")
            #hepb2
            if(vaccine.hepb2_date is None):
                if((date-patient.bday).days > 30):
                    q.append("hepb #2")
            #hepb3
            if(vaccine.hepb3_date is None):
                if((date-patient.bday).days > 180):
                    q.append("hepb #3")
            #hib1
            if(vaccine.hib1_date is None):
                if(vaccine.hepb3_date is not None):
                    if((date-vaccine.hepb3_date).days > 42):
                        q.append("hib #1")
            #hib2
            if(vaccine.hib2_date is None):
                if(vaccine.hib1_date is not None):
                    if((date-vaccine.hib1_date).days > 28):
                        q.append("hib #2")
            #hib3
            if(vaccine.hib3_date is None):
                if(vaccine.hib2_date is not None):
                    if((date-vaccine.hib2_date).days > 28):
                        q.append("hib #3")
            #hib booster1
            if(vaccine.hib4_date is None):
                if(vaccine.hib3_date is not None):
                    if((date-vaccine.hib3_date).days > 180):
                        q.append("hib booster #1")
            #hpv11
            if (vaccine.hpv11_date is None):
                q.append("hpv #1 of 1")
            #hpv12
            if(vaccine.hpv12_date is None):
                if(vaccine.hpv11_date is not None):
                    if(9<years<15):
                        if ((date-vaccine.hpv11_date).days > 180):
                            q.append("hpv #1 of 2")
            #hpv21
            if(vaccine.hpv21_date is None):
                if (vaccine.hpv21_date is None):
                    q.append("hpv #2 of 1")
            #hpv22
            if(vaccine.hpv22_date is None):
                if(vaccine.hpv21_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv21_date).days > 120):
                            q.append("hpv #2 of 2")
            #hpv23
            if(vaccine.hpv23_date is None):
                if(vaccine.hpv22_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv22_date).days > 180):
                            q.append("hpv #3 of 2")
            #inactivehepa1
            if(vaccine.hepa1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("inactive hepa #1")
            #inactivehepa2
            if(vaccine.hepa2_date is None):
                if(vaccine.hepa1_date is not None):
                    if((date-vaccine.hepa1_date).days > 180):
                        q.append("inactive hepa #2")
            #inf1
            if(vaccine.inf1_date is None):
                if((date-patient.bday).days > 180):
                    q.append("inf #1")
            #inf2
            if(vaccine.inf2_date is None):
                if(vaccine.inf1_date is not None):
                    if((date-vaccine.inf1_date).days > 28):
                        q.append("inf #2")
            #annual flu
            if(vaccine.anf_date is None):
                q.append("annual flu")
            else:
                if((date-vaccine.anf_date).days > 360):
                    q.append("annual flu")
            #ipv/opv1
            if(vaccine.ipv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("ipv/opv #1")
            #ipv/opv2
            if(vaccine.ipv2_date is None):
                if(vaccine.ipv1_date is not None):
                    if((date-vaccine.ipv1_date).days > 28):
                        q.append("ipv/opv #2")
            #ipv/opv3
            if(vaccine.ipv3_date is None):
                if(vaccine.ipv2_date is not None):
                    if((date-vaccine.ipv2_date).days > 28):
                        q.append("ipv/opv #3")
            #ipv/opv booster 1
            if(vaccine.ipv4_date is None):
                if((date-patient.bday).days > 360):
                    q.append("ipv/opv booster #1")
            #ipv/opv booster 2
            if(vaccine.ipv5_date is None):
                if((date-patient.bday).days > 1440):
                    q.append("ipv/opv booster #2")
            #japencb1
            if(vaccine.japb1_date is None):
                if((date-patient.bday).days > 270):
                    q.append("jap enc b #1")
            #japencb2
            if(vaccine.japb2_date is None):
                if(vaccine.japb1_date is not None):
                    if(360 < (date-vaccine.japb1_date).days <= 720):
                        q.append("jap enc b #2")
            #msl
            if(vaccine.msl_date is None):
                if((date-patient.bday).days > 180):
                    q.append("measles")
            #men
            if(vaccine.men_date is None):
                    if(720< (date-patient.bday).days < 19800):
                        q.append("meninggo")
            #mmr1
            if(vaccine.mmr1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("mmr #1")
            #mmr2
            if(vaccine.mmr2_date is None):
                if(vaccine.mmr1_date is not None):
                    if(((date-patient.bday).days > 1440) |
                            ((date-vaccine.mmr1_date).days > 28)):
                            q.append("mmr #2")
            #pcv1
            if(vaccine.pcv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("pcv #1")
            #pcv2
            if(vaccine.pcv2_date is None):
                if(vaccine.pcv1_date is not None):
                    if((date-vaccine.pcv1_date).days > 28):
                        q.append("pcv #2")
            #pcv3
            if(vaccine.pcv3_date is None):
                if(vaccine.pcv2_date is not None):
                    if((date-vaccine.pcv2_date).days > 28):
                        q.append("pcv #3")
            #pcv booster1
            if(vaccine.pcv4_date is None):
                if(vaccine.pcv3_date is not None):
                    if((date-vaccine.pcv3_date).days > 180):
                        q.append("pcv booster #1")
            #rota1
            if(vaccine.rota1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("rota #1")
            #rota2
            if(vaccine.rota2_date is None):
                if(vaccine.rota1_date is not None):
                    if((date-vaccine.rota1_date).days > 28):
                        q.append("rota #2")
            #rota3
            if(vaccine.rota3_date is None):
                if(vaccine.rota2_date is not None):
                    if((date-vaccine.rota2_date).days > 28):
                        q.append("rota #3")
            #td
            if(vaccine.td_date is None):
                if(3240 < (date-patient.bday).days <= 5400):
                    q.append("td")
            #typ
            if(vaccine.typ_date is None):
                if((date-patient.bday).days > 720):
                    q.append("typ")
            else:
                if(720 < (date-vaccine.typ_date).days <= 1080):
                    q.append("typ")
            #var1
            if(vaccine.var1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("var #1")
            #var2
            if(vaccine.var2_date is None):
                if(vaccine.var1_date is not None):
                    if(((date-patient.bday).days > 1440 ) |
                    ((date-vaccine.var1_date).days > 90)):
                        q.append("var #2")

            #query filter
            if (len(q) == 0):
                due_vax_result = due_vax_result.exclude(user=patient.user)
        
        # print(q)
    myFilter = RecordFilter(request.GET, queryset=due_vax_result)
    due_vax_result = myFilter.qs

    data = {'patients':due_vax_result, 'myFilter':myFilter,'notExist':notExist}
    return render(request, 'vaccinerecordapp/tool/reminder.html',data)

def reminder_vaccines(request,pk):
    record = PatientRecord.objects.get(id = pk)
    age = relativedelta(datetime.date.today(),record.bday)
    years = age.years
    vaccine = Vaccine.objects.get(user = record.user)
    remind = []

    patients = PatientRecord.objects.all()
    user = User.objects.get(username=request.user.username)
    if user.groups.filter(name="Doctor"):
        doc = Doctor.objects.get(user = user)
        due_vax_result = PatientRecord.objects.filter(doctor_assigned = doc)
        notExist = ""
    
    for patient in patients:
        q = []
        if (request.method != 'POST'):
            date = datetime.date.today()
            vaccine = Vaccine.objects.get(user = patient.user)
            if(vaccine.bcg_date is None):
                q.append("bcg")
            #dtap1
            if(vaccine.dtap1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("dtap #1")
            #dtap2
            if(vaccine.dtap2_date is None):
                if(vaccine.dtap1_date is not None):
                    if((date-vaccine.dtap1_date).days > 28): 
                        q.append("dtap #2")
                        #dtap3
            if(vaccine.dtap3_date is None):
                if(vaccine.dtap2_date is not None):
                    if((date-vaccine.dtap2_date).days > 28): 
                        q.append("dtap #3")
            #dtap booster 1
            if(vaccine.dtap4_date is None):
                if((date-patient.bday).days > 350):
                    q.append("dtap booster #1")
            #dtap booster 2
            if(vaccine.dtap5_date is None):
                if((date-patient.bday).days > 1400):
                    q.append("dtap booster #2")
            #hepb1
            if(vaccine.hepb1_date is None):
                q.append("hepb #1")
            #hepb2
            if(vaccine.hepb2_date is None):
                if((date-patient.bday).days > 30):
                    q.append("hepb #2")
            #hepb3
            if(vaccine.hepb3_date is None):
                if((date-patient.bday).days > 180):
                    q.append("hepb #3")
            #hib1
            if(vaccine.hib1_date is None):
                if(vaccine.hepb3_date is not None):
                    if((date-vaccine.hepb3_date).days > 42):
                        q.append("hib #1")
            #hib2
            if(vaccine.hib2_date is None):
                if(vaccine.hib1_date is not None):
                    if((date-vaccine.hib1_date).days > 28):
                        q.append("hib #2")
            #hib3
            if(vaccine.hib3_date is None):
                if(vaccine.hib2_date is not None):
                    if((date-vaccine.hib2_date).days > 28):
                        q.append("hib #3")
            #hib booster1
            if(vaccine.hib4_date is None):
                if(vaccine.hib3_date is not None):
                    if((date-vaccine.hib3_date).days > 180):
                        q.append("hib booster #1")
            #hpv11
            if (vaccine.hpv11_date is None):
                q.append("hpv #1 of 1")
            #hpv12
            if(vaccine.hpv12_date is None):
                if(vaccine.hpv11_date is not None):
                    if(9<years<15):
                        if ((date-vaccine.hpv11_date).days > 180):
                            q.append("hpv #1 of 2")
            #hpv21
            if(vaccine.hpv21_date is None):
                if (vaccine.hpv21_date is None):
                    q.append("hpv #2 of 1")
            #hpv22
            if(vaccine.hpv22_date is None):
                if(vaccine.hpv21_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv21_date).days > 120):
                            q.append("hpv #2 of 2")
            #hpv23
            if(vaccine.hpv23_date is None):
                if(vaccine.hpv22_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv22_date).days > 180):
                            q.append("hpv #3 of 2")
            #inactivehepa1
            if(vaccine.hepa1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("inactive hepa #1")
            #inactivehepa2
            if(vaccine.hepa2_date is None):
                if(vaccine.hepa1_date is not None):
                    if((date-vaccine.hepa1_date).days > 180):
                        q.append("inactive hepa #2")
            #inf1
            if(vaccine.inf1_date is None):
                if((date-patient.bday).days > 180):
                    q.append("inf #1")
            #inf2
            if(vaccine.inf2_date is None):
                if(vaccine.inf1_date is not None):
                    if((date-vaccine.inf1_date).days > 28):
                        q.append("inf #2")
            #annual flu
            if(vaccine.anf_date is None):
                q.append("annual flu")
            else:
                if((date-vaccine.anf_date).days > 360):
                    q.append("annual flu")
            #ipv/opv1
            if(vaccine.ipv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("ipv/opv #1")
            #ipv/opv2
            if(vaccine.ipv2_date is None):
                if(vaccine.ipv1_date is not None):
                    if((date-vaccine.ipv1_date).days > 28):
                        q.append("ipv/opv #2")
            #ipv/opv3
            if(vaccine.ipv3_date is None):
                if(vaccine.ipv2_date is not None):
                    if((date-vaccine.ipv2_date).days > 28):
                        q.append("ipv/opv #3")
            #ipv/opv booster 1
            if(vaccine.ipv4_date is None):
                if((date-patient.bday).days > 360):
                    q.append("ipv/opv booster #1")
            #ipv/opv booster 2
            if(vaccine.ipv5_date is None):
                if((date-patient.bday).days > 1440):
                    q.append("ipv/opv booster #2")
            #japencb1
            if(vaccine.japb1_date is None):
                if((date-patient.bday).days > 270):
                    q.append("jap enc b #1")
            #japencb2
            if(vaccine.japb2_date is None):
                if(vaccine.japb1_date is not None):
                    if(360 < (date-vaccine.japb1_date).days <= 720):
                        q.append("jap enc b #2")
            #msl
            if(vaccine.msl_date is None):
                if((date-patient.bday).days > 180):
                    q.append("measles")
            #men
            if(vaccine.men_date is None):
                    if(720< (date-patient.bday).days < 19800):
                        q.append("meninggo")
            #mmr1
            if(vaccine.mmr1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("mmr #1")
            #mmr2
            if(vaccine.mmr2_date is None):
                if(vaccine.mmr1_date is not None):
                    if(((date-patient.bday).days > 1440) |
                            ((date-vaccine.mmr1_date).days > 28)):
                            q.append("mmr #2")
            #pcv1
            if(vaccine.pcv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("pcv #1")
            #pcv2
            if(vaccine.pcv2_date is None):
                if(vaccine.pcv1_date is not None):
                    if((date-vaccine.pcv1_date).days > 28):
                        q.append("pcv #2")
            #pcv3
            if(vaccine.pcv3_date is None):
                if(vaccine.pcv2_date is not None):
                    if((date-vaccine.pcv2_date).days > 28):
                        q.append("pcv #3")
            #pcv booster1
            if(vaccine.pcv4_date is None):
                if(vaccine.pcv3_date is not None):
                    if((date-vaccine.pcv3_date).days > 180):
                        q.append("pcv booster #1")
            #rota1
            if(vaccine.rota1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("rota #1")
            #rota2
            if(vaccine.rota2_date is None):
                if(vaccine.rota1_date is not None):
                    if((date-vaccine.rota1_date).days > 28):
                        q.append("rota #2")
            #rota3
            if(vaccine.rota3_date is None):
                if(vaccine.rota2_date is not None):
                    if((date-vaccine.rota2_date).days > 28):
                        q.append("rota #3")
            #td
            if(vaccine.td_date is None):
                if(3240 < (date-patient.bday).days <= 5400):
                    q.append("td")
            #typ
            if(vaccine.typ_date is None):
                if((date-patient.bday).days > 720):
                    q.append("typ")
            else:
                if(720 < (date-vaccine.typ_date).days <= 1080):
                    q.append("typ")
            #var1
            if(vaccine.var1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("var #1")
            #var2
            if(vaccine.var2_date is None):
                if(vaccine.var1_date is not None):
                    if(((date-patient.bday).days > 1440 ) |
                    ((date-vaccine.var1_date).days > 90)):
                        q.append("var #2")
            #query filter
            if (len(q) == 0):
                due_vax_result = due_vax_result.exclude(user=patient.user)
        
        else:
            q = []
            date = request.POST.get('date')
            date = datetime.date.fromisoformat(date)
            # age = date - patient.bday
            vaccine = Vaccine.objects.get(user = patient.user)
            # print(age)
            # print(patient.bday)
            if(vaccine.bcg_date is None):
                q.append("bcg")
            #dtap1
            if(vaccine.dtap1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("dtap #1")
            #dtap2
            if(vaccine.dtap2_date is None):
                if(vaccine.dtap1_date is not None):
                    if((date-vaccine.dtap1_date).days > 28): 
                        q.append("dtap #2")
                        #dtap3
            if(vaccine.dtap3_date is None):
                if(vaccine.dtap2_date is not None):
                    if((date-vaccine.dtap2_date).days > 28): 
                        q.append("dtap #3")
            #dtap booster 1
            if(vaccine.dtap4_date is None):
                if((date-patient.bday).days > 350):
                    q.append("dtap booster #1")
            #dtap booster 2
            if(vaccine.dtap5_date is None):
                if((date-patient.bday).days > 1400):
                    q.append("dtap booster #2")
            #hepb1
            if(vaccine.hepb1_date is None):
                q.append("hepb #1")
            #hepb2
            if(vaccine.hepb2_date is None):
                if((date-patient.bday).days > 30):
                    q.append("hepb #2")
            #hepb3
            if(vaccine.hepb3_date is None):
                if((date-patient.bday).days > 180):
                    q.append("hepb #3")
            #hib1
            if(vaccine.hib1_date is None):
                if(vaccine.hepb3_date is not None):
                    if((date-vaccine.hepb3_date).days > 42):
                        q.append("hib #1")
            #hib2
            if(vaccine.hib2_date is None):
                if(vaccine.hib1_date is not None):
                    if((date-vaccine.hib1_date).days > 28):
                        q.append("hib #2")
            #hib3
            if(vaccine.hib3_date is None):
                if(vaccine.hib2_date is not None):
                    if((date-vaccine.hib2_date).days > 28):
                        q.append("hib #3")
            #hib booster1
            if(vaccine.hib4_date is None):
                if(vaccine.hib3_date is not None):
                    if((date-vaccine.hib3_date).days > 180):
                        q.append("hib booster #1")
            #hpv11
            if (vaccine.hpv11_date is None):
                q.append("hpv #1 of 1")
            #hpv12
            if(vaccine.hpv12_date is None):
                if(vaccine.hpv11_date is not None):
                    if(9<years<15):
                        if ((date-vaccine.hpv11_date).days > 180):
                            q.append("hpv #1 of 2")
            #hpv21
            if(vaccine.hpv21_date is None):
                if (vaccine.hpv21_date is None):
                    q.append("hpv #2 of 1")
            #hpv22
            if(vaccine.hpv22_date is None):
                if(vaccine.hpv21_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv21_date).days > 120):
                            q.append("hpv #2 of 2")
            #hpv23
            if(vaccine.hpv23_date is None):
                if(vaccine.hpv22_date is not None):
                    if(years>=15):
                        if ((date-vaccine.hpv22_date).days > 180):
                            q.append("hpv #3 of 2")
            #inactivehepa1
            if(vaccine.hepa1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("inactive hepa #1")
            #inactivehepa2
            if(vaccine.hepa2_date is None):
                if(vaccine.hepa1_date is not None):
                    if((date-vaccine.hepa1_date).days > 180):
                        q.append("inactive hepa #2")
            #inf1
            if(vaccine.inf1_date is None):
                if((date-patient.bday).days > 180):
                    q.append("inf #1")
            #inf2
            if(vaccine.inf2_date is None):
                if(vaccine.inf1_date is not None):
                    if((date-vaccine.inf1_date).days > 28):
                        q.append("inf #2")
            #annual flu
            if(vaccine.anf_date is None):
                q.append("annual flu")
            else:
                if((date-vaccine.anf_date).days > 360):
                    q.append("annual flu")
            #ipv/opv1
            if(vaccine.ipv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("ipv/opv #1")
            #ipv/opv2
            if(vaccine.ipv2_date is None):
                if(vaccine.ipv1_date is not None):
                    if((date-vaccine.ipv1_date).days > 28):
                        q.append("ipv/opv #2")
            #ipv/opv3
            if(vaccine.ipv3_date is None):
                if(vaccine.ipv2_date is not None):
                    if((date-vaccine.ipv2_date).days > 28):
                        q.append("ipv/opv #3")
            #ipv/opv booster 1
            if(vaccine.ipv4_date is None):
                if((date-patient.bday).days > 360):
                    q.append("ipv/opv booster #1")
            #ipv/opv booster 2
            if(vaccine.ipv5_date is None):
                if((date-patient.bday).days > 1440):
                    q.append("ipv/opv booster #2")
            #japencb1
            if(vaccine.japb1_date is None):
                if((date-patient.bday).days > 270):
                    q.append("jap enc b #1")
            #japencb2
            if(vaccine.japb2_date is None):
                if(vaccine.japb1_date is not None):
                    if(360 < (date-vaccine.japb1_date).days <= 720):
                        q.append("jap enc b #2")
            #msl
            if(vaccine.msl_date is None):
                if((date-patient.bday).days > 180):
                    q.append("measles")
            #men
            if(vaccine.men_date is None):
                    if(720< (date-patient.bday).days < 19800):
                        q.append("meninggo")
            #mmr1
            if(vaccine.mmr1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("mmr #1")
            #mmr2
            if(vaccine.mmr2_date is None):
                if(vaccine.mmr1_date is not None):
                    if(((date-patient.bday).days > 1440) |
                            ((date-vaccine.mmr1_date).days > 28)):
                            q.append("mmr #2")
            #pcv1
            if(vaccine.pcv1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("pcv #1")
            #pcv2
            if(vaccine.pcv2_date is None):
                if(vaccine.pcv1_date is not None):
                    if((date-vaccine.pcv1_date).days > 28):
                        q.append("pcv #2")
            #pcv3
            if(vaccine.pcv3_date is None):
                if(vaccine.pcv2_date is not None):
                    if((date-vaccine.pcv2_date).days > 28):
                        q.append("pcv #3")
            #pcv booster1
            if(vaccine.pcv4_date is None):
                if(vaccine.pcv3_date is not None):
                    if((date-vaccine.pcv3_date).days > 180):
                        q.append("pcv booster #1")
            #rota1
            if(vaccine.rota1_date is None):
                if((date-patient.bday).days > 42):
                    q.append("rota #1")
            #rota2
            if(vaccine.rota2_date is None):
                if(vaccine.rota1_date is not None):
                    if((date-vaccine.rota1_date).days > 28):
                        q.append("rota #2")
            #rota3
            if(vaccine.rota3_date is None):
                if(vaccine.rota2_date is not None):
                    if((date-vaccine.rota2_date).days > 28):
                        q.append("rota #3")
            #td
            if(vaccine.td_date is None):
                if(3240 < (date-patient.bday).days <= 5400):
                    q.append("td")
            #typ
            if(vaccine.typ_date is None):
                if((date-patient.bday).days > 720):
                    q.append("typ")
            else:
                if(720 < (date-vaccine.typ_date).days <= 1080):
                    q.append("typ")
            #var1
            if(vaccine.var1_date is None):
                if((date-patient.bday).days > 360):
                    q.append("var #1")
            #var2
            if(vaccine.var2_date is None):
                if(vaccine.var1_date is not None):
                    if(((date-patient.bday).days > 1440 ) |
                    ((date-vaccine.var1_date).days > 90)):
                        q.append("var #2")
            #query filter
            if (len(q) == 0):
                due_vax_result = due_vax_result.exclude(user=patient.user)
            
    # print(q)
    myFilter = RecordFilter(request.GET, queryset=due_vax_result)
    due_vax_result = myFilter.qs

    # for due vaccine list
    if (request.method != 'POST'):
        if(vaccine.bcg_date is None):
            remind.append("bcg")
        #dtap1
        if(vaccine.dtap1_date is None):
            if((datetime.date.today()-record.bday).days > 42):
                remind.append("dtap #1")
        #dtap2
        if(vaccine.dtap2_date is None):
            if(vaccine.dtap1_date is not None):
                if((datetime.date.today()-vaccine.dtap1_date).days > 28): 
                    remind.append("dtap #2")
        #dtap3
        if(vaccine.dtap3_date is None):
            if(vaccine.dtap2_date is not None):
                if((datetime.date.today()-vaccine.dtap2_date).days > 28): 
                    remind.append("dtap #3")
        #dtap booster 1
        if(vaccine.dtap4_date is None):
            if((datetime.date.today()-record.bday).days > 350):
                remind.append("dtap booster #1")
        #dtap booster 2
        if(vaccine.dtap5_date is None):
            if((datetime.date.today()-record.bday).days > 1400):
                remind.append("dtap booster #2")
        #hepb1
        if(vaccine.hepb1_date is None):
            remind.append("hepb #1")
        #hepb2
        if(vaccine.hepb2_date is None):
            if((datetime.date.today()-record.bday).days > 30):
                remind.append("hepb #2")
        #hepb3
        if(vaccine.hepb3_date is None):
            if((datetime.date.today()-record.bday).days > 180):
                remind.append("hepb #3")
        #hib1
        if(vaccine.hib1_date is None):
            if(vaccine.hepb3_date is not None):
                if((datetime.date.today()-vaccine.hepb3_date).days > 42):
                    remind.append("hib #1")
        #hib2
        if(vaccine.hib2_date is None):
            if(vaccine.hib1_date is not None):
                if((datetime.date.today()-vaccine.hib1_date).days > 28):
                    remind.append("hib #2")
        #hib3
        if(vaccine.hib3_date is None):
            if(vaccine.hib2_date is not None):
                if((datetime.date.today()-vaccine.hib2_date).days > 28):
                    remind.append("hib #3")
        #hib booster1
        if(vaccine.hib4_date is None):
            if(vaccine.hib3_date is not None):
                if((datetime.date.today()-vaccine.hib3_date).days > 180):
                    remind.append("hib booster #1")
        #hpv11
        if (vaccine.hpv11_date is None):
            remind.append("hpv #1 of 1")
        #hpv12
        if(vaccine.hpv12_date is None):
            if(vaccine.hpv11_date is not None):
                if(9<years<15):
                    if ((datetime.date.today()-vaccine.hpv11_date).days > 180):
                        remind.append("hpv #1 of 2")
        #hpv21
        if(vaccine.hpv21_date is None):
            if (vaccine.hpv21_date is None):
                remind.append("hpv #2 of 1")
        #hpv22
        if(vaccine.hpv22_date is None):
            if(vaccine.hpv21_date is not None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv21_date).days > 120):
                        remind.append("hpv #2 of 2")
        #hpv23
        if(vaccine.hpv23_date is None):
            if(vaccine.hpv22_date is not None):
                if(years>=15):
                    if ((datetime.date.today()-vaccine.hpv22_date).days > 180):
                        remind.append("hpv #3 of 2")
        #inactivehepa1
        if(vaccine.hepa1_date is None):
            if((datetime.date.today()-record.bday).days > 360):
                remind.append("inactive hepa #1")
        #inactivehepa2
        if(vaccine.hepa2_date is None):
            if(vaccine.hepa1_date is not None):
                if((datetime.date.today()-vaccine.hepa1_date).days > 180):
                    remind.append("inactive hepa #2")
        #inf1
        if(vaccine.inf1_date is None):
            if((datetime.date.today()-record.bday).days > 180):
                remind.append("inf #1")
        #inf2
        if(vaccine.inf2_date is None):
            if(vaccine.inf1_date is not None):
                if((datetime.date.today()-vaccine.inf1_date).days > 28):
                    remind.append("inf #2")
        #annual flu
        if(vaccine.anf_date is None):
            remind.append("annual flu")
        else:
            if((datetime.date.today()-vaccine.anf_date).days > 360):
                remind.append("annual flu")
        #ipv/opv1
        if(vaccine.ipv1_date is None):
            if((datetime.date.today()-record.bday).days > 42):
                remind.append("ipv/opv #1")
        #ipv/opv2
        if(vaccine.ipv2_date is None):
            if(vaccine.ipv1_date is not None):
                if((datetime.date.today()-vaccine.ipv1_date).days > 28):
                    remind.append("ipv/opv #2")
        #ipv/opv3
        if(vaccine.ipv3_date is None):
            if(vaccine.ipv2_date is not None):
                if((datetime.date.today()-vaccine.ipv2_date).days > 28):
                    remind.append("ipv/opv #3")
        #ipv/opv booster 1
        if(vaccine.ipv4_date is None):
            if((datetime.date.today()-record.bday).days > 360):
                remind.append("ipv/opv booster #1")
        #ipv/opv booster 2
        if(vaccine.ipv5_date is None):
            if((datetime.date.today()-record.bday).days > 1440):
                remind.append("ipv/opv booster #2")
        #japencb1
        if(vaccine.japb1_date is None):
            if((datetime.date.today()-record.bday).days > 270):
                remind.append("jap enc b #1")
        #japencb2
        if(vaccine.japb2_date is None):
            if(vaccine.japb1_date is not None):
                if(360 < (datetime.date.today()-vaccine.japb1_date).days <= 720):
                    remind.append("jap enc b #2")
        #msl
        if(vaccine.msl_date is None):
            if((datetime.date.today()-record.bday).days > 180):
                remind.append("measles")
        #men
        if(vaccine.men_date is None):
                if(720< (datetime.date.today()-record.bday).days < 19800):
                    remind.append("meninggo")
        #mmr1
        if(vaccine.mmr1_date is None):
            if((datetime.date.today()-record.bday).days > 360):
                remind.append("mmr #1")
        #mmr2
        if(vaccine.mmr2_date is None):
            if(vaccine.mmr1_date is not None):
                if(((datetime.date.today()-record.bday).days > 1440) |
                        ((datetime.date.today()-vaccine.mmr1_date).days > 28)):
                        remind.append("mmr #2")
        #pcv1
        if(vaccine.pcv1_date is None):
            if((datetime.date.today()-record.bday).days > 42):
                remind.append("pcv #1")
        #pcv2
        if(vaccine.pcv2_date is None):
            if(vaccine.pcv1_date is not None):
                if((datetime.date.today()-vaccine.pcv1_date).days > 28):
                    remind.append("pcv #2")
        #pcv3
        if(vaccine.pcv3_date is None):
            if(vaccine.pcv2_date is not None):
                if((datetime.date.today()-vaccine.pcv2_date).days > 28):
                    remind.append("pcv #3")
        #pcv booster1
        if(vaccine.pcv4_date is None):
            if(vaccine.pcv3_date is not None):
                if((datetime.date.today()-vaccine.pcv3_date).days > 180):
                    remind.append("pcv booster #1")
        #rota1
        if(vaccine.rota1_date is None):
            if((datetime.date.today()-record.bday).days > 42):
                remind.append("rota #1")
        #rota2
        if(vaccine.rota2_date is None):
            if(vaccine.rota1_date is not None):
                if((datetime.date.today()-vaccine.rota1_date).days > 28):
                    remind.append("rota #2")
        #rota3
        if(vaccine.rota3_date is None):
            if(vaccine.rota2_date is not None):
                if((datetime.date.today()-vaccine.rota2_date).days > 28):
                    remind.append("rota #3")
        #td
        if(vaccine.td_date is None):
            if(3240 < (datetime.date.today()-record.bday).days <= 5400):
                remind.append("td")
        #typ
        if(vaccine.typ_date is None):
            if((datetime.date.today()-record.bday).days > 720):
                remind.append("typ")
        else:
            if(720 < (datetime.date.today()-vaccine.typ_date).days <= 1080):
                remind.append("typ")

        #var1
        if(vaccine.var1_date is None):
            if((datetime.date.today()-record.bday).days > 360):
                remind.append("var #1")
        #var2
        if(vaccine.var2_date is None):
            if(vaccine.var1_date is not None):
                if(((datetime.date.today()-record.bday).days > 1440 ) |
                ((datetime.date.today()-vaccine.var1_date).days > 90)):
                    remind.append("var #2")

    else:
        date = request.POST.get('date')
        date = datetime.date.fromisoformat(date)
        # age = date - patient.bday
        vaccine = Vaccine.objects.get(user = record.user)
        if(vaccine.bcg_date is None):
            remind.append("bcg")
        #dtap1
        if(vaccine.dtap1_date is None):
            if((date-record.bday).days > 42):
                remind.append("dtap #1")
        #dtap2
        if(vaccine.dtap2_date is None):
            if(vaccine.dtap1_date is not None):
                if((date-vaccine.dtap1_date).days > 28): 
                    remind.append("dtap #2")
        #dtap3
        if(vaccine.dtap3_date is None):
            if(vaccine.dtap2_date is not None):
                if((date-vaccine.dtap2_date).days > 28): 
                    remind.append("dtap #3")
        #dtap booster 1
        if(vaccine.dtap4_date is None):
            if((date-record.bday).days > 350):
                remind.append("dtap booster #1")
        #dtap booster 2
        if(vaccine.dtap5_date is None):
            if((date-record.bday).days > 1400):
                remind.append("dtap booster #2")
        #hepb1
        if(vaccine.hepb1_date is None):
            remind.append("hepb #1")
        #hepb2
        if(vaccine.hepb2_date is None):
            if((date-record.bday).days > 30):
                remind.append("hepb #2")
        #hepb3
        if(vaccine.hepb3_date is None):
            if((date-record.bday).days > 180):
                remind.append("hepb #3")
        #hib1
        if(vaccine.hib1_date is None):
            if(vaccine.hepb3_date is not None):
                if((date-vaccine.hepb3_date).days > 42):
                    remind.append("hib #1")
        #hib2
        if(vaccine.hib2_date is None):
            if(vaccine.hib1_date is not None):
                if((date-vaccine.hib1_date).days > 28):
                    remind.append("hib #2")
        #hib3
        if(vaccine.hib3_date is None):
            if(vaccine.hib2_date is not None):
                if((date-vaccine.hib2_date).days > 28):
                    remind.append("hib #3")
        #hib booster1
        if(vaccine.hib4_date is None):
            if(vaccine.hib3_date is not None):
                if((date-vaccine.hib3_date).days > 180):
                    remind.append("hib booster #1")
        #hpv11
        if (vaccine.hpv11_date is None):
            remind.append("hpv #1 of 1")
        #hpv12
        if(vaccine.hpv12_date is None):
            if(vaccine.hpv11_date is not None):
                if(9<years<15):
                    if ((date-vaccine.hpv11_date).days > 180):
                        remind.append("hpv #1 of 2")
        #hpv21
        if(vaccine.hpv21_date is None):
            if (vaccine.hpv21_date is None):
                remind.append("hpv #2 of 1")
        #hpv22
        if(vaccine.hpv22_date is None):
            if(vaccine.hpv21_date is not None):
                if(years>=15):
                    if ((date-vaccine.hpv21_date).days > 120):
                        remind.append("hpv #2 of 2")
        #hpv23
        if(vaccine.hpv23_date is None):
            if(vaccine.hpv22_date is not None):
                if(years>=15):
                    if ((date-vaccine.hpv22_date).days > 180):
                        remind.append("hpv #3 of 2")
        #inactivehepa1
        if(vaccine.hepa1_date is None):
            if((date-record.bday).days > 360):
                remind.append("inactive hepa #1")
        #inactivehepa2
        if(vaccine.hepa2_date is None):
            if(vaccine.hepa1_date is not None):
                if((date-vaccine.hepa1_date).days > 180):
                    remind.append("inactive hepa #2")
        #inf1
        if(vaccine.inf1_date is None):
            if((date-record.bday).days > 180):
                remind.append("inf #1")
        #inf2
        if(vaccine.inf2_date is None):
            if(vaccine.inf1_date is not None):
                if((date-vaccine.inf1_date).days > 28):
                    remind.append("inf #2")
        #annual flu
        if(vaccine.anf_date is None):
            remind.append("annual flu")
        else:
            if((date-vaccine.anf_date).days > 360):
                remind.append("annual flu")
        #ipv/opv1
        if(vaccine.ipv1_date is None):
            if((date-record.bday).days > 42):
                remind.append("ipv/opv #1")
        #ipv/opv2
        if(vaccine.ipv2_date is None):
            if(vaccine.ipv1_date is not None):
                if((date-vaccine.ipv1_date).days > 28):
                    remind.append("ipv/opv #2")
        #ipv/opv3
        if(vaccine.ipv3_date is None):
            if(vaccine.ipv2_date is not None):
                if((date-vaccine.ipv2_date).days > 28):
                    remind.append("ipv/opv #3")
        #ipv/opv booster 1
        if(vaccine.ipv4_date is None):
            if((date-record.bday).days > 360):
                remind.append("ipv/opv booster #1")
        #ipv/opv booster 2
        if(vaccine.ipv5_date is None):
            if((date-record.bday).days > 1440):
                remind.append("ipv/opv booster #2")
        #japencb1
        if(vaccine.japb1_date is None):
            if((date-record.bday).days > 270):
                remind.append("jap enc b #1")
        #japencb2
        if(vaccine.japb2_date is None):
            if(vaccine.japb1_date is not None):
                if(360 < (date-vaccine.japb1_date).days <= 720):
                    remind.append("jap enc b #2")
        #msl
        if(vaccine.msl_date is None):
            if((date-record.bday).days > 180):
                remind.append("measles")
        #men
        if(vaccine.men_date is None):
                if(720< (date-record.bday).days < 19800):
                    remind.append("meninggo")
        #mmr1
        if(vaccine.mmr1_date is None):
            if((date-record.bday).days > 360):
                remind.append("mmr #1")
        #mmr2
        if(vaccine.mmr2_date is None):
            if(vaccine.mmr1_date is not None):
                if(((date-record.bday).days > 1440) |
                        ((date-vaccine.mmr1_date).days > 28)):
                        remind.append("mmr #2")
        #pcv1
        if(vaccine.pcv1_date is None):
            if((date-record.bday).days > 42):
                remind.append("pcv #1")
        #pcv2
        if(vaccine.pcv2_date is None):
            if(vaccine.pcv1_date is not None):
                if((date-vaccine.pcv1_date).days > 28):
                    q.append("pcv #2")
        #pcv3
        if(vaccine.pcv3_date is None):
            if(vaccine.pcv2_date is not None):
                if((date-vaccine.pcv2_date).days > 28):
                    q.append("pcv #3")
        #pcv booster1
        if(vaccine.pcv4_date is None):
            if(vaccine.pcv3_date is not None):
                if((date-vaccine.pcv3_date).days > 180):
                    remind.append("pcv booster #1")
        #rota1
        if(vaccine.rota1_date is None):
            if((date-record.bday).days > 42):
                remind.append("rota #1")
        #rota2
        if(vaccine.rota2_date is None):
            if(vaccine.rota1_date is not None):
                if((date-vaccine.rota1_date).days > 28):
                    remind.append("rota #2")
        #rota3
        if(vaccine.rota3_date is None):
            if(vaccine.rota2_date is not None):
                if((date-vaccine.rota2_date).days > 28):
                    remind.append("rota #3")
        #td
        if(vaccine.td_date is None):
            if(3240 < (date-record.bday).days <= 5400):
                remind.append("td")
        #typ
        if(vaccine.typ_date is None):
            if((date-record.bday).days > 720):
                remind.append("typ")
        else:
            if(720 < (date-vaccine.typ_date).days <= 1080):
                remind.append("typ")
        #var1
        if(vaccine.var1_date is None):
            if((date-record.bday).days > 360):
                remind.append("var #1")
        #var2
        if(vaccine.var2_date is None):
            if(vaccine.var1_date is not None):
                if(((date-record.bday).days > 1440 ) |
                ((date-vaccine.var1_date).days > 90)):
                    remind.append("var #2")

    data =  {'patients':due_vax_result,'myFilter':myFilter,'notExist':notExist, 'vaccines':remind}
    return render(request,'vaccinerecordapp/tool/reminder.html',data)

def send_email_reminder(request,pk):
    patient = PatientRecord.objects.get(id = pk)
    email = patient.user.email
    first_name = patient.first_name
    last_name = patient.last_name
    subject = "Reminder for due vaccine: "
    message = "<h1> Good day " + first_name + " " + last_name + "! We are writing to inform you that you have due vaccinations."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
   
    email.content_subtype = 'html'
    email.send()
    print("sent")    
    data = {'patient':patient}
    return render(request,'vaccinerecordapp/tool/reminder.html',data)
