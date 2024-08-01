from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_empresa = models.BooleanField('Is empresa', default=False)
    nombres = models.CharField('Nombres', max_length=50,default='')
    apellidos = models.CharField('Apellidos', max_length=50, default='')
    correo = models.EmailField('Correo', unique=True, default='')
    telefono = models.CharField('Teléfono', max_length=15,default='')
    genero = models.CharField('Género', max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], default='')
    direccion = models.CharField('Dirección', max_length=255,default='')
    
    username = models.CharField(max_length=150, unique=True, default=uuid.uuid4)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username', 'nombres', 'apellidos']

    def __str__(self):
        return self.correo



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
   
    fecha_de_nacimiento = models.DateField('Fecha de nacimiento', blank=True, null=True)
    direccion_sede = models.CharField('Dirección de la Sede', max_length=255, blank=True, null=True)
    telefono_empresa = models.CharField('Teléfono de la Empresa', max_length=15, blank=True, null=True)
    telefono_empresa2 = models.CharField('Teléfono de la Empresa', max_length=15, blank=True, null=True)
    numero_identificacion_fiscal = models.CharField('Número de Identificación Fiscal', max_length=50, blank=True, null=True)
    tipo_empresa = models.CharField('Tipo de Empresa', max_length=100, blank=True, null=True)
    sector_empresa = models.CharField('Sector de la Empresa', max_length=100, blank=True, null=True)
    numero_empleados = models.IntegerField('Número de Empleados', blank=True, null=True)
    descripcion_empresa = models.TextField('Descripción de la Empresa', blank=True, null=True)

    def __str__(self):
        return self.user.correo
