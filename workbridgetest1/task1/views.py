from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from task1.models import Proyecto
from .forms import  ProyectoForm, ComentarioForm
from .models import Proyecto
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import View
from .models import Comentario
from .decorators import admin_required, empresa_required



TEMPLACE_DIRS = (
    'os_path.join(BASE_DIR,"templates"),'
)
 

@login_required
def proyectoinsertar(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('indexA')
    else:
        form = ProyectoForm()
    return render(request, 'interfaz_admin/home/creacion.html', {'form': form})

@login_required
def actualizarproyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('indexA')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'interfaz_admin/home/actualizar.html', {'form': form})

@login_required
def borrarproyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('indexA')
    return render(request, 'interfaz_admin/home/eliminar.html', {'proyecto': proyecto})

def inicio(request):
    return render(request, 'interfaz_inicio/home/inicio.html')

@login_required
def indexA(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'interfaz_admin/home/indexA.html', {'proyectos': proyectos})

@login_required
def indexE(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'interfaz_empresa/home/indexE.html', {'proyectos': proyectos})

@login_required
def inicioE(request):
    return render(request, 'interfaz_empresa/home/inicioE.html')

def indexU(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'interfaz_inicio/home/indexU.html', {'proyectos': proyectos})


@login_required
@empresa_required
def comentarios_proyectoE(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    comentarios = Comentario.objects.filter(proyecto=proyecto).order_by('-fecha')
    
    if request.method == "POST" and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.proyecto = proyecto
            comentario.usuario = request.user
            comentario.save()
            return redirect('comentariosE', proyecto_id=proyecto.id_proyecto)  # Redireccionar para evitar duplicados
    else:
        form = ComentarioForm()
    
    context = {
        'proyecto': proyecto,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'interfaz_empresa/home/comentariosE.html', context)

@login_required
@empresa_required
def comentarios_proyectoA(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    comentariosA = Comentario.objects.filter(proyecto=proyecto).order_by('-fecha')
    
    if request.method == "POST" and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.proyecto = proyecto
            comentario.usuario = request.user
            comentario.save()
            return redirect('comentariosA', proyecto_id=proyecto.id_proyecto)  # Redireccionar para evitar duplicados
    else:
        form = ComentarioForm()
    
    context = {
        'proyecto': proyecto,
        'comentarios': comentariosA,
        'form': form,
    }
    return render(request, 'interfaz_admin/home/comentariosA.html', context)


def comentarios_proyectoU(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    comentariosU = Comentario.objects.filter(proyecto=proyecto).order_by('-fecha')
    
    context = {
        'proyecto': proyecto,
        'comentarios': comentariosU,
    }
    
    return render(request, 'interfaz_inicio/home/comentariosU.html', context)


"""
def guardar_comentario(request, id_proyecto):
    if request.method == 'POST':
        comentario_texto = request.POST.get('comentario')
        proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
        comentario_user = User.objects.get(username='Empresa')
        nuevo_comentario = Comentario(proyecto=proyecto, texto=comentario_texto, autor=comentario_user)
        nuevo_comentario.save()
        return redirect('comentarios', id_proyecto=id_proyecto)


"""

"""
class addcomment(View):
    def post(self, request, *args, **kwargs):
        nombre_autor = request.POST.get('nombre_autor')
        texto = request.POST.get('texto')
        proyecto_id = kwargs['proyecto_id']  
        comentario = Comentario(nombre_autor=nombre_autor, texto=texto, proyecto_id=proyecto_id)
        comentario.save()
        return redirect('comentarios', proyecto_id=proyecto_id)

"""



