from django.db import models

# Create your models here.
class CategoriaPlato(models.Model):
    nombre = models.CharField(max_length=150)
    CATEGORIA_ESTADO = (
        ("A","Activo"),
        ("I","Inactivo")
    )
    estado = models.CharField(max_length=1,choices=CATEGORIA_ESTADO)
    
    def __str__(self):
        return self.nombre#Pintar el nombre en la BD
    

class Plato(models.Model):
    nombre = models.CharField(max_length=150)
    link = models.URLField()
    #cantidad = models.PositiveSmallIntegerField()
    precio = models.FloatField()
    categoria = models.ForeignKey(CategoriaPlato, on_delete=models.CASCADE)
    PLATO_ESTADO = (
        ("A","Activo"),
        ("I","Inactivo")
    )
    estado = models.CharField(max_length=1,choices=PLATO_ESTADO)
    def __str__(self):
        return self.nombre#Pintar el nombre en la BD

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=150)    
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.plato}-{self.nombre}"

class Paso(models.Model):
    numero_paso = models.CharField(max_length=150)
    descripcion = models.TextField()
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.plato}-{self.numero_paso}"

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    contra = models.CharField(max_length=150)
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
    

