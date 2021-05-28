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


# Create your views here.

def isCentroVerified(request):
    # Si no hay cuenta de Centro asociada al User actual
    if len(CentroDeReciclaje.objects.filter(usuario=request.user)) < 1:
        messages.warning(request,
                         "Esta cuenta no esta Verificada como Coperativa o Empresa.  <a style='color:white;text-decoration: underline' class='modal-trigger' href='#cuentaNoVerificadaModal'>Leer Mas.</a>")
        return None
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
    return render(request, "dashboard.html", {})


@login_required
def intermediariosView(request):
    isCentroVerified(request)
    intermediarios = Intermediario.objects.filter(puntos__centro__usuario=request.user)
    puntosDelCentro = PuntoDeAcopio.objects.filter(centro=CentroDeReciclaje.objects.get(usuario=request.user))
    return render(request, "intermediarios.html", {"intermediarios": intermediarios,
                                                   "puntosDelCentro": puntosDelCentro})


@login_required
def addIntermediarioView(request):
    isCentroVerified(request)
    puntosDelCentro = PuntoDeAcopio.objects.filter(centro=CentroDeReciclaje.objects.get(usuario=request.user))
    return render(request, "addintermediario.html", {"puntosDelCentro": puntosDelCentro})


@login_required
def perfilView(request):
    centro = isCentroVerified(request)
    social = False
    if len(SocialAccount.objects.filter(user_id=request.user.id)) > 0:  # El Usuario esta logeado con SocialApp
        social = True
    return render(request, "perfil.html", {"social": social, 'centro' : centro})


@login_required
def puntosView(request):
    isCentroVerified(request)
    puntos = PuntoDeAcopio.objects.filter(centro__usuario=request.user)
    return render(request, "puntos.html", {"puntos":puntos})

@login_required
def updatePerfilView(request):
    if request.method == "POST":
        # Si no hay cuenta de Centro asociada al User actual creo una
        if len(CentroDeReciclaje.objects.filter(usuario=request.user)) < 1:
            CentroDeReciclaje.objects.create(
                usuario=request.user,
                nombre=request.POST.get("nombre"),
                ubicacion=request.POST.get("ubicacion"),
                telefono=request.POST.get("telefono"),
                horarioInicio=request.POST.get("horarioInicio"),
                horarioFinal=request.POST.get("horarioFinal"),
            )
        #Sino hago el Update
        else:
            centro = CentroDeReciclaje.objects.get(usuario=request.user)
            centro.usuario = request.user
            centro.nombre = request.POST.get("nombre")
            centro.ubicacion = request.POST.get("ubicacion")
            centro.telefono = request.POST.get("telefono")
            centro.horarioInicio = request.POST.get("horarioInicio")
            centro.horarioFinal = request.POST.get("horarioFinal")
            centro.save()
        messages.success(request, "Perfil Actualizado con Exito")
    return redirect("/perfil")

@login_required
def changePasswordView(request):
    if request.method == "POST":
        if request.user.check_password(request.POST.get("actual")):
            if request.POST.get("password1") == request.POST.get("password2"):
                request.user.set_password(request.POST.get("password1"))
                messages.success(request, "Contraseña Cambiada con Exito")
        else:
            messages.success(request, "CONTRASEÑA ACTUAL INCORRECTA, INTENTE DE NUEVO")
    return redirect("/perfil")

@login_required
def updatePuntoView(request):
    if request.method == "POST":
        if request.POST.get("id") == None: #Crear nuevo Punto
            PuntoDeAcopio.objects.create(
                centro=CentroDeReciclaje.objects.get(usuario=request.user),
                nombre=request.POST.get("nombre_punto"),
                ubicacion=request.POST.get("nombre_punto"),
                tipoDeReciclado=request.POST.get("tipo_reciclado")
            )
            messages.success(request, "Punto creado con Exito")
        else: #Actualizar Info de Existente
            punto = PuntoDeAcopio.objects.get(id=request.POST.get("id"))
            punto.nombre = request.POST.get("nombre_punto_modal")
            punto.ubicacion = request.POST.get("ubicacion_modal")
            punto.tipoDeReciclado = request.POST.get("tipo_reciclado_modal")
            punto.save()
            messages.success(request, "Punto ({}) actualizado con Exito".format(punto.nombre))
    return redirect("/puntosdeacopio")

@login_required
def updateIntermediarioView(request):
    #Verificar que le pertenece el intermediario al Centro
    if request.method == "POST":
        if request.POST.get("id") == None: #Crear nuevo Intermediario
            intermediario = Intermediario.objects.create(
                nombre=request.POST.get("nombre"),
                telefono=request.POST.get("telefono"),
                diasRecoleccion=request.POST.get("diasRecoleccion"),
            )
            for punto in request.POST.get("puntos"):
                intermediario.puntos.add(PuntoDeAcopio.objects.get(id=punto))
            messages.success(request, "Intermediario creado con Exito")
        else: #Actualizar Info del Existente
            intermediario = Intermediario.objects.get(id=request.POST.get("id"))
            intermediario.nombre = request.POST.get("nombre")
            intermediario.telefono = request.POST.get("telefono")
            print(request.POST.get("puntos"))
            for punto in intermediario.puntos.all():
                intermediario.puntos.remove(punto)
            for punto in request.POST.get("puntos"):
                intermediario.puntos.add(PuntoDeAcopio.objects.get(nombre=punto))

            intermediario.diasRecoleccion = request.POST.get("diasRecoleccion")
            intermediario.save()
            messages.success(request, "Intermediario ({}) actualizado con Exito".format(intermediario.nombre))
    return redirect("/intermediarios")

@login_required
def deleteIntermediarioView(request, id):
    intermediario = get_object_or_404(Intermediario, id=id)
    #Verifico que el intermediario pertenezca al centro
    if intermediario.puntos.first().centro != CentroDeReciclaje.objects.get(usuario=request.user):
        messages.error(request, "Error al eliminar Intermediario")
    else:
        nombre = intermediario.nombre
        intermediario.delete()
        messages.success(request, "Intermediario ({}) eliminado con Exito".format(nombre))
    return redirect("/intermediarios")


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


def homeView(request):
    return render(request, 'home.html')


def aboutView(request):
    return render(request, 'somos.html')
