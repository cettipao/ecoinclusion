from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import request
from multiselectfield import MultiSelectField


class UserForm(ModelForm):
    #last_name = forms.CharField(blank=False)
    #first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    fields = ['basic_field']

class CreateUserForm(UserCreationForm):
    #last_name = forms.CharField(blank=False)
    #first_name = forms.CharField(blank=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True



class IntermediarioForm(ModelForm):
    class Meta:
        model = Intermediario
        fields = ['nombre','telefono','puntos','diasRecoleccion']
    def __init__(self, *args, **kwargs):
        super(IntermediarioForm, self).__init__(*args, **kwargs)


        instance = kwargs.get("instance")
        centro = instance.centro
        puntos = PuntoDeAcopio.objects.filter(centro=centro)
        self.fields['nombre'].required = True
        self.fields['telefono'].required = True
        self.fields['puntos'].queryset = puntos
        self.fields['puntos'].required = True
        self.fields['diasRecoleccion'].required = True


        
class CentroDeReciclajeForm(ModelForm):
    class Meta:
        model = CentroDeReciclaje
        fields = ['nombre','lat','long','telefono','horarioInicio','horarioFinal']
    def __init__(self, *args, **kwargs):
        super(CentroDeReciclajeForm, self).__init__(*args, **kwargs)
        self.fields['lat'].required = True
        self.fields['long'].required = True
        self.fields['lat'].hidden = True
        self.fields['long'].hidden = True
        self.fields['nombre'].required = True
        self.fields['telefono'].required = True
        self.fields['horarioFinal'].required = True
        self.fields['horarioInicio'].required = True