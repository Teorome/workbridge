from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate
from .models import User,Profile
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.utils.translation import gettext_lazy as _

class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=[('empresa', 'Empresa')], label=_('Rol'))
    genero = forms.ChoiceField(
        choices=[('', 'Ninguno'), ('M', 'Masculino'), ('F', 'Femenino')],
        label=_('Género'),
        required=False,  
        initial=''  
    )

    class Meta:
        model = User
        fields = ['rol', 'nombres', 'apellidos', 'correo', 'telefono', 'genero', 'direccion', 'password1', 'password2']
        labels = {
            'nombres': _('Nombres'),
            'apellidos': _('Cargo'),  
            'correo': _('Correo electrónico'),
            'telefono': _('Teléfono'),
            'direccion': _('Dirección'),
        }
        error_messages = {
            'correo': {
                'unique': _("Ya existe un usuario con este correo."),
            },
            'password1': {
                'password_too_short': _("Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres."),
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Las contraseñas no coinciden"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class LoginForm(AuthenticationForm):
    correo = forms.EmailField(label=_("Correo electrónico"), widget=forms.EmailInput(attrs={'autofocus': True}))

    class Meta:
        fields = ['correo', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = self.fields['correo'].widget
        del self.fields['correo']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password) 
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Usuario o contraseña inválidos."),
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    


class ProfileForm(forms.ModelForm):
    fecha_de_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'fecha_de_nacimiento',
            'direccion_sede',
            'telefono_empresa',
            'telefono_empresa2',
            'numero_identificacion_fiscal',
            'tipo_empresa',
            'sector_empresa',
            'numero_empleados',
            'descripcion_empresa'
        ]

    def clean_fecha_de_nacimiento(self):
        fecha_de_nacimiento = self.cleaned_data.get('fecha_de_nacimiento')
        if fecha_de_nacimiento and fecha_de_nacimiento > date.today():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')
        return fecha_de_nacimiento

    def clean_telefono_empresa(self):
        telefono_empresa = self.cleaned_data.get('telefono_empresa')
        if telefono_empresa and not re.match(r'^\+?1?\d{5,15}$', telefono_empresa):
            raise ValidationError('El número de teléfono debe ser válido. Debe contener entre 9 y 15 dígitos.')
        return telefono_empresa

    def clean_telefono_empresa2(self):
        telefono_empresa2 = self.cleaned_data.get('telefono_empresa2')
        if telefono_empresa2 and not re.match(r'^\+?1?\d{5,15}$', telefono_empresa2):
            raise ValidationError('El número de teléfono debe ser válido. Debe contener entre 9 y 15 dígitos.')
        return telefono_empresa2

    def clean_numero_identificacion_fiscal(self):
        numero_identificacion_fiscal = self.cleaned_data.get('numero_identificacion_fiscal')
        if numero_identificacion_fiscal and not re.match(r'^[A-Z0-9]+$', numero_identificacion_fiscal):
            raise ValidationError('El número de identificación fiscal solo puede contener letras mayúsculas y números.')
        return numero_identificacion_fiscal

    def clean_numero_empleados(self):
        numero_empleados = self.cleaned_data.get('numero_empleados')
        if numero_empleados and (numero_empleados < 0 or numero_empleados > 100000):
            raise ValidationError('El número de empleados debe estar entre 0 y 100000.')
        return numero_empleados

    def clean(self):
        cleaned_data = super().clean()
        direccion_sede = cleaned_data.get('direccion_sede')
        telefono_empresa = cleaned_data.get('telefono_empresa')
        numero_identificacion_fiscal = cleaned_data.get('numero_identificacion_fiscal')

        # Validación condicional: Si uno de los campos de empresa está presente, todos deben estar presentes.
        if any([direccion_sede, telefono_empresa, numero_identificacion_fiscal]):
            if not all([direccion_sede, telefono_empresa, numero_identificacion_fiscal]):
                raise ValidationError('Todos los campos relacionados con la empresa deben ser completados.')

        return cleaned_data