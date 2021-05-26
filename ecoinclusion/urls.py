from django.urls import path
from .views import *

urlpatterns = [
     path('',homeView, name="home"),
     path('login', loginView, name="login"),
     path('somos', aboutView, name="about"),
     path('register', registerView, name="register"),
     path('logout', logoutView, name="logout"),
     path('perfil', perfilView, name="perfil"),
     path('dashboard', dashboardView, name="dashboard"),
     path('puntosdeacopio', puntosView, name="puntosdeacopio"),
     path('intermediarios', intermediariosView, name="intermediarios"),
     path('agregarintermediario', addIntermediarioView, name="addintermediario"),

]