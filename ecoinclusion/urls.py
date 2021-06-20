from django.urls import path
from .views import *


from rest_framework import routers, serializers, viewsets
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
     path('api', include(router.urls)),
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
     path('updateperfil', updatePerfilView, name="updateperfil"),
     path('changepassword', changePasswordView, name="changepassword"),
     path('updatepunto', updatePuntoView, name="updatepunto"),
     path('updateintermediario/delete/<int:id>', deleteIntermediarioView, name="deleteintermedario"),
     path('updateintermediario', updateIntermediarioView, name="updateintermediario"),

]