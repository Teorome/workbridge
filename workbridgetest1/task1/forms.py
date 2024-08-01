from django import forms
from .models import Proyecto, Comentario

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'nom_proyecto', 'nom_aprendiz', 'descripcion', 'fecha', 'telefono', 'contacto', 
            'categoria', 'tiempo_desarrollo', 'tecnologias', 'colaboradores', 
            'imagen', 'imagen1', 'imagen2', 'imagen3', 'imagen4'
        ]

        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario aquí...', 'rows': 3}),
        }