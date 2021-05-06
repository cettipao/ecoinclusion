from django.urls import path
from .views import *

urlpatterns = [
     path('',homeView, name="home"),
     path('login', loginView, name="login"),
     path('somos', aboutView, name="about"),
     path('register', registerView, name="register"),
     path('logout', logoutView, name="logout"),
     
]