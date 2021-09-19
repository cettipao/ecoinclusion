
from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers 
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PuntoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PuntoDeAcopio
        fields = ['nombre','lat','long','getTiporeciclado','cant_intermediarios','id','tipo_de_reciclado','centro']
         
class TipoDeRecicladoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoDeReciclado
        fields = '__all__'

class IntermediarioSerializer(serializers.ModelSerializer):
    centro = serializers.ReadOnlyField(source='centro.id')
   
    class Meta:
        model = Intermediario
        fields = ['url','id','nombre', 'telefono', 'centro', 'puntos', 'dias_disponibles']
        optional_fields = ['puntos']


class DepositoSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Deposito
        fields = ['id','fecha','punto_de_acopio','centro','cantidades','getCantidades']
        optional_fields = ['punto_de_acopio']


class CantidadRecicladoSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(min_value=1)
    
    class Meta:
        model = CantidadReciclado
        fields = ['id','deposito','cantidad','peso','tipo_de_reciclado']
        optional_fields = ['peso']

class CentroSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CentroDeReciclaje
        fields =  ['url','id','usuario','nombre','lat','long','telefono','horario_inicio','horario_final','verificado']

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user