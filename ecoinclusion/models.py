from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

# Create your models here.
class Dia(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class TipoDeReciclado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class LugarDeReciclado(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_de_reciclado = models.ManyToManyField("TipoDeReciclado")
    lat = models.DecimalField(max_digits=23, decimal_places=21, null=True, blank=True)
    long = models.DecimalField(max_digits=24, decimal_places=21, null=True, blank=True)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CentroDeReciclaje(LugarDeReciclado):
    usuario = models.OneToOneField(
        User, related_name="cooperativa", on_delete=models.CASCADE
    )
    telefono = models.CharField(max_length=50, null=True, blank=True)
    horario_apertura = models.TimeField(null=True, blank=True)
    horario_cierre = models.TimeField(null=True, blank=True)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return "Cooperativa " + self.nombre + " Usuario: " + self.usuario.username


class PuntoDeAcopio(LugarDeReciclado):
    centro = models.ForeignKey(
        "CentroDeReciclaje",
        related_name="puntos",
        on_delete=models.CASCADE,
    )

    @property
    def cant_depositos(self):
        return len(self.depositos.all())

    @property
    def cant_intermediarios(self):
        return len(Intermediario.objects.filter(lugares=self))

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
        return "Punto de acopio " + self.nombre


class Intermediario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    centro = models.ForeignKey(
        CentroDeReciclaje, related_name="intermediarios", on_delete=models.CASCADE
    )
    lugares = models.ManyToManyField(
        "LugarDeReciclado",
    )
    dias_disponibles = models.ManyToManyField("Dia", max_length=7)

    def __str__(self):
        return self.nombre

    def getPuntosName(self):
        list = ""
        first = True
        for i in self.lugares.all():
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


class Deposito(models.Model):
    user = models.ForeignKey(User, related_name="depositos", on_delete=models.CASCADE)
    lugar = models.ForeignKey(
        LugarDeReciclado, related_name="depositos", on_delete=models.CASCADE
    )
    tipo_de_reciclado = models.ForeignKey(
        "TipoDeReciclado", related_name="depositos", on_delete=models.CASCADE
    )
    cantidad = models.IntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=9, decimal_places=1, null=True, blank=True)
    fecha = models.DateField()
    fecha_deposito = models.DateField(null=True, blank=True)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} deposito {self.cantidad} con un peso total de {self.peso} ({self.fecha})"


class ApiKeyGoogleMaps(models.Model):
    key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.key
