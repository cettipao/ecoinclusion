from django.urls import path
from .views import *

urlpatterns = [
     path('',homeView, name="home"),
     path('login', loginView, name="login"),
     path('somos', aboutView, name="about"),
     path('register', registerView, name="register"),
     path('logout', logoutView, name="logout"),
     path('perfil', perfilView, name="perfil"),
     path('updateperfil', updatePerfilView, name="updateperfil"),
     path('changepassword', changePasswordView, name="changepassword"),

     path('dashboard', dashboardView, name="dashboard"),
     
     path('puntosdeacopio', puntosView, name="puntosdeacopio"),
     path('puntosdeacopio/updatepunto', updatePuntoView, name="updatepunto"),
     path('puntosdeacopio/updatepunto/delete/<int:id>', deletePuntoView, name="deletepunto"),

     path('intermediarios', intermediariosView, name="intermediarios"),
     path('intermediarios/agregarintermediario', addIntermediarioView, name="addintermediario"),
     path('intermediarios/deleteintermiediario/<int:id>', deleteIntermediarioView, name="deleteintermediario"),
     path('intermediarios/updateintermediario/<int:pk_intermediario>', updateIntermediarioView, name="updateintermediario"),

     # Url patterns for django rest framework
     path('api/intermediario', ListUsers.as_view(), name="updateintermediario"),

]