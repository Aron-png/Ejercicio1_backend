from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.CategoriaPlato)
admin.site.register(models.Plato)
admin.site.register(models.Ingrediente)
admin.site.register(models.Paso)
