from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text','placeholder': 'Usuario','id': 'log-form-user','class': 'validate'}))
	password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password','placeholder': 'Contraseña','id': 'log-form-password','class': 'validate'}))

OPCIONES = [('S','Si'),('N','No')]

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