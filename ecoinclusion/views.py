
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
from django.http import Http404

# Django rest framework imports
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions, viewsets
import django_filters.rest_framework

# Social accounts imports
from allauth.socialaccount.models import SocialAccount

# My imports
from .forms import *
from .models import *
from .decorators import *
from .serializers import *
from .filters import *

#Django rest framework imports
from rest_framework import permissions
from rest_framework import routers, serializers, viewsets
from .serializers import *
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



class IsCentroVerified(permissions.BasePermission):
    """
    Custom permission to only allow Centro de reciclajes verificados hacer ciertas funciones.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # Write permissions are only allowed to the owner of the snippet.
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True

        else:
            
            try:
                
                centro = CentroDeReciclaje.objects.get(usuario=request.user)
                return centro.verificado
            except:
                print("f")
                return False
            
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
                # Check permissions for read-only request
            return True

        else:
            
            try:
                
                centro = CentroDeReciclaje.objects.get(usuario=request.user)
                try :
                    centro_obj = obj.centro
                except:
                    centro_obj = obj
                if centro_obj == centro:
                    return centro.verificado
                else:
                    return False
            except:
                return False
        
        

class CentroReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = CentroDeReciclaje.objects.all()
    authentication_classes = ()
    serializer_class = CentroSerializer

    def get_queryset(self):
        verificado = self.request.query_params.get('verificado')
        if verificado == "true":
            return CentroDeReciclaje.objects.filter(verificado=True)
        elif verificado == "false":
            return CentroDeReciclaje.objects.filter(verificado=False)
        else:
            return CentroDeReciclaje.objects.all()

class PuntoReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = PuntoDeAcopio.objects.all()
    authentication_classes = ()
    serializer_class = PuntoSerializer

    
"""
class PuntoViewSet(viewsets.ModelViewSet):
    queryset = PuntoDeAcopio.objects.all()
    serializer_class = PuntoSerializer
    permission_classes = [permissions.IsAuthenticated,IsCentroVerified]
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PuntoFilter

    def perform_create(self, serializer):
        centro = get_object_or_404(CentroDeReciclaje, usuario=self.request.user)
        serializer.save(centro=centro)
"""
    

class IntermediarioViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Intermediario.objects.all()
    serializer_class = IntermediarioSerializer
    permission_classes = [permissions.IsAuthenticated,IsCentroVerified]
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = IntermediarioFilter
    
    def perform_create(self, serializer):
        centro = get_object_or_404(CentroDeReciclaje, usuario=self.request.user)
        puntos = centro.puntos.all()
        serializer.save(centro=centro,puntos=puntos)

class DepositoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Deposito.objects.all()
    serializer_class = DepositoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,SessionAuthentication)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data._mutable = True
        request.data['user'] = user.pk
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

"""
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication])
def getIntermediariosId(request):
    return Response(list(Intermediario.objects.all().values("id")))
"""


    

   

    
    

    
        
        
