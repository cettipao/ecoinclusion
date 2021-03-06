import django_filters

from .models import (
    CentroDeReciclaje,
    Deposito,
    Intermediario,
    LugarDeReciclado,
    PuntoDeAcopio,
)


class IntermediarioFilter(django_filters.FilterSet):
    class Meta:
        model = Intermediario
        fields = {
            "nombre": ["icontains"],
            "lugares": ["exact"],
        }


class PuntoFilter(django_filters.FilterSet):
    lat = django_filters.RangeFilter()
    long = django_filters.RangeFilter()

    class Meta:
        model = PuntoDeAcopio
        fields = {
            "lat": [],
            "long": [],
            "direccion": ["icontains"],  
            "tipo_de_reciclado": ["exact"],
            "nombre": ["icontains"],
            "centro": ["exact"],
        }


class LugarDeRecicladoFilter(django_filters.FilterSet):
    lat = django_filters.RangeFilter()
    long = django_filters.RangeFilter()

    class Meta:
        model = LugarDeReciclado
        fields = {
            "lat": [],
            "long": [],
            "tipo_de_reciclado": ["exact"],
            "nombre": ["icontains"],
        }


class CentroFilter(django_filters.FilterSet):
    lat = django_filters.RangeFilter()
    long = django_filters.RangeFilter()

    class Meta:
        model = CentroDeReciclaje
        fields = {
            "lat": [],
            "long": [],
            "direccion": ["icontains"], 
            "nombre": ["icontains"],
            "verificado": ["exact"],
        }


class DepositoFilter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Deposito
        fields = {
            "fecha": [],
            "lugar": ["exact"],
            "verificado": ["exact"],
        }
