from django.contrib import admin
from django.urls import path, include
from django import views
from . import views
from task1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio, name='inicio'),
    path('creacion/', views.proyectoinsertar, name='creacion'),
    path('indexA/', views.indexA, name='indexA'),
    path('indexE/', views.indexE, name='indexE'),
    path('indexU/', views.indexU, name='indexU'),
    path('inicioE/', views.inicioE, name='inicioE'),
    path('proyectos/actualizar/<int:id>/', views.actualizarproyecto, name='actualizar'),
    path('proyectos/eliminar/<int:id>/', views.borrarproyecto, name='borrar'),
    path('comentariosA/<int:proyecto_id>/', views.comentarios_proyectoA, name='comentariosA'),
    path('comentariosE/<int:proyecto_id>/', views.comentarios_proyectoE, name='comentariosE'),  
    path('comentariosU/<int:proyecto_id>/', views.comentarios_proyectoU, name='comentariosU'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)