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