from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from betterforms.multiform import MultiModelForm

from axes.utils import reset as logReset

from . import models

import random

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text','placeholder': 'Usuario','id': 'log-form-user','class': 'validate','autofocus': 'true'}))
	password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password','placeholder': 'Contraseña','id': 'log-form-password','class': 'validate'}))

class SolicitudBienForm(forms.ModelForm):
	class Meta:
		model = models.SolicitudBien
		fields = ['nucleo', 'mensaje']
		labels = {
			'nucleo': '',
			'mensaje': 'mensaje'
		}
		widgets = {
			'nucleo': forms.RadioSelect(attrs={'style': 'display: none'}),
			'mensaje': forms.TextInput(attrs={'placeholder': 'Mensaje'})
		}

class SolicitudInstrumentoForm(forms.ModelForm):
	class Meta:
		model = models.SolicitudInstrumento
		fields = ['nucleo', 'mensaje']
		labels = {
			'nucleo': '',
			'mensaje': 'mensaje'
		}
		widgets = {
			'nucleo': forms.RadioSelect(attrs={'style': 'display: none'}),
			'mensaje': forms.TextInput(attrs={'placeholder': 'Mensaje'})
		}

class AgregarBienForm(forms.ModelForm):
	class Meta:
		model = models.Bien
		fields = ['codigo','nombre','marca','nucleo','caracteristicas']
		labels = {
			'codigo': 'Codigo',
			'nombre': 'Tipo de Bien',
			'marca': 'Marca',
			'nucleo': '',
			'caracteristicas': 'Caracteristicas'
		}
		widgets = {
			'codigo': forms.NumberInput(attrs={'placeholder': 'Codigo'}),
			'nombre': forms.Select(),
			'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
			'nucleo': forms.Select(attrs={'style': 'display: none'}),
			'caracteristicas': forms.Textarea(attrs={'class': 'materialize-textarea'})
		}

class AgregarInstrumentoForm(forms.ModelForm):
	class Meta:
		model = models.Instrumento
		fields = ['codigo','nombre','marca','nucleo','caracteristicas']
		labels = {
			'codigo': 'Codigo',
			'nombre': 'Tipo de Instrumento',
			'marca': 'Marca',
			'nucleo': '',
			'caracteristicas': 'Caracteristicas'
		}
		widgets = {
			'codigo': forms.NumberInput(attrs={'placeholder': 'Codigo'}),
			'nombre': forms.Select(),
			'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
			'nucleo': forms.Select(attrs={'style': 'display: none'}),
			'caracteristicas': forms.Textarea(attrs={'class': 'materialize-textarea'})
		}

class AgregarMusicoForm(forms.ModelForm):
	class Meta:
		model = models.Musico
		fields = ['cedula','nombre','apellido','telefono','direccion','email','fecha','fecha_ing','sexo','tipo','catedra','nucleo']
		widgets = {
			'cedula': forms.NumberInput(attrs={'placeholder': 'Cedula'}),
			'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
			'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
			'telefono': forms.NumberInput(attrs={'placeholder': 'Telefono'}),
			'direccion': forms.Textarea(attrs={'placeholder': 'Direccion','class': 'materialize-textarea'}),
			'email': forms.EmailInput(attrs={'placeholder': 'Correo'}),
			'fecha': forms.DateInput(attrs={'type': 'date'}),
			'fecha_ing': forms.DateInput(attrs={'type': 'date'}),
			'sexo': forms.Select(),
			'tipo': forms.Select(attrs={'style': 'display: none'}),
			'catedra': forms.Select(),
			'nucleo': forms.Select(),
		}

class AgregarAsignacionForm(forms.ModelForm):
	class Meta:
		model = models.Asignacion
		fields = ['musico','instrumento','fecha_ini']
		widgets = {
			'musico': forms.Select(),
			'instrumento': forms.Select(),
			'fecha_ini': forms.DateInput(attrs={'type': 'date', 'accept': 'image/*'})
		}

class AgregarPagoForm(forms.ModelForm):
	class Meta:
		model = models.Pago
		fields = ['asignacion','fecha','imagen']
		widgets = {
			'asignacion': forms.Select(),
			'fecha': forms.DateInput(attrs={'type': 'date'}),
			'imagen': forms.FileInput()
		}

class AgregarPartituraForm(forms.ModelForm):
	class Meta:
		model = models.Partitura
		fields = ['nombre','autor','voz','tonalidad','media']
		widgets = {
			'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
			'autor': forms.Select(),
			'voz': forms.Select(),
			'tonalidad': forms.Select(),
			'media': forms.FileInput(attrs={'accept': 'application/pdf'})
		}

class GaleriaForm(forms.ModelForm):
	class Meta:
		model = models.Galeria
		fields = ['imagen','descripcion','fecha','visible']
		labels = {
			'imagen': '',
			'descripcion': 'Descripción',
			'fecha': 'Fecha',
			'visible': 'Visible'
		}
		widgets = {
			'imagen': forms.FileInput(attrs={'style': 'display: none;','onchange': 'openFile(event);'}),
			'descripcion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
			'fecha': forms.DateInput(attrs={'type': 'date'}),
			'visible': forms.RadioSelect()
		}

class RecuperarForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'type': 'text',
		'placeholder': 'Usuario',
		'id': 'log-form-user',
		'class': 'validate',
	}))

	def send_mail(self,correo):
		usuario = User.objects.get(username=self.cleaned_data['username'])
		registros = models.RecuperarPassword.objects.filter(usuario_id=usuario.id)
		if len(registros) > 0:
			for registro in registros:
				r = registro
				r.delete()
		username = usuario.username
		if len(username) == 7:
			username = "0" + username
		codigo = ""
		i = 0
		b = 0
		for x in range(1,50):
			if i == 1 or i == 5 or i == 9 or i == 13 or i == 17 or i == 21 or i == 25 or i == 29:
				codigo += username[b]
				b += 1
			else:
				a = random.randint(0,2)
				if a == 1:
					codigo += str(random.randint(0,9))
				else:
					cadena = "aabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
					codigo += cadena[random.randint(0,52)]
			i += 1
		models.RecuperarPassword.objects.create(
			usuario=usuario,
			codigo=codigo
		)
		email = EmailMessage(
			'Recuperar contraseña - SGAMP',
			'Para recuperar su contraseña ingrese al siguiente enlace http://sgamp.pythonanywhere.com/recuperar/%s/' %(codigo),
			to=[correo]
		)
		email.send()

class RecuperarCodigoForm(forms.Form):
	password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password','placeholder': 'Nueva contraseña','id': 'log-form-password','class': 'validate'}))
	password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password','placeholder': 'Ingrese nuevamente','id': 'log-form-password-2','class': 'validate'}))

	def cambiarPassword(self,username,codigo):
		usuario = User.objects.get(username=username)
		usuario.set_password(self.cleaned_data['password'])
		usuario.save()
		logReset(username=username)
		registro = models.RecuperarPassword.objects.get(codigo=codigo)
		registro.delete()