from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PuntoDeAcopio)
admin.site.register(Contribuyente)
admin.site.register(Intermediario)
admin.site.register(CentroDeReciclaje)
admin.site.register(Dia)
admin.site.register(TipoDeReciclado)
admin.site.register(Deposito)