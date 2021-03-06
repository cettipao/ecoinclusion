from datetime import datetime

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
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.utils.html import strip_tags


# Django rest framework imports
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import (
    permission_classes,
    api_view,
    authentication_classes,
)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions, viewsets
import django_filters.rest_framework

# Social accounts imports
from allauth.socialaccount.models import SocialAccount

# My imports
from .forms import (
    CentroDeReciclajeForm,
    CreateUserForm,
    IntermediarioForm,
    PuntoDeAcopioForm,
)
from .models import (
    ApiKeyGoogleMaps,
    CentroDeReciclaje,
    Deposito,
    Intermediario,
    LugarDeReciclado,
    PuntoDeAcopio,
    TipoDeReciclado,
)
from .decorators import (
    cooperative_verified_required,
    cooperative_verified_required_for_perfil,
    unauthenticated_user,
    orderInteranual,
)
from .serializers import (
    CentroSerializer,
    DepositoSerializer,
    IntermediarioSerializer,
    PuntoSerializer,
    RegisterSerializer,
    TipoDeRecicladoSerializer,
    LugarDeRecicladoSerializer,
)
from .filters import (
    CentroFilter,
    DepositoFilter,
    IntermediarioFilter,
    PuntoFilter,
    LugarDeRecicladoFilter,
)

# Django rest framework imports
from rest_framework import permissions
from rest_framework import routers, serializers, viewsets

# Create your views here.


@login_required
@cooperative_verified_required
def dashboardView(request):
    puntos = PuntoDeAcopio.objects.filter(centro__usuario=request.user)

    depositosYear = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    depositos = Deposito.objects.none()

    for punto in puntos:
        depositos_punto = Deposito.objects.filter(
            lugar=punto,
            fecha__gt=timezone.now().replace(
                year=timezone.now().year - 1, month=timezone.now().month + 1
            ),
        )
        depositos.union(depositos_punto)

    for deposito in depositos:
        if deposito.fecha.month == 1:
            # print(ausentismo.id)
            ausentismosYear[0] += 1
        elif deposito.fecha.month == 2:
            ausentismosYear[1] += 1
        elif deposito.fecha.month == 3:
            ausentismosYear[2] += 1
        elif deposito.fecha.month == 4:
            ausentismosYear[3] += 1
        elif deposito.fecha.month == 5:
            ausentismosYear[4] += 1
        elif deposito.fecha.month == 6:
            ausentismosYear[5] += 1
        elif deposito.fecha.month == 7:
            ausentismosYear[6] += 1
        elif deposito.fecha.month == 8:
            ausentismosYear[7] += 1
        elif deposito.fecha.month == 9:
            ausentismosYear[8] += 1
        elif deposito.fecha.month == 10:
            ausentismosYear[9] += 1
        elif deposito.fecha.month == 11:
            ausentismosYear[10] += 1
        elif deposito.fecha.month == 12:
            ausentismosYear[11] += 1

    depositosYear = orderInteranual(depositosYear)
    meses = orderInteranual(meses)

    return render(
        request,
        "dashboard.html",
        {"puntos": puntos, "depositosYear": depositosYear, "meses": meses},
    )


class FormAndObject:
    def __init__(self, object, form):
        self.object = object
        self.form = form


@login_required
@cooperative_verified_required
def intermediariosView(request):
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)

    instance = Intermediario(centro=centro)
    form = IntermediarioForm(instance=instance)
    if request.method == "POST":

        form = IntermediarioForm(request.POST, instance=instance)
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
        form_and_object = FormAndObject(form=f, object=intermediario)
        forms_and_objects.append(form_and_object)
    context = {
        "intermediarios_form": forms_and_objects,
        "form": form,
        "google_api_key": ApiKeyGoogleMaps.objects.first().key,
    }
    return render(request, "intermediarios.html", context)


"""
@unauthenticated_user
Paolo Cetti
- No termino de entender este decorador, de todas formas en esta vista 
no funciona
    if request.user.is_authenticated:
            return redirect('home')
- Osea que si el usuario esta authenticated, te redirrecciona al home?
- En este caso como si esta authenticated lo redirecciona el home y nunca
    ejecuta la funcion de eliminar, evitando que se elimine el intermediario
"""


@login_required
@cooperative_verified_required
def deleteIntermediarioView(request, id):
    print("DDDDD")

    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)

    intermediario = get_object_or_404(Intermediario, id=id)
    # Verifico que el Punto pertenezca al centro

    nombre = intermediario.nombre
    intermediario.delete()
    messages.success(request, "Intermediario ({}) eliminado con Exito".format(nombre))
    return redirect("intermediarios")


@login_required
@cooperative_verified_required
def updateIntermediarioView(request, id):
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)

    intermediario = get_object_or_404(Intermediario, id=id)

    if request.method == "POST":
        form = IntermediarioForm(request.POST, instance=intermediario)
        if form.is_valid():
            obj = form.save()
            messages.success(
                request, f"Intermediario {obj.nombre} actualizado con Exito."
            )
        else:
            messages.error(request, "El formulario no es valido.")

    return redirect("intermediarios")


