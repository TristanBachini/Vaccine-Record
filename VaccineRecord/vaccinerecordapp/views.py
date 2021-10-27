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
                data = {"form1":form1, "form2":form2, "patients":patients}
                return render(request, 'vaccinerecordapp/dashboard.html',data)
            else:
                patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
                data = {'patient':patient}
                return render(request, 'vaccinerecordapp/patient-landing.html',data)
        else:
            messages.error(request,"Invalid Email or Password")
    form = LoginForm()
    data = {"form":form}
        
    return render(request, 'vaccinerecordapp/home.html',data)


@login_required(login_url='/home')
def dashboard(request):
    return render(request,'vaccinerecordapp/dashboard.html')

def create_record(request):
    form = PatientRecordForm()
    patients = PatientRecord.objects.all()
    print("create patient record")
    if(request.method == "POST"):
        print("pumasok post")
        username = request.POST.get('username')
        print('username')        
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
    data = {"form":form, "patients":patients}
    return render(request, 'vaccinerecordapp/patient-profile.html',data)

def update_patient_profile(request):
    patient = PatientRecord.objects.get(user = User.objects.get(username = request.user.username))
    form = UpdatePatientRecordForm(instance = patient)
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
            return redirect("/patient-landing")
        else:
            print(form.errors)
    data = {"form":form}
    return render(request, "vaccinerecordapp/update-patient-profile.html", data)

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
                    messages.success(request, "Account was created for " +
                                    form1.cleaned_data.get("username"))
                    group = Group.objects.get(name="patient")
                    user = User.objects.get(username = form1.cleaned_data.get("username"))
                    user.groups.add(group) 
                    return redirect('/create-patient-record')


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
            messages.success(request, "Account was created for " +
                            form1.cleaned_data.get("username"))
            group = Group.objects.get(name="patient")
            user = User.objects.get(username = form1.cleaned_data.get("username"))
            user.groups.add(group) 
            return redirect('/create-patient-record')


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
            lname = User.objects.get(last_name = form1.cleaned_data.get("last_name"))
            fname = User.objects.get(first_name = form1.cleaned_data.get("first_name"))
            form2 = DoctorForm({'user':user, 'last_name':lname, 'first_name':fname, 'contact':request.POST.get('contact'),'prefix':request.POST.get('prefix'),
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
        messages.error(request, "Something was wrong with the input, please try again and make sure every field is filled is filled correctly.")

    data = {"form1":form1, "form2":form2}
    return render(request, 'vaccinerecordapp/tool/staff.html',data)

@login_required(login_url='/')
def search_patient(request):
    patients = PatientRecord.objects.all()
    myFilter = RecordFilter(request.GET, queryset=patients)
    patients = myFilter.qs
    data = {"patients":patients, 'myFilter':myFilter}
    return render(request, 'vaccinerecordapp/search-patient.html',data)

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
def vaccine_record(request):
    #record = PatientRecord.objects.get(id = pk)

    #data = {"record":record}
    return render(request, 'vaccinerecordapp/vaccine-record.html')

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