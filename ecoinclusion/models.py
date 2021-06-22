from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

# Create your models here.

class Contribuyente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username



DAYS_WEEK = (
    
    (1,_('lunes')),
    (2,_('martes')),
    (3,_('miercoles')),
    (4,_('jueves')),
    (5,_('viernes')),
    (6,_('sabado')),
    (7,_('domingo')),
)
class Intermediario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = PhoneField(blank=True, help_text='Celular')
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #delanteDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    #dorsoDni = models.ImageField(max_length=100, upload_to='fotos/', blank=True, null=True)
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        on_delete=models.CASCADE,
    )
    puntos = models.ManyToManyField(
        'PuntoDeAcopio',
    )
    diasRecoleccion =  MultiSelectField(choices=DAYS_WEEK)
   
    def __str__(self):
        return self.nombre

    def getPuntosName(self):
        nombresPuntos = ""
        first = True
        for punto in self.puntos.all():
            if first:
                nombresPuntos += "{}".format(punto.nombre)
                first = False
            else:
                nombresPuntos += ", {}".format(punto.nombre)
        return nombresPuntos




class CentroDeReciclaje(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    telefono = PhoneField(blank=True, help_text='Celular', null=True)
    horarioInicio = models.TimeField( null=True, blank=True)
    horarioFinal = models.TimeField( null=True, blank=True)
    verificado = models.BooleanField(default=False)
    

    def __str__(self):
        return self.usuario.username

class PuntoDeAcopio(models.Model):
    nombre = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
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

