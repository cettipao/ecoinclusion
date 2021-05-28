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
    nombre = models.CharField(max_length=100)
    telefono = PhoneField(blank=True, help_text='Celular')
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #delanteDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    #dorsoDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    puntos = models.ManyToManyField(
        'PuntoDeAcopio',
    )
    diasRecoleccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def getPuntosName(self):
        nombresPuntos = ""
        first = True
        for punto in self.puntos.all():
            if first:
                nombresPuntos += "{}".format(punto.nombre)
            else:
                nombresPuntos += ", {}".format(punto.nombre)
        return nombresPuntos



class CentroDeReciclaje(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    telefono = PhoneField(blank=True, help_text='Celular')
    horarioInicio = models.CharField(max_length=10, default="")
    horarioFinal = models.CharField(max_length=10, default="")
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

class PuntoDeAcopio(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    tipoDeReciclado = models.CharField(max_length=100)
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        on_delete=models.CASCADE,
    )

    @property
    def cant_intermediarios(self):
        return len(Intermediario.objects.filter(puntos=self))

    def __str__(self):
        return self.nombre

