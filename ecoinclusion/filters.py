import django_filters

from .models import *


class IntermediarioFilter(django_filters.FilterSet):
    class Meta:
        model = Intermediario
        fields = {
            'nombre': ['icontains'],
            'centro': ['exact'],
            'puntos': ['exact'],
        }

class PuntoFilter(django_filters.FilterSet):
    class Meta:
        model = PuntoDeAcopio
        fields = {
            'nombre': ['icontains'],
            'centro': ['exact'],
        }


class CentroFilter(django_filters.FilterSet):
    class Meta:
        model = CentroDeReciclaje
        fields = {
            'nombre': ['icontains'],
            'verificado': ['exact'],
        }      

class DepositoFilter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Deposito
        fields = {
            'fecha': [],
            'centro': ['exact'],
            'punto_de_acopio': ['exact'],
            'verificado': ['exact'],
        }   