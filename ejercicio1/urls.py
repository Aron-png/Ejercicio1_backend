from django.urls import path
from . import views

urlpatterns = [
    path("plato",views.obtenerPlato),
    path("categoria",views.obtenerCategorias),
    path("ingredientes",views.ingredientes),
    path("pasos",views.Pasos),
    path("login",views.login)
]