from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . models import CategoriaPlato, Plato, Ingrediente, Paso
import json


#http://127.0.0.1:8000/ejercicio1/plato?categoria=-1
@csrf_exempt#Te permite hacer una comunicacion de servidor al cliente, sin errores (403) SOLO PARA POST
def obtenerPlato(request):
    if request.method == "GET":
        idcategoria = request.GET.get("categoria")#Recogemos la info de la url del query, valor String
        if idcategoria == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)        
        # TODO: Consultas a base de datos -> HECHO
        #categoria__id=idCategoria
        #Un String con una categoria como comparacon no esta bien
        #Si al objeto quiero filtrar por su id
        #categoria__"valor"
        peliculasFiltradas = []

        if idcategoria == "-1":
            PeliculaQS = Plato.objects.all()
        else:
            PeliculaQS = Plato.objects.filter(categoria__id=idcategoria)
        
        for p in PeliculaQS:
            peliculasFiltradas.append(
              {
                "id":p.pk,
                "nombre":p.nombre,
                "link":p.link,
                "categoria":{
                "id":p.categoria.pk,
                "nombre":p.categoria.nombre
                },
                "precio":p.precio,
                "estado":p.estado
              }
            )
            


        dictResponse = {
            "error": "",
            "platos": peliculasFiltradas
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


#http://127.0.0.1:8000/ejercicio1/categoria
def obtenerCategorias(request):
    if request.method=="GET":
        #Lista en formato QuerySet
        #Filtrar categorias cuyo estado sea A de Activo
                                                   #Comparacion: stado="A"
        ListaCategoriasQuerySet = CategoriaPlato.objects.all()
    #ListaCategorias = list(ListaCategoriasQuerySet)#convertido a lista de python (NO FUNCIONA)
        #En su reemplazo hacemos esto:
        ListaCategorias = []
        for c in ListaCategoriasQuerySet:
            ListaCategorias.append({
                "id":c.id,
                "nombre":c.nombre
            })#convertido a lista de python
        dictOK = {
            "error" : "",
            "categoria" : ListaCategorias
        }
        #Para retornarlo en el frondend, tengo que convertirlo a un String JSON y no dicc
        return HttpResponse(json.dumps(dictOK))
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

#Obtener ingredientes por plato
#http://127.0.0.1:8000/ejercicio1/ingredientes?plato=-1

def ingredientes(request):
    if request.method=="GET":
        
        idplato = request.GET.get("plato")

        if idplato == None:
            dictError = {
                "error": "Debe enviar un plato como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)   
        
        ListaIngredientes = []
        if idplato=="-1":
           ListaIngredientesQuerySet = Ingrediente.objects.all()
        else:
            ListaIngredientesQuerySet = Ingrediente.objects.filter(plato__id=idplato)
            

        for p in ListaIngredientesQuerySet:
            ListaIngredientes.append({
                "id":p.pk,
                "nombre": p.nombre,
                "plato":{
                "id":p.plato.pk,
                "nombre":p.plato.nombre
                }
            })

        dictOk = {
            "error":"",
            "ingredientes":ListaIngredientes
        }
        return HttpResponse(json.dumps(dictOk))
    else:
        dictError = {
            "error":"Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
#Obtener pasos por plato
#http://127.0.0.1:8000/ejercicio1/pasos?plato=-1
def Pasos(request):
    if request.method=="GET":

        idplato = request.GET.get("plato")
        if idplato == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)   
        if idplato=="-1":
           ListaPasoQuerySet = Paso.objects.all()
        else:
            ListaPasoQuerySet = Paso.objects.filter(plato__id=idplato)

        ListaPaso = []

        for i in ListaPasoQuerySet:
            ListaPaso.append({
                "id":i.pk,
                "numero_paso": i.numero_paso,
                "descripcion":i.descripcion,
                "plato":{
                "id":i.plato.pk,
                "nombre":i.plato.nombre
                }
            })

        dictOk = {
            "error":"",
            "Pasos":ListaPaso
        }
        return HttpResponse(json.dumps(dictOk))
    else:
        dictError = {
            "error":"Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)