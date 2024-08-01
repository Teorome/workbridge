from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

"""
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nom_aprendiz = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nom_aprendiz} {self.apellido}'
"""


class Proyecto(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nom_proyecto = models.CharField(max_length=255)
    nom_aprendiz = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField()
    telefono = models.CharField(max_length=15)
    contacto = models.EmailField()
    categoria = models.CharField(max_length=100)
    tiempo_desarrollo = models.PositiveIntegerField(blank=True, null=True)
    tecnologias = models.CharField(max_length=500, blank=True, null=True)
    colaboradores = models.PositiveIntegerField(blank=True, null=True)
    imagen = models.ImageField(upload_to='proyectos/')
    imagen1 = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    
    def __str__(self):
        return self.nom_proyecto



class Comentario(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    