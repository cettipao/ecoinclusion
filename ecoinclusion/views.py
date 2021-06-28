
# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User

# Django rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import TemplateHTMLRenderer

# Social accounts imports
from allauth.socialaccount.models import SocialAccount

# My imports
from .forms import *
from .models import *
from .decorators import *


# Create your views here.

def isCentroVerified(request):
    # Si no hay cuenta de Centro asociada al User actual
    if len(CentroDeReciclaje.objects.filter(usuario=request.user)) < 1:
        messages.warning(request,
                         "Esta cuenta no esta Verificada como Cooperativa o Empresa.  <a style='color:white;text-decoration: underline' class='modal-trigger' href='#cuentaNoVerificadaModal'>Leer Mas.</a>")
        centro = CentroDeReciclaje.objects.create(usuario=request.user)
        return centro
    else:
        #Si hay una cuenta y esta verificada
        if CentroDeReciclaje.objects.get(usuario=request.user).verificado:
            return CentroDeReciclaje.objects.get(usuario=request.user)
        #Si no esta verificada
        else:
            messages.warning(request,
                             "Esta cuenta no esta Verificada como Coperativa o Empresa.  <a style='color:white;text-decoration: underline' class='modal-trigger' href='#cuentaNoVerificadaModal'>Leer Mas.</a>")
            return CentroDeReciclaje.objects.get(usuario=request.user)

@login_required
def dashboardView(request):
    isCentroVerified(request)
    puntos = PuntoDeAcopio.objects.filter(centro__usuario=request.user)
    return render(request, "dashboard.html", {"puntos": puntos})

class FormAndObject():
    def __init__(self,object,form):
        self.object = object
        self.form = form
       
   
@login_required
def intermediariosView(request):
    isCentroVerified(request)
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)
    

    instance = Intermediario(centro=centro)
    form = IntermediarioForm(instance=instance)
    if request.method == "POST":
        intermediario = Intermediario(centro=centro)
        form = IntermediarioForm(request.POST,instance=intermediario)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Intermediario {obj.nombre} creado con Exito.")
            form = IntermediarioForm(instance=instance)
        else:
            messages.error(request, "El formulario no es valido.")
    
    intermediarios = Intermediario.objects.filter(centro=centro)
    forms_and_objects = []
    for intermediario in intermediarios:
        f = IntermediarioForm(instance=intermediario)
        form_and_object = FormAndObject(form=f,object=intermediario)
        forms_and_objects.append(form_and_object)
    context = {
        "intermediarios_form":forms_and_objects,
        'form':form,
        'google_api_key':settings.APY_KEY,
    }
    return render(request, "intermediarios.html", context)

@login_required
def deleteIntermediarioView(request,id):
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediario = get_object_or_404(Intermediario, id=id)
    #Verifico que el Punto pertenezca al centro
    
    nombre = intermediario.nombre
    intermediario.delete()
    messages.success(request, "Intermediario ({}) eliminado con Exito".format(nombre))
    return redirect("intermediarios")

@login_required
def updateIntermediarioView(request,id):
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediario = get_object_or_404(Intermediario, id=id)
    
    if request.method == "POST":
        form = IntermediarioForm(request.POST,instance=intermediario)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Intermediario {obj.nombre} actualizado con Exito.")
        else:
            messages.error(request, "El formulario no es valido.")
    
    return redirect("intermediarios")

@login_required
def puntosView(request):
    isCentroVerified(request)
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)
    insatnce = PuntoDeAcopio(centro=centro)
    form = PuntoDeAcopioForm(instance=insatnce)
    if request.method == "POST":
        punto_de_acopio = PuntoDeAcopio(centro=centro)
        form = PuntoDeAcopioForm(request.POST,instance=punto_de_acopio)
        
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Centro {obj.nombre} creado con Exito.")
            form = PuntoDeAcopioForm(instance=insatnce)
        else:
            messages.error(request, "El formulario no es valido.")

    puntos = PuntoDeAcopio.objects.filter(centro=centro)
    forms_and_objects = []
    for punto in puntos:
        f = PuntoDeAcopioForm(instance=punto)
        form_and_object = FormAndObject(form=f,object=punto)
        forms_and_objects.append(form_and_object)
        
    context = {
        "puntos_form":forms_and_objects,
        'form':form,
        'google_api_key':settings.APY_KEY,
    }
    return render(request, "puntos.html", context)

@login_required
def deletePuntoView(request, id):
    punto = get_object_or_404(PuntoDeAcopio, id=id)
    #Verifico que el Punto pertenezca al centro
    if punto.centro != CentroDeReciclaje.objects.get(usuario=request.user):
        messages.error(request, "Error al eliminar el Punto de Acopio")
    else:
        nombre = punto.nombre
        punto.delete()
        messages.success(request, "Punto de Acopio ({}) eliminado con Exito".format(nombre))
    return redirect("puntosdeacopio")

@login_required
def updatePuntoView(request,id):
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    punto = get_object_or_404(PuntoDeAcopio, id=id)
    
    if request.method == "POST":
        form = PuntoDeAcopioForm(request.POST,instance=punto)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Punto de acopio {obj.nombre} actualizado con Exito.")
        else:
            messages.error(request, "El formulario no es valido.")
    
    return redirect("puntosdeacopio")

@login_required
def perfilView(request):
    centro = isCentroVerified(request)
    social = False
    if len(SocialAccount.objects.filter(user_id=request.user.id)) > 0:  # El Usuario esta logeado con SocialApp
        social = True
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)
    form = CentroDeReciclajeForm(instance=centro)   
    context = {
        'form':form,
        "social": social,
        'google_api_key':settings.APY_KEY,
    }
    return render(request, "perfil.html", context)

@login_required
def updatePerfilView(request):
    if request.method == "POST":
        form = CentroDeReciclajeForm(request.POST)
        if len(CentroDeReciclaje.objects.filter(usuario=request.user)) < 1:
            if form.is_valid():
                obj = form.save()
        #Sino hago el Update
        else:
            form = CentroDeReciclajeForm(request.POST,instance=CentroDeReciclaje.objects.get(usuario=request.user))
            if form.is_valid():
                obj = form.save()
        messages.success(request, "Perfil Actualizado con Exito")
    return redirect("perfil")

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")

@unauthenticated_user
def loginView(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Exitoso")
            return redirect('dashboard')
        else:
            messages.error(request, "Username o Contraseña Incorrecta")
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, "Account was created for " + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

@login_required
def changePasswordView(request):
    if request.method == "POST":
        if request.user.check_password(request.POST.get("actual")):
            if request.POST.get("password1") == request.POST.get("password2"):
                request.user.set_password(request.POST.get("password1"))
                messages.success(request, "Contraseña Cambiada con Exito")
        else:
            messages.success(request, "CONTRASEÑA ACTUAL INCORRECTA, INTENTE DE NUEVO")
    return redirect("perfil")

def homeView(request):
    return render(request, 'home.html')

def aboutView(request):
    return render(request, 'somos.html')


# Django Rest framework views


class ListUsers(APIView):
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'intermediario_list.html'
    
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        queryset = Intermediario.objects.all()
        return Response({'intermediarios': queryset})
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        
        #Return a list of all users.
        
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)