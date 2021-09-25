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
    usuario = models.OneToOneField(User,related_name='cooperativa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    lat = models.DecimalField(max_digits=23, decimal_places=21, null=True, blank=True)
    long = models.DecimalField(max_digits=24, decimal_places=21, null=True, blank=True)
    telefono = PhoneField(blank=True, help_text='Celular', null=True)
    horario_inicio = models.TimeField( null=True, blank=True)
    horario_final = models.TimeField( null=True, blank=True)
    verificado = models.BooleanField(default=False)
    

    def __str__(self):
        return self.nombre


class PuntoDeAcopio(models.Model):
    nombre = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=23, decimal_places=21, null=True, blank=True)
    long = models.DecimalField(max_digits=24, decimal_places=21, null=True, blank=True)
    tipo_de_reciclado = models.ManyToManyField('TipoDeReciclado')
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        related_name='puntos',
        on_delete=models.CASCADE,
    )
    @property
    def cant_depositos(self):
        return len(self.depositos.all())
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

class Deposito(models.Model):
    user = models.ForeignKey(User, related_name='depositos',on_delete=models.CASCADE)
    punto_de_acopio = models.ForeignKey(PuntoDeAcopio,related_name='depositos', on_delete=models.CASCADE,null=True, blank=True)
    centro = models.ForeignKey(
        'CentroDeReciclaje',
        related_name='depositos',
        on_delete=models.CASCADE
    )

    fecha = models.DateField()
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} deposito {self.getCantidades()} en la fecha {self.fecha}"

    def getCantidades(self):
    
        cant = 0
        peso = 0
        
        
        for i in self.cantidades.all():
            try:
                cant += i.cantidad
                peso += i.peso
            except:
                pass
        list = f"cantidad: {cant},peso: {peso}Kg"
        return list

class CantidadReciclado(models.Model):
    
    cantidad = models.IntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=9, decimal_places=1, null=True, blank=True)
    tipo_de_reciclado = models.ForeignKey('TipoDeReciclado',related_name="cantidades",on_delete=models.CASCADE)
    deposito = models.ForeignKey('Deposito', related_name='cantidades', on_delete=models.CASCADE)

    def __str__(self):
        try:
            list = f"deposito: {self.deposito} cantidad: {self.cantidad},peso: {self.peso}Kg, tipo de reciclado: {str(self.tipo_de_reciclado)}"
            return list
        except:
            list = f"deposito: {self.deposito}, tipo de reciclado: {str(self.tipo_de_reciclado)}"
            return list


class ApiKeyGoogleMaps(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.key

