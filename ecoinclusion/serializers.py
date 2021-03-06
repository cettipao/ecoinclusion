from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags



class TipoDeRecicladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeReciclado
        fields = "__all__"


class LugarDeRecicladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LugarDeReciclado
        fields = "__all__"


class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroDeReciclaje
        fields = [
            "url",
            "id",
            "usuario",
            "nombre",
            "tipo_de_reciclado",
            "lat",
            "long",
            "direccion",
            "telefono",
            "horario_apertura",
            "horario_cierre",
            "verificado",
        ]


class PuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoDeAcopio
        fields = [
            "url",
            "id",
            "centro",
            "nombre",
            "tipo_de_reciclado",
            "lat",
            "long",
            "direccion",
            "getTiporeciclado",
            "cant_intermediarios",
        ]


class IntermediarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intermediario
        fields = [
            "url",
            "id",
            "nombre",
            "telefono",
            "centro",
            "lugares",
            "dias_disponibles",
        ]


class DepositoSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(min_value=1, max_value=100, allow_null=True)
    peso = serializers.DecimalField(
        min_value=1, max_value=100, max_digits=9, decimal_places=1, allow_null=True
    )
    fecha_deposito = serializers.DateTimeField(read_only=True)
    verificado = serializers.BooleanField(read_only=True)

    class Meta:
        model = Deposito
        fields = [
            "id",
            "lugar",
            "cantidad",
            "peso",
            "tipo_de_reciclado",
            "fecha",
            "fecha_deposito",
            "verificado",
        ]
        optional_fields = ["peso", "cantidad"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.email = ""
        user.save()
        current_site = "ecoinclusion.herokuapp.com"
        mail_subject = 'Activa tu cuenta'
        to_email = validated_data["email"]
        message = render_to_string('email_template.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'email': to_email,
                })
        
        plain_message = strip_tags(message)
            
        send_mail(mail_subject, plain_message, 'ecopuntos.com@gmail.com', [to_email],html_message=message)

        return user
