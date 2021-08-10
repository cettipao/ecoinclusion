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
        related_name='intermediarios',
        on_delete=models.CASCADE,
    )
    puntos = models.ManyToManyField(
        'PuntoDeAcopio',
    )
    dias_disponibles =  models.ManyToManyField('Dia',max_length=7)
   
    def __str__(self):
        return self.nombre

    def getPuntosName(self):
        list = ""
        first = True
        for i in self.puntos.all():
            if first:
                list += f"{i.nombre}"
                first = False
            else:
                list += f", {i.nombre}"
        return list

    def getDias(self):
        list = ""
        first = True
        for i in self.dias_disponibles.all():
            if first:
                list += f"{i.nombre}"
                first = False
            else:
                list += f", {i.nombre}"
        return list

class Dia(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class CentroDeReciclaje(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    telefono = PhoneField(blank=True, help_text='Celular', null=True)
    horario_inicio = models.TimeField( null=True, blank=True)
    horario_final = models.TimeField( null=True, blank=True)
    verificado = models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.usuario.username

class PuntoDeAcopio(models.Model):
    nombre = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    tipo_de_reciclado = models.ManyToManyField('TipoDeReciclado')
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        related_name='puntos',
        on_delete=models.CASCADE,
    )

    @property
    def cant_intermediarios(self):
        return len(Intermediario.objects.filter(puntos=self))
    
    def getTiporeciclado(self):
        list = ""
        first = True
        for i in self.tipo_de_reciclado.all():
            if first:
                list += f"{i.nombre}"
                first = False
            else:
                list += f", {i.nombre}"
        return list

    def __str__(self):
        return self.nombre

class TipoDeReciclado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre