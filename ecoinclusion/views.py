from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def logoutViews(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login_url")

def registerView(request):
    return render(request, 'register.html')

def loginView(request):
    return render(request,'login.html')