
from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers 


class PuntoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PuntoDeAcopio
        fields = ['nombre','lat','long','getTiporeciclado','cant_intermediarios','id','tipo_de_reciclado','centro']
         

class IntermediarioSerializer(serializers.ModelSerializer):
    centro = serializers.ReadOnlyField(source='centro.id')
   
    class Meta:
        model = Intermediario
        fields = ['url','id','nombre', 'telefono', 'centro', 'puntos', 'dias_disponibles']
        optional_fields = ['puntos']


class DepositoSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Deposito
        fields = ['user', 'tipo_de_reciclado', 'punto_de_acopio','fecha',]
        optional_fields = ['tipo_de_reciclado']


class CentroSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CentroDeReciclaje
        fields =  ['url','id','usuario','nombre','lat','long','telefono','horario_inicio','horario_final','verificado']
