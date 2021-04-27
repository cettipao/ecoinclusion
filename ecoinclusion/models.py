from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from multiselectfield import MultiSelectField

# Create your models here.

class Contribuyente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username


class Intermediario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    delanteDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    dorsoDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.usuario.username


class CentroDeReciclaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    coordenadas = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    celular = PhoneField(blank=True, help_text='Celular')

    def __str__(self):
        return self.usuario.username

materiales =(
    ("1", "Secos"),
    ("2", "Humedos"),
    ("3", "Alumnio"),
)
class PuntoDeAcopio(models.Model):
    coordenadas = models.CharField(max_length=100)
    tipoDeReciclado = MultiSelectField(choices=materiales, max_choices=3, max_length=1)
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.usuario.username

