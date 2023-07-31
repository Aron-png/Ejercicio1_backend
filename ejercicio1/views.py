from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt#Util al momento de usar POST
from . models import CategoriaPlato, Plato, Ingrediente, Paso, Usuario
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


'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/login
{
    "email": "aaronlivias0412@gmail.com",
    "password":"admin"
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt
def login(request):
    if request.method == "POST":
        #La data q obtenemos de registrarse en forma de String "request.body".
        dictDataRequest = json.loads(request.body)#convertir a diccionario
        email = dictDataRequest["email"]
        password = dictDataRequest["password"]
        
        ListaUsuariosQuerySet = Usuario.objects.all()
        
        evento = 0#Suponemos que la contrasea o usuario esta mal ingresado
        UsuarioSeleccionado = "nada"
        for i in ListaUsuariosQuerySet:
            
            if email == i.email and password == i.contra:
                evento = evento + 1
                UsuarioSeleccionado = i.nombre

        if evento == 1:
            #Correcto
            dictOk = {
                "error" : "",
                "usuario": UsuarioSeleccionado
            }
            return HttpResponse(json.dumps(dictOk))
        else:
            #Error login
            dictOk = {
                "error" : "No existe el usuario o password"
            }
            strError = json.dumps(dictOk)
            return HttpResponse(strError)

    else:
        #Error en caso que la peticion no sea post
        dictError = {
            "error" : "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/record
{
    "nombre":"aaron2.0",
    "email":"aarqe",
    "contra":"qwer"
}
'''
@csrf_exempt
def record(request):
    if request.method != "POST":
        dictError = {
            "error":"Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dictRecord = json.loads(request.body)
    
    email = dictRecord["email"]
    contra = dictRecord["contra"]
    nombre = dictRecord["nombre"]

    cat = Usuario(email=email, contra=contra, nombre=nombre)
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))
'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/registrarCategoria
{
    "nombre":"meriendas"
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt
def registrarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    #El Request esta siendo llamado. Con "json.loads" convertirmos en la cadena de texto en
    #un diccionario para poder asi acceder a sus valores con dictCategoria["nombre"].
    #En otras palabras, el dicc de que ponemos en el postman se llama con json.loads
    dictCategoria = json.loads(request.body)
    nombre = dictCategoria["nombre"]
    
    #          Se declara el objet cat
    #Lo esta haciendo directamente porque son String
    #El valor se le esta asignando el argumento de entrada "nombre=nombre"
    
    cat = CategoriaPlato(nombre=nombre)
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/modificarCategoria
{
    "id":4,
    "nombre":"Meriendas"
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def modificarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dicctCategoria = json.loads(request.body)

    identificador = dicctCategoria["id"]
    #cat = Categoria.objects.all() --> Ya no se usa esto, porque el filter devuelve una querySet
    #luego el querySet lo convierto en lista. No quiero lista Sino un objeto Categoria.

    #                Para eso utilizamos esta funcion get de DJANGO
    #Obtener (objeto Categoria = cat) de base de datos --> .objects.get(pk=identificador) 
    #.objects.get("nombre de la variable en el model Categoria"=identificador)
    cat = CategoriaPlato.objects.get(pk=identificador) 


    #Si hago una consulta de un elemento de categoria que no existe, "python" se cae
    #En otras palabras, si usamos esto "dicctCategoria["nombre"]" -> Sale Error
    #                Para eso utilizamos esta funcion get de PYTHON
    if dicctCategoria.get("nombre") != None:#Aqui pregunto si dentro del dicc hay o no un elemento
        cat.nombre = dicctCategoria.get("nombre")
    
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/eliminarCategoria
{
    "id":6 <--Seria el proximo id si se agrega otro
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def eliminarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dicctCategoria = json.loads(request.body)
    idCategoria = dicctCategoria["id"]

    if idCategoria == None:
        dictError = {
            "error": "Debe de enviar una categoria para eliminarlo"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    cat = CategoriaPlato.objects.get(pk=idCategoria)#Obtener la id de la Categoria
    cat.delete()#Elimino la categoria de la base de datos
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/registrarPlato
{
    "nombre":"Meriendas",
    "link":"https://tofuu.getjusto.com/orioneat-prod/kFaFECW7sCChsc9bb-orioneat-prod_sahHpYEDvABFbxk4j-S%C3%A1ndwich-triple-especial.png",
    "precio":13.4,
    "categoria":6,
    "estado":"A"
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt
def registrarPlato(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    #El Request esta siendo llamado. Con "json.loads" convertirmos en la cadena de texto en
    #un diccionario para poder asi acceder a sus valores con dictCategoria["nombre"].
    #En otras palabras, el dicc de que ponemos en el postman se llama con json.loads
    dictPlato = json.loads(request.body)
    nombre = dictPlato["nombre"]
    link = dictPlato["link"]
    precio = dictPlato["precio"]
    idcategoria = dictPlato["categoria"]
    estado = dictPlato["estado"]
    Instancia_Categoria=CategoriaPlato.objects.get(pk=idcategoria)
    #          Se declara el objet cat
    #Lo esta haciendo directamente porque son String
    #El valor se le esta asignando el argumento de entrada "nombre=nombre"
    
    cat = Plato(nombre=nombre,link=link,precio=precio,categoria=Instancia_Categoria,estado=estado)
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/modificarPlato
{
    "id":7,
    "nombre":"Triple",
    "link":"https://tofuu.getjusto.com/orioneat-prod/kFaFECW7sCChsc9bb-orioneat-prod_sahHpYEDvABFbxk4j-S%C3%A1ndwich-triple-especial.png",
    "precio":3.4,
    "categoria":6,
    "estado":"I"
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def modificarPlato(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dictPlato = json.loads(request.body)

    identificador = dictPlato["id"]
    #cat = Categoria.objects.all() --> Ya no se usa esto, porque el filter devuelve una querySet
    #luego el querySet lo convierto en lista. No quiero lista Sino un objeto Categoria.

    #                Para eso utilizamos esta funcion get de DJANGO
    #Obtener (objeto Categoria = cat) de base de datos --> .objects.get(pk=identificador) 
    #.objects.get("nombre de la variable en el model Categoria"=identificador)
    cat = Plato.objects.get(pk=identificador) 


    #Si hago una consulta de un elemento de categoria que no existe, "python" se cae
    #En otras palabras, si usamos esto "dictPlato["nombre"]" -> Sale Error
    #                Para eso utilizamos esta funcion get de PYTHON
    if dictPlato.get("nombre") != None:#Aqui pregunto si dentro del dicc hay o no un elemento
        cat.nombre = dictPlato.get("nombre")
    
    if dictPlato.get("link") != None:
        cat.link = dictPlato.get("link")
    
    if dictPlato.get("precio") != None:
        cat.precio = dictPlato.get("precio")
    
    if dictPlato.get("categoria") != None:
        idcategoria = dictPlato.get("categoria")
        Instancia_Categoria=CategoriaPlato.objects.get(pk=idcategoria)
        cat.categoria = Instancia_Categoria

    if dictPlato.get("estado") != None:
        cat.estado = dictPlato.get("estado")
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/eliminarPlato
{
    "id":8 <--Seria el proximo id si se agrega otro
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def eliminarPlato(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictPlato = json.loads(request.body)
    idPlato = dictPlato["id"]

    if idPlato == None:
        dictError = {
            "error": "Debe de enviar una categoria para eliminarlo"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    cat = Plato.objects.get(pk=idPlato)#Obtener la id de la Plato
    cat.delete()#Elimino la Plato de la base de datos
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/registrarIngredientes
{
    "nombre":"1",
    "plato":8
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt
def registrarIngredientes(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    #El Request esta siendo llamado. Con "json.loads" convertirmos en la cadena de texto en
    #un diccionario para poder asi acceder a sus valores con dictCategoria["nombre"].
    #En otras palabras, el dicc de que ponemos en el postman se llama con json.loads
    dictIngrediente = json.loads(request.body)
    nombre = dictIngrediente["nombre"]
    idplato = dictIngrediente["plato"]
    
    Instancia_plato=Plato.objects.get(pk=idplato)
    #          Se declara el objet cat
    #Lo esta haciendo directamente porque son String
    #El valor se le esta asignando el argumento de entrada "nombre=nombre"
    
    cat = Ingrediente(nombre=nombre, plato=Instancia_plato)
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/modificarIngrediente
{
    "id":69,
    "nombre":"Vino",
    "plato":8
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def modificarIngrediente(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dictIngrediente = json.loads(request.body)

    identificador = dictIngrediente["id"]
    #cat = Categoria.objects.all() --> Ya no se usa esto, porque el filter devuelve una querySet
    #luego el querySet lo convierto en lista. No quiero lista Sino un objeto Categoria.

    #                Para eso utilizamos esta funcion get de DJANGO
    #Obtener (objeto Categoria = cat) de base de datos --> .objects.get(pk=identificador) 
    #.objects.get("nombre de la variable en el model Categoria"=identificador)
    cat = Ingrediente.objects.get(pk=identificador) 


    #Si hago una consulta de un elemento de categoria que no existe, "python" se cae
    #En otras palabras, si usamos esto "dictIngrediente["nombre"]" -> Sale Error
    #                Para eso utilizamos esta funcion get de PYTHON
    if dictIngrediente.get("nombre") != None:#Aqui pregunto si dentro del dicc hay o no un elemento
        cat.nombre = dictIngrediente.get("nombre")
        
    if dictIngrediente.get("plato") != None:
        idplato = dictIngrediente.get("plato")
        Instancia_Plato=Plato.objects.get(pk=idplato)
        cat.plato = Instancia_Plato

        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/eliminarIngrediente
{
    "id":69 <--Seria el proximo id si se agrega otro
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def eliminarIngrediente(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictIngrediente = json.loads(request.body)
    idIngrediente = dictIngrediente["id"]

    if idIngrediente == None:
        dictError = {
            "error": "Debe de enviar una categoria para eliminarlo"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    cat = Ingrediente.objects.get(pk=idIngrediente)#Obtener la id de la Plato
    cat.delete()#Elimino la Plato de la base de datos
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/registrarPasos
{
    "numero_paso":1,
    "descripcion":"YA tu za",
    "plato":8
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt
def registrarPasos(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    #El Request esta siendo llamado. Con "json.loads" convertirmos en la cadena de texto en
    #un diccionario para poder asi acceder a sus valores con dictCategoria["nombre"].
    #En otras palabras, el dicc de que ponemos en el postman se llama con json.loads
    dictPasos = json.loads(request.body)
    numero_paso = dictPasos["numero_paso"]
    descripcion = dictPasos["descripcion"]
    idplato = dictPasos["plato"]
    
    Instancia_plato=Plato.objects.get(pk=idplato)
    #          Se declara el objet cat
    #Lo esta haciendo directamente porque son String
    #El valor se le esta asignando el argumento de entrada "nombre=nombre"
    
    cat = Paso(numero_paso=numero_paso, descripcion=descripcion,plato=Instancia_plato)
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/modificarPaso
{
    "id":39,
    "numero_paso":1,
    "descripcion":"YA tu zabezzz",
    "plato":8
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def modificarPaso(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dictPaso = json.loads(request.body)

    identificador = dictPaso["id"]
    #cat = Categoria.objects.all() --> Ya no se usa esto, porque el filter devuelve una querySet
    #luego el querySet lo convierto en lista. No quiero lista Sino un objeto Categoria.

    #                Para eso utilizamos esta funcion get de DJANGO
    #Obtener (objeto Categoria = cat) de base de datos --> .objects.get(pk=identificador) 
    #.objects.get("nombre de la variable en el model Categoria"=identificador)
    cat = Paso.objects.get(pk=identificador) 


    #Si hago una consulta de un elemento de categoria que no existe, "python" se cae
    #En otras palabras, si usamos esto "dictPaso["nombre"]" -> Sale Error
    #                Para eso utilizamos esta funcion get de PYTHON
    if dictPaso.get("numero_paso") != None:#Aqui pregunto si dentro del dicc hay o no un elemento
        cat.numero_paso = dictPaso.get("numero_paso")

    if dictPaso.get("descripcion") != None:
        cat.descripcion = dictPaso.get("descripcion")
        
    if dictPaso.get("plato") != None:
        idplato = dictPaso.get("plato")
        Instancia_Plato=Plato.objects.get(pk=idplato)
        cat.plato = Instancia_Plato

        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))

'''
Instalar Postman
http://127.0.0.1:8000/ejercicio1/eliminarPaso
{
    "id":69 <--Seria el proximo id si se agrega otro
}
El @csrf_exempt 
Solo se usa en POST
Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
'''
@csrf_exempt 
def eliminarPaso(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictPaso = json.loads(request.body)
    idPaso = dictPaso["id"]

    if idPaso == None:
        dictError = {
            "error": "Debe de enviar una categoria para eliminarlo"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    cat = Paso.objects.get(pk=idPaso)#Obtener la id de la Plato
    cat.delete()#Elimino la Plato de la base de datos
    dictOK = {
        "error" : ""
    }
        
    return HttpResponse(json.dumps(dictOK))