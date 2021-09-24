
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
from rest_framework import status, permissions, generics
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
    try:
        centro = CentroDeReciclaje.objects.get(usuario=request.user)
    except:
        return Response(status=404, message="You have to register yor cooperative in the register page")
    #Si hay una cuenta y esta verificada
    if centro.verificado:
        return centro
    #Si no esta verificada
    else:
        messages.warning(request,
                            "Esta cuenta no esta Verificada como Coperativa o Empresa.  <a style='color:white;text-decoration: underline' class='modal-trigger' href='#cuentaNoVerificadaModal'>Leer Mas.</a>")
        return centro

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
    centro = isCentroVerified(request)
    

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
        'google_api_key':ApiKeyGoogleMaps.objects.first().key,
    }
    return render(request, "intermediarios.html", context)

@login_required
def deleteIntermediarioView(request,id):
    centro = isCentroVerified(request)
    
    intermediario = get_object_or_404(Intermediario, id=id)
    #Verifico que el Punto pertenezca al centro
    
    nombre = intermediario.nombre
    intermediario.delete()
    messages.success(request, "Intermediario ({}) eliminado con Exito".format(nombre))
    return redirect("intermediarios")

@login_required
def updateIntermediarioView(request,id):
    centro = isCentroVerified(request)
    
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
    centro = isCentroVerified(request)
    
   
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
        'google_api_key':ApiKeyGoogleMaps.objects.first().key,
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
    centro = isCentroVerified(request)
    

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
    
    form = CentroDeReciclajeForm(instance=centro)
    if request.method == "POST":
        form = CentroDeReciclajeForm(request.POST,instance=centro)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Perfil Actualizado con Exito") 
        else:
            messages.success(request, "Error en el formulario.") 
    context = {
        'form':form,
        "social": social,
        'google_api_key':ApiKeyGoogleMaps.objects.first().key,
    }
    return render(request, "perfil.html", context)

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
        centro = isCentroVerified(request)
        if user is not None:
            login(request, user)
            centro = isCentroVerified(request)
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
            centro = CentroDeReciclaje.objects.create(usuario=user)
            
            messages.success(request, "Account was created for " + username)
            login(request, user)
            return redirect('dashboard')
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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = CentroFilter

class PuntoReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = PuntoDeAcopio.objects.all()
    authentication_classes = ()
    serializer_class = PuntoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PuntoFilter

    
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

class CantidadRecicladoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = CantidadReciclado.objects.all()
    serializer_class = CantidadRecicladoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_class = DepositoFilter
    def create(self, request, *args, **kwargs):
        deposito  = get_object_or_404(Deposito,pk=request.data['deposito'])
        tipo_de_reciclado = get_object_or_404(TipoDeReciclado,pk=request.data['tipo_de_reciclado'])
        if deposito not in self.request.user.depositos.all():
            data = {
                "deposito": [
                    "This filed need to be part of the current user."
                ]
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        for cantidad in deposito.cantidades.all():
            if cantidad.tipo_de_reciclado == tipo_de_reciclado:
                data = {
                "tipo_de_reciclado": [
                    "This recycle type is already used."
                ]
                
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        queryset = None
        for deposito in user.depositos.all():
            if queryset == None:
                queryset = deposito.cantidades.all()
            else:
                queryset = deposito.cantidades.all() | queryset 
        
        return queryset

class DepositoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Deposito.objects.order_by('-fecha')
    serializer_class = DepositoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = DepositoFilter

    def create(self, request, *args, **kwargs):
        
        centro  = get_object_or_404(CentroDeReciclaje,pk=request.data['centro'])

        
       
        try:
            punto = PuntoDeAcopio.objects.get(pk=request.data['punto_de_acopio'])
            if punto.centro != centro:
                data = {
                    "punto_de_acopio": [
                        "El punto de acopio debe ser del centro elegido"
                    ]
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)    
        except:
            pass

        return super().create(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        queryset = user.depositos.order_by('-fecha')
        
        return queryset

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ()
    serializer_class = RegisterSerializer

class TipoDeRecicladoReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = TipoDeReciclado.objects.all()
    authentication_classes = ()
    serializer_class = TipoDeRecicladoSerializer

"""
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication])
def getIntermediariosId(request):
    return Response(list(Intermediario.objects.all().values("id")))
"""


    

   

    
    

    
        
        
