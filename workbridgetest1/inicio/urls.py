# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('Usuarios/logout', views.loginsalir),
    path('indexA/', views.admin_dashboard, name='admin_dashboard'),    
    path('empresa_dashboard/', views.empresa_dashboard, name='empresa_dashboard'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('perfil/', views.perfil, name='perfil'),

]
