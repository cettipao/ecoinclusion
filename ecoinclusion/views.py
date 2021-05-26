from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from django.contrib import messages
from .models import *
from allauth.socialaccount.models import SocialAccount

# Create your views here.

@login_required
def dashboardView(request):
    return render(request, "dashboard.html", {})

@login_required
def intermediariosView(request):
    return render(request, "intermediarios.html", {})

@login_required
def addIntermediarioView(request):
    return render(request, "addintermediario.html", {})

@login_required
def perfilView(request):
    social= False
    if len(SocialAccount.objects.filter(user_id=request.user.id)) > 0:#El Usuario esta logeado con SocialApp
        social = True
    return render(request, "perfil.html", {"social":social})

@login_required
def puntosView(request):
    return render(request, "puntos.html", {})

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")

@unauthenticated_user
def loginView(request):
    context= {}
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request , username=username,password=password)
        if user is not None:
            login(request,user)
            messages.error(request, "Succefully loged in with account " + username)
            return redirect('dashboard')
        else :
            messages.error(request, "Username OR password is incorrect " )
            return render(request, 'login.html' , context)
    
    
    return render(request,'login.html',context)

@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, "Account was created for " + username)
            return redirect('login')
    context= {
        'form':form
    }
    return render(request, 'register.html' , context)


def homeView(request):
    return render(request, 'home.html')

def aboutView(request):
    return render(request, 'somos.html')