@login_required
@cooperative_verified_required
def puntosView(request):
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)

    insatnce = PuntoDeAcopio(centro=centro)
    form = PuntoDeAcopioForm(instance=insatnce)
    if request.method == "POST":
        punto_de_acopio = PuntoDeAcopio(centro=centro)
        form = PuntoDeAcopioForm(request.POST, instance=punto_de_acopio)

        if form.is_valid():
            obj = form.save()
            messages.success(
                request, "Punto de acopio {} creado con Exito.".format(obj.nombre)
            )
            form = PuntoDeAcopioForm(instance=insatnce)
        else:
            messages.error(request, "El formulario no es valido.")

    puntos = PuntoDeAcopio.objects.filter(centro=centro)
    forms_and_objects = []
    for punto in puntos:
        f = PuntoDeAcopioForm(instance=punto)
        form_and_object = FormAndObject(form=f, object=punto)
        forms_and_objects.append(form_and_object)

    context = {
        "puntos_form": forms_and_objects,
        "form": form,
        "google_api_key": ApiKeyGoogleMaps.objects.first().key,
    }
    return render(request, "puntos.html", context)


@login_required
@cooperative_verified_required
def deletePuntoView(request, id):
    punto = get_object_or_404(PuntoDeAcopio, id=id)
    # Verifico que el Punto pertenezca al centro
    if punto.centro != CentroDeReciclaje.objects.get(usuario=request.user):
        messages.error(request, "Error al eliminar el Punto de Acopio")
    else:
        nombre = punto.nombre
        punto.delete()
        messages.success(
            request, "Punto de Acopio ({}) eliminado con Exito".format(nombre)
        )
    return redirect("puntosdeacopio")


@login_required
@cooperative_verified_required
def updatePuntoView(request, id):

    punto = get_object_or_404(PuntoDeAcopio, id=id)

    if request.method == "POST":
        form = PuntoDeAcopioForm(request.POST, instance=punto)
        if form.is_valid():
            obj = form.save()
            messages.success(
                request, f"Punto de acopio {obj.nombre} actualizado con Exito."
            )
        else:
            messages.error(request, "El formulario no es valido.")

    return redirect("puntosdeacopio")


@login_required
@cooperative_verified_required_for_perfil
def perfilView(request):
    centro = get_object_or_404(CentroDeReciclaje, usuario=request.user)
    social = False
    if (
        len(SocialAccount.objects.filter(user_id=request.user.id)) > 0
    ):  # El Usuario esta logeado con SocialApp
        social = True

    form = CentroDeReciclajeForm(instance=centro)
    if request.method == "POST":
        form = CentroDeReciclajeForm(request.POST, instance=centro)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Perfil Actualizado con Exito")
        else:
            messages.error(request, "Error en el formulario.")
    context = {
        "form": form,
        "social": social,
        "google_api_key": ApiKeyGoogleMaps.objects.first().key,
    }
    return render(request, "perfil.html", context)


def logoutView(request):
    if request.user.is_authenticated:
        messages.success(request, f"Chau {request.user.username}")
        logout(request)
        return redirect("home")


@unauthenticated_user
def loginView(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.success(request, "Hola de nuevo " + username + "!")
            return redirect("dashboard")
        else:
            messages.error(request, "Username o Contrase??a Incorrecta")
            return render(request, "login.html", context)

    return render(request, "login.html", context)


@unauthenticated_user
def registerView(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = ""
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            to_email = form.cleaned_data.get('email')
            message = render_to_string('email_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'email': to_email,
                    })
            plain_message = strip_tags(message)
            
            send_mail(mail_subject, plain_message, 'ecopuntos.com@gmail.com', [to_email],html_message=message)
            messages.success(request, f'Porfavor confirma tu email, te hemos enviado una verificacion para el email')
            #messages.success(request, "Bienvenido " + username + "!")
            #login(request, user)
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)

def activateView(request, uidb64, token, email):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email = email
        user.save()
        messages.success(request,"Gracias por la confirmacion del email. Ahora puede iniciar sesion en su cuenta")
        return redirect("login")
        
    else:
        messages.error(request,"El codigo de activacion es invalido, puede que ya confirmaste tu email.")
        
        return redirect("login")


@login_required
def changePasswordView(request):
    if request.method == "POST":
        if request.user.check_password(request.POST.get("actual")):
            if request.POST.get("password1") == request.POST.get("password2"):
                request.user.set_password(request.POST.get("password1"))
                messages.success(request, "Contrase??a Cambiada con Exito")
        else:
            messages.error(request, "Contrase??a actual incorrecta, intente de nuevo")
    return redirect("perfil")


def homeView(request):
    return render(request, "home.html")


def aboutView(request):
    return render(request, "somos.html")


def mobileView(request):
    return render(request, "mobile.html")


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
                try:
                    centro_obj = obj.centro
                except:
                    centro_obj = obj
                if centro_obj == centro:
                    return centro.verificado
                else:
                    return False
            except:
                return False


class LugarDeRecicladoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = LugarDeReciclado.objects.all()
    authentication_classes = ()
    serializer_class = LugarDeRecicladoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = LugarDeRecicladoFilter


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
    permission_classes = [permissions.IsAuthenticated, IsCentroVerified]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = IntermediarioFilter

    def perform_create(self, serializer):
        centro = get_object_or_404(CentroDeReciclaje, usuario=self.request.user)
        puntos = centro.puntos.all()
        serializer.save(centro=centro, puntos=puntos)


class DepositoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = Deposito.objects.order_by("-fecha")
    serializer_class = DepositoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = DepositoFilter

    def create(self, request, *args, **kwargs):

        try:
            lugar = LugarDeReciclado.objects.get(pk=request.data["lugar"])
            tipo_de_reciclado = TipoDeReciclado.objects.get(
                pk=request.data["tipo_de_reciclado"]
            )
            if tipo_de_reciclado not in lugar.tipo_de_reciclado.all():
                data = {
                    "tipo_de_reciclado": [
                        "El tipo de reciclado tiene que ser uno de los del lugar."
                    ]
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {
                "tipo_de_reciclado": ["This field has not to be null."],
                "lugar": ["This field has not to be null."],
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = user.depositos.order_by("-fecha")

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
