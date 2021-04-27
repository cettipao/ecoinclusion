from django.contrib import admin
from .models import *

from django.forms import CheckboxSelectMultiple

# Overriding standart CheckboxSelectMultiple for jet admin
class JetCheckboxSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'admin/forms/widgets/checkbox_option.html'

# Register your models here.
@admin.register(PuntoDeAcopio)
class PuntoDeAcopioAdmin(admin.ModelAdmin):
    formfield_overrides = {
        MultiSelectField: {'widget': JetCheckboxSelectMultiple},
    }

admin.site.register(Contribuyente)
admin.site.register(Intermediario)
admin.site.register(CentroDeReciclaje)

