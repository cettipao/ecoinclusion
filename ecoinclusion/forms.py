from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import request
from multiselectfield import MultiSelectField


class UserForm(ModelForm):
    # last_name = forms.CharField(blank=False)
    # first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["last_name"].required = True
        self.fields["first_name"].required = True

    fields = ["basic_field"]


class CreateUserForm(UserCreationForm):
    # last_name = forms.CharField(blank=False)
    # first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["last_name"].required = True
        self.fields["first_name"].required = True


class IntermediarioForm(ModelForm):
    class Meta:
        model = Intermediario
        fields = ["nombre", "telefono", "lugares", "dias_disponibles"]

    def __init__(self, *args, **kwargs):
        super(IntermediarioForm, self).__init__(*args, **kwargs)

        instance = kwargs.get("instance")
        centro = instance.centro

        self.fields["nombre"].required = True
        self.fields["telefono"].required = True
        self.fields["lugares"].queryset = centro.puntos.all()
        self.fields["lugares"].required = True
        self.fields["dias_disponibles"].required = True


class CentroDeReciclajeForm(ModelForm):
    lat = forms.DecimalField(min_value=-90, max_value=90)
    long = forms.DecimalField(min_value=-180, max_value=180)

    class Meta:
        model = CentroDeReciclaje
        fields = [
            "nombre",
            "lat",
            "long",
            "telefono",
            "horario_inicio",
            "horario_final",
        ]

    def __init__(self, *args, **kwargs):
        super(CentroDeReciclajeForm, self).__init__(*args, **kwargs)
        self.fields["lat"].required = True
        self.fields["lat"].max_value = 90
        self.fields["lat"].min_value = -90
        self.fields["long"].required = True
        self.fields["long"].max_value = 180
        self.fields["long"].min_value = -180
        self.fields["nombre"].required = True
        self.fields["telefono"].required = True
        self.fields["horario_final"].required = True
        self.fields["horario_inicio"].required = True


class PuntoDeAcopioForm(ModelForm):
    lat = forms.DecimalField(min_value=-90, max_value=90)
    long = forms.DecimalField(min_value=-180, max_value=180)

    class Meta:
        model = PuntoDeAcopio
        fields = ["nombre", "lat", "long", "tipo_de_reciclado"]

    def __init__(self, *args, **kwargs):
        super(PuntoDeAcopioForm, self).__init__(*args, **kwargs)
        self.fields["lat"].required = True
        self.fields["lat"].max_value = 90
        self.fields["lat"].min_value = -90
        self.fields["long"].required = True
        self.fields["long"].max_value = 180
        self.fields["long"].min_value = -180
        self.fields["nombre"].required = True
        self.fields["tipo_de_reciclado"].required = False
        self.fields["tipo_de_reciclado"].blank = True
        self.fields["tipo_de_reciclado"].null = True
