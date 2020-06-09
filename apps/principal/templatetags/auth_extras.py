from django import template
from django.contrib.auth.models import Group
from apps.principal.models import Perfil, Coordinador, Musico

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
	group = Group.objects.get(name=group_name) 
	return True if group in user.groups.all() else False

@register.simple_tag
def usuarioFoto(usuario):
	num = usuario.id
	if str(usuario.groups.get()) == 'GE' or str(usuario.groups.get()) == 'SE' or str(usuario.groups.get()) == 'CB' or str(usuario.groups.get()) == 'CR':
		return Perfil.objects.get(usuario_id=num).foto.url
	elif str(usuario.groups.get()) == 'CN':
		return Coordinador.objects.get(usuario_id=num).foto.url
	elif str(usuario.groups.get()) == 'PR' or str(usuario.groups.get()) == 'ES':
		return Musico.objects.get(cedula=usuario.username).foto.url

@register.simple_tag
def usuarioNombre(usuario):
	num = usuario.id
	cadena = "{0} {1}"
	if str(usuario.groups.get()) == 'GE' or str(usuario.groups.get()) == 'SE' or str(usuario.groups.get()) == 'CB' or str(usuario.groups.get()) == 'CR':
		return cadena.format(Perfil.objects.get(usuario_id=num).nombre, Perfil.objects.get(usuario_id=num).apellido)
	elif str(usuario.groups.get()) == 'CN':
		return cadena.format(Coordinador.objects.get(usuario_id=num).nombre, Coordinador.objects.get(usuario_id=num).apellido)
	elif str(usuario.groups.get()) == 'PR' or str(usuario.groups.get()) == 'ES':
		return cadena.format(Musico.objects.get(cedula=usuario.username).nombre, Musico.objects.get(cedula=usuario.username).apellido)

@register.filter(name='addvalue')
def addvalue(value, arg):
    return value.as_widget(attrs={'value': arg})

@register.filter(name='addplaceholder')
def addplaceholder(value, arg):
    return value.as_widget(attrs={'placeholder': arg})

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})