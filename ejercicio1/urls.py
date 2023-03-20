from django.urls import path
from . import views

urlpatterns = [
    path("plato",views.obtenerPlato),
    path("categoria",views.obtenerCategorias),
    path("ingredientes",views.ingredientes),
    path("pasos",views.Pasos),
    path("login",views.login),
    path("registrarCategoria",views.registrarCategoria),
    path("modificarCategoria",views.modificarCategoria),
    path("eliminarCategoria",views.eliminarCategoria),
    path("registrarPlato",views.registrarPlato),
    path("modificarPlato",views.modificarPlato),
    path("eliminarPlato",views.eliminarPlato),
    path("registrarIngredientes",views.registrarIngredientes),
    path("modificarIngrediente",views.modificarIngrediente),
    path("eliminarIngrediente",views.eliminarIngrediente),
    path("registrarPasos",views.registrarPasos),
    path("modificarPaso",views.modificarPaso),
    path("eliminarPaso",views.eliminarPaso)
    
    
]