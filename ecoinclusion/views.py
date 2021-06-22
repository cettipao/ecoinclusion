from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *
from django.contrib import messages
from .models import *
from allauth.socialaccount.models import SocialAccount

from django.conf import settings

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

def cleanList(lista):
    string = ""
    first = True
    for i in list(lista):
        if first:
            string += i
            first = False
        else:
            string += ", {}".format(i)
    print(string)
    return string

@login_required
def dashboardView(request):
    isCentroVerified(request)
    puntos = PuntoDeAcopio.objects.filter(centro__usuario=request.user)
    return render(request, "dashboard.html", {"puntos": puntos})

class formIntermediario():
    def __init__(self,intermediario,form,choices):
        self.intermediario = intermediario
        self.form = form
        self.choices = choices
        
@login_required
def intermediariosView(request):
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediarios = Intermediario.objects.filter(centro=centro)
    
    context = {
        "intermediarios": intermediarios
    }
    return render(request, "intermediarios.html", context)

@login_required
def updateIntermediarioView(request,pk_intermediario):
    """if not request.user.has_perm('backend.add_artist'):
        raise PermissionDenied"""
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediario = get_object_or_404(Intermediario, pk=pk_intermediario)
    
    if request.method == 'POST':
        form = IntermediarioForm(data=request.POST,instance=intermediario)
        if form.is_valid():
            object = form.save()
            
            messages.success(request, "Intermediario ({}) actualizado con Exito".format(object.nombre))
            return redirect('intermediarios')    
    else:
        form = IntermediarioForm(instance=intermediario)
    context = {
        "form":form,
        "intermediario":intermediario,
    }
    return render(request,'updateintermediario.html',context)
    
@login_required
def addIntermediarioView(request):
    isCentroVerified(request)
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediario = Intermediario(centro=centro)
    form = IntermediarioForm(data=request.POST,instance=intermediario)
    if request.method == 'POST':
        form = IntermediarioForm(data=request.POST,instance=intermediario)
        if form.is_valid():
            object = form.save()
            
            messages.success(request, "Intermediario ({}) agregado con Exito".format(object.nombre))
            return redirect('intermediarios')    
    context = {
        "form":form
    }
    return render(request,'addintermediario.html',context)

@login_required
def deleteIntermediarioView(request, id):
    centro =  get_object_or_404(CentroDeReciclaje, usuario=request.user)
    intermediario = get_object_or_404(Intermediario,centro=centro,pk=id)
    nombre = intermediario.nombre
    intermediario.delete()
    messages.success(request, "Intermediario ({}) eliminado con Exito".format(nombre))
    return redirect("intermediarios")

@login_required
def puntosView(request):
    isCentroVerified(request)
    puntos = PuntoDeAcopio.objects.filter(centro__usuario=request.user)
    context = {
        "puntos":puntos,
        'google_api_key':settings.APY_KEY,
    }
    return render(request, "puntos.html", context)

@login_required
def updatePuntoView(request):
    if request.method == "POST":
        if request.POST.get("id") == None: #Crear nuevo Punto
            PuntoDeAcopio.objects.create(
                centro=get_object_or_404(CentroDeReciclaje, usuario=request.user),
                nombre=request.POST.get("nombre_punto"),
                lat=request.POST.get("lat"),
                long=request.POST.get("long"),
                tipoDeReciclado=cleanList(request.POST.getlist("tipo_reciclado"))
            )
            messages.success(request, "Punto creado con Exito")
        else: #Actualizar Info de Existente
            punto = PuntoDeAcopio.objects.get(id=request.POST.get("id"))
            punto.nombre = request.POST.get("nombre_punto")
            punto.lat = request.POST.get("lat")
            punto.long = request.POST.get("long")
            punto.tipoDeReciclado = cleanList(request.POST.getlist("tipo_reciclado"))
            punto.save()
            messages.success(request, "Punto ({}) actualizado con Exito".format(punto.nombre))
    return redirect("puntosdeacopio")

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
