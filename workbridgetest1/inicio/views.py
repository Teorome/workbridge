from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, empresa_required
from .forms import RegistroForm, LoginForm,ProfileForm
from django.views.decorators.cache import never_cache
from .models import User,Profile
import uuid


#Login-Registro
@never_cache
@login_required
def logout_view(request):
    logout(request)
    response = redirect('login') 
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            rol = form.cleaned_data['rol']

            if rol == 'empresa':
                user.is_empresa = True
            elif rol == 'admin':
                user.is_admin = True

            user.username = str(uuid.uuid4())
            user.save()
            messages.success(request, "Registrado.")
            return redirect('login')
        else:
            messages.error(request, "Problemas en el registro.")
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
               
                if user.is_admin:
                    request.session['rol_usuario'] = 'Admin'
                    return redirect('admin_dashboard')
                elif user.is_empresa:
                    request.session['rol_usuario'] = 'Empresa'
                    return redirect('empresa_dashboard')
                else:
                    request.session['rol_usuario'] = 'Usuario' 
            else:
                messages.error(request, "Usuario o contraseña invalido.")
        else:
            messages.error(request, "Se proporcionaron datos de inicio de sesión no válidos.")

    return render(request, 'accounts/login.html', {'form': form})

@never_cache
@admin_required
def admin_dashboard(request):
    return render(request, 'task1/templates/interfaz_admin/home/indexA.html')


@never_cache
@empresa_required
def empresa_dashboard(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'accounts/empresa_dashboard.html', {'user': user, 'profile': profile})

@login_required
def editar_perfil(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      
        profile = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('empresa_dashboard')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/editar_perfil.html', {'form': form})

@admin_required
@login_required
def perfil(request):
    user = request.user
    return render(request, 'accounts/perfil.html', {'user': user})



#Crud usuarios/registro

@login_required
@admin_required
def user_list(request):
    users = User.objects.all() 
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@admin_required
def user_create(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            rol = form.cleaned_data['rol']

            if rol == 'admin':
                user.is_admin = True
            elif rol == 'empresa':
                user.is_empresa = True

            user.username = str(uuid.uuid4())
            user.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('user_list')
        else:
            messages.error(request, 'Error en la creación del usuario.')
    else:
        form = RegistroForm()
    return render(request, 'users/user_form.html', {'form': form})

@login_required
@admin_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('user_list')
        else:
            messages.error(request, 'Error en la actualización del usuario.')
    else:
        form = RegistroForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

@login_required
@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


def loginsalir(request):
    logout(request)
    return redirect('/login')