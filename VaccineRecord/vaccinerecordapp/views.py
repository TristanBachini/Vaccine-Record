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

# Create your views here.

def home(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            print("should work")
            return render(request, 'vaccinerecordapp/dashboard.html')
        else:
            messages.error(request,"Invalid Email or Password")
    form = LoginForm()
    data = {"form":form}
        
    return render(request, 'vaccinerecordapp/home.html',data)


@login_required(login_url='/home')
def dashboard(request):
    return render(request,'vaccinerecordapp/dashboard.html')

def create_patient(request):
    if(request.method == "POST"):
        form = UserForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, "Account was created for " +
                             form.cleaned_data.get("username"))
            group = Group.objects.get(name="patient")
            user = User.objects.get(username = form.cleaned_data.get("username"))
            user.groups.add(group) 
            return redirect('')
    else:
        messages.error(request, "Something was wrong with the input, please try again and make sure every field is filled is filled correctly.")

    data = {"form":form}
    return render(request, 'vaccinerecordapp/search-create-patient.html',data)

@login_required(login_url='/')
def search_create_patient(request):
    form = UserForm(request.POST)
    data = {"form":form}
    return render(request, 'vaccinerecordapp/search-create-patient.html',data)

@login_required(login_url='/')
def tool(request): 
    return render(request, 'vaccinerecordapp/tool.html')

@login_required(login_url='/')
def staff(request): 
    return render(request, 'vaccinerecordapp/staff.html')

def passwordReset(request): 
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "vaccinerecordapp/password_reset_email.txt"
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
    return render(request=request, template_name="vaccinerecordapp/password-reset.html", context={"password_reset_form":password_reset_form})