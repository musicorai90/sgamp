from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.forms.utils import ErrorList
from django.http import JsonResponse
from django.db.models import Q

from django import forms as FormsModule

from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .mixins import GroupRequiredMixin, ControlAccess, ControlAccess2, ControlAccess3, get_nucleo, get_group, get_user_manual

from . import models
from . import forms

from itertools import chain
from operator import attrgetter

class Index(generic.base.View):
	def get(self, request, *args, **kwargs):
		if str(request.user) is "AnonymousUser":
			return render(request, "index.html", {'galeria': models.Galeria.objects.all()})
		else:
			context = {
				'bienes': str(len(models.Bien.objects.all())),
				'instrumentos': str(len(models.Instrumento.objects.all())),
				'profesores': str(len(models.Musico.objects.filter(tipo="P"))),
				'alumnos': str(len(models.Musico.objects.filter(tipo="A"))),
				'asignaciones': str(len(models.Asignacion.objects.all())),
				'galeria': str(len(models.Galeria.objects.all()))
			}
			if get_group(self) == 'CR' or get_group(self) == 'PR' or get_group(self) == 'ES':
				partituras = models.Partitura.objects.all()[::-1]
				paginator = Paginator(partituras, 5)

				page_number = request.GET.get('page')
				page_obj = paginator.get_page(page_number)
				context['page_obj'] =  page_obj
				context['partituras'] =  partituras
			return render(request, "dashboard.html", context)

class Mensaje(generic.base.View):

	def post(self, request, *args, **kwargs):
		email = EmailMessage(
			request.POST['mensaje-asunto'],
			'%s \n %s' %(request.POST['mensaje-correo'], request.POST['mensaje-mensaje']),
			to=['raimong79@gmail.com']
		)
		email.send()
		messages.add_message(request, messages.INFO, "Se ha enviado el correo")
		return redirect('/')

class Login(LoginView):
	authentication_form = forms.LoginForm
	form_class = forms.LoginForm
	template_name = "login.html"
	redirect_authenticated_user = "index"

	def form_valid(self, form):
		login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)

class Logout(generic.base.View):
	def get(self,request, *args, **kwargs):
		logout(request)
		return redirect('principal:index')

class Nosotros(generic.base.TemplateView):
	template_name = "nosotros.html"

class Perfil(generic.base.TemplateView):
	template_name = "perfil.html"

	def get_context_data(self, **kwargs):
		context = super(Perfil, self).get_context_data(**kwargs)
		context['usuario'] = get_user_manual(self)
		return context

	def post(self, request, *args, **kwargs):
		num = request.user.id
		usuario = get_user_manual(self)
		usuario.foto = request.FILES['new-img']
		usuario.save()
		return redirect('/perfil/')

class CambiarPass(LoginRequiredMixin, generic.edit.FormView):
	template_name = "cambiar_pass.html"
	form_class = forms.CambiarPassForm
	success_url = '/'
	success_message = "Se ha cambiardo la contraseña"

	def form_valid(self, form):
		a = self.request.user
		if a.check_password(self.request.POST['password']):
			a.set_password(self.request.POST['password2'])
			a.save()
		else:
			messages.add_message(self.request, messages.INFO, "La contraseña actual es incorrecta")
			self.success_url = '/cambiar/'
		return super().form_valid(form)

class ModificarPerfil(LoginRequiredMixin, generic.edit.FormView):
	template_name = "modificarPerfil.html"
	form_class = forms.ModificarPerfilForm
	success_url = '/perfil/'

	def form_valid(self, form):
		usuario = get_user_manual(self)
		usuario.nombre = self.request.POST['nombre']
		usuario.apellido = self.request.POST['apellido']
		usuario.telefono = self.request.POST['telefono']
		usuario.direccion = self.request.POST['direccion']
		usuario.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(ModificarPerfil, self).get_context_data(**kwargs)
		context['usuario'] = get_user_manual(self)
		return context

class AgregarBien(generic.base.TemplateView):
	template_name = "agregarBien.html"

class Solicitudes(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE', u'CN', u'SE']
	template_name = "solicitudes.html"
	paginate_by = 5

	def get_queryset(self):
		bienes = models.SolicitudBien.objects.all()
		instrumentos = models.SolicitudInstrumento.objects.all()
		if get_group(self) == "CN":
			nucleo = get_nucleo(self)
			bienes = models.SolicitudBien.objects.filter(nucleo_id=nucleo)
			instrumentos = models.SolicitudInstrumento.objects.filter(nucleo_id=nucleo)
		elif get_group(self) == "SE":
			bienes = models.SolicitudBien.objects.filter(status="A")
			bieall = models.SolicitudBien.objects.all()
			for bien in bieall:
				if bien.status == 'L':
					bienes |= models.SolicitudBien.objects.filter(id=bien.id)
			instrumentos = models.SolicitudInstrumento.objects.filter(status="A")
			insall = models.SolicitudInstrumento.objects.all()
			for instrumento in insall:
				if instrumento.status == 'L':
					instrumentos |= models.SolicitudInstrumento.objects.filter(id=instrumento.id)
		result = sorted(chain(bienes,instrumentos), key=attrgetter('fecha'))
		queryset = result[::-1]
		return queryset

class AgregarSolicitudBien(LoginRequiredMixin, GroupRequiredMixin, generic.edit.CreateView):
	group_required = [u'CN']
	model = models.SolicitudBien
	template_name = "agregar_solicitud.html"
	form_class = forms.SolicitudBienForm

	def get_context_data(self, **kwargs):
		context = super(AgregarSolicitudBien, self).get_context_data(**kwargs)
		context['bienes'] = models.TipoBien.objects.all()
		nucleo = get_nucleo(self)
		context['nucleo'] = nucleo
		return context

	def form_valid(self, form):
		self.object = form.save()
		cantidad = int((len(self.request.POST) - 3) / 2)
		for x in range(0,cantidad):
			try:
				bien = models.TipoBien.objects.get(id=int(self.request.POST['bien%d' %(x+1)]))
			except:
				bien = models.TipoBien.objects.create(nombre=self.request.POST['bien-nuevo-%d' %(x+1)]) 
			models.SolicitudTipoBien.objects.create(
				solicitud = self.object,
				bien = bien,
				cantidad_solicitada = self.request.POST['cantidad%d' %(x+1)]
			)
		return redirect('principal:solicitudes')

class AgregarSolicitudInstrumento(LoginRequiredMixin, GroupRequiredMixin, generic.edit.CreateView):
	group_required = [u'CN']
	model = models.SolicitudInstrumento
	template_name = "agregar_solicitud.html"
	form_class = forms.SolicitudInstrumentoForm

	def get_context_data(self, **kwargs):
		context = super(AgregarSolicitudInstrumento, self).get_context_data(**kwargs)
		context['bienes'] = models.TipoInstrumento.objects.all()
		nucleo = get_nucleo(self)
		context['nucleo'] = nucleo
		return context

	def form_valid(self, form):
		self.object = form.save()
		cantidad = int((len(self.request.POST) - 3) / 2)
		for x in range(0,cantidad):
			try:
				bien = models.TipoInstrumento.objects.get(id=int(self.request.POST['bien%d' %(x+1)]))
			except:
				bien = models.TipoInstrumento.objects.create(nombre=self.request.POST['bien-nuevo-%d' %(x+1)]) 
			models.SolicitudTipoInstrumento.objects.create(
				solicitud = self.object,
				bien = bien,
				cantidad_solicitada = self.request.POST['cantidad%d' %(x+1)]
			)
		return redirect('principal:solicitudes')

class SolicitudBien(LoginRequiredMixin, GroupRequiredMixin, ControlAccess, generic.edit.UpdateView):
	group_required = [u'GE', u'CN', u'SE']
	model = models.SolicitudBien
	fields = ['status']
	template_name = "solicitud.html"

	def get_context_data(self, **kwargs):
		context = super(SolicitudBien, self).get_context_data(**kwargs)
		tipos = models.SolicitudTipoBien.objects.filter(solicitud_id=self.object.id)
		context['bienes'] = tipos
		context['bieall'] = models.Bien.objects.all()
		cantidades = []
		for tipo in tipos:
			num = len(models.Bien.objects.filter(~Q(nucleo_id=self.object.nucleo.id),nombre_id=tipo.bien.id,status='DI'))
			cantidades.append({'id': tipo.id, 'cantidad': num})
		context['cantidades'] = cantidades
		return context

	def form_valid(self, form):
		self.object = form.save()
		if get_group(self) == 'GE':
			for bien in models.SolicitudTipoBien.objects.filter(solicitud_id=self.object.id):
				bien.cantidad_aprobada = self.request.POST.get('ctd%i' %(bien.id))
				if int(self.request.POST.get('ctd%i' %(bien.id))) > int(bien.cantidad_solicitada):
					messages.add_message(self.request, messages.INFO, 'Hay cantiades mayores a las solicitadas')
					return redirect('/solicitudes/bienes/%d/' %(self.object.id))
				bien.save()
		elif get_group(self) == 'CN':
			bienes = self.request.POST.getlist('bienes')
			nucleo = models.Nucleo.objects.get(id=int(self.object.nucleo_id))
			for bien in bienes:
				elem = models.Bien.objects.get(id=int(bien))
				elem.nucleo = nucleo
				elem.save()
		return super().form_valid(form)

class SolicitudInstrumento(LoginRequiredMixin, GroupRequiredMixin, ControlAccess, generic.edit.UpdateView):
	group_required = [u'GE', u'CN']
	model = models.SolicitudInstrumento
	fields = ['status']
	template_name = "solicitud.html"

	def get_context_data(self, **kwargs):
		context = super(SolicitudInstrumento, self).get_context_data(**kwargs)
		tipos = models.SolicitudTipoInstrumento.objects.filter(solicitud_id=self.object.id)
		context['bienes'] = tipos
		context['bieall'] = models.Instrumento.objects.all()
		cantidades = []
		for tipo in tipos:
			num = len(models.Instrumento.objects.filter(nombre_id=tipo.instrumento.id,status='DI'))
			cantidades.append({'id': tipo.id, 'cantidad': num})
		context['cantidades'] = cantidades
		return context

	def form_valid(self, form):
		self.object = form.save()
		if get_group(self) == 'GE':
			for instrumento in models.SolicitudTipoInstrumento.objects.filter(solicitud_id=self.object.id):
				instrumento.cantidad_aprobada = self.request.POST.get('ctd%i' %(instrumento.id))
				if int(self.request.POST.get('ctd%i' %(instrumento.id))) > int(instrumento.cantidad_solicitada):
					messages.add_message(self.request, messages.INFO, 'Hay cantiades mayores a las solicitadas')
					return redirect('/solicitudes/instrumentos/%d/' %(self.object.id))
				instrumento.save()
		elif get_group(self) == 'CN':
			instrumentos = self.request.POST.getlist('bienes')
			nucleo = models.Nucleo.objects.get(id=int(self.object.nucleo_id))
			for instrumento in instrumentos:
				elem = models.Instrumento.objects.get(id=int(instrumento))
				elem.nucleo = nucleo
				elem.save()
		return super().form_valid(form)

class Bien(LoginRequiredMixin, GroupRequiredMixin, ControlAccess3, generic.DetailView):
	group_required = [u'GE', u'CN', u'SE']
	model = models.Bien
	template_name = "bien.html"

class BienDesincorporar(View, GroupRequiredMixin, LoginRequiredMixin):
	group_required = [u'CN']

	def post(self, request, *args, **kwargs):
		bien_id = int(request.POST['id'])
		bien = models.Bien.objects.get(id=bien_id)
		mensaje = str(request.POST['mensaje']) 
		models.BienDesincorporado.objects.create(nombre=bien,mensaje=mensaje)	
		return redirect('/')

class Bienes(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE', u'CN', u'SE']
	paginate_by = 5
	template_name = "bienes.html"
	ordering = ['-id']

	def get_queryset(self):
		bienes = models.Bien.objects.all()[::-1]
		if get_group(self) == 'CN':
			nucleo = get_nucleo(self)
			bienes = models.Bien.objects.filter(nucleo_id=nucleo)[::-1]
		return bienes

class AgregarBien(LoginRequiredMixin, GroupRequiredMixin, generic.edit.CreateView):
	group_required = [u'SE']
	template_name = "agregar_bien.html"
	model = models.Bien
	form_class = forms.AgregarBienForm

	def form_valid(self, form):
		self.object = form.save()
		if self.request.POST['nuevo'] == "1":
			tipo = models.TipoBien.objects.create(nombre=self.request.POST['new-bien'])
			self.object.nombre = tipo
			self.object.save()
		return super(AgregarBien, self).form_valid(form)

class Instrumentos(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'CN',u'SE',u'CB']
	paginate_by = 5
	template_name = "instrumentos.html"
	ordering = ['-id']

	def get_queryset(self):
		bienes = models.Instrumento.objects.all()[::-1]
		if get_group(self) == 'CN':
			nucleo = get_nucleo(self)
			bienes = models.Instrumento.objects.filter(nucleo_id=int(nucleo))
		return bienes

class Instrumento(LoginRequiredMixin, GroupRequiredMixin, ControlAccess3, generic.DetailView):
	group_required = [u'GE', u'CN', u'SE',u'CB']
	model = models.Instrumento
	template_name = "instrumento.html"

class AgregarInstrumento(LoginRequiredMixin, GroupRequiredMixin, generic.edit.CreateView):
	group_required = [u'SE']
	template_name = "agregar_instrumento.html"
	model = models.Instrumento
	form_class = forms.AgregarInstrumentoForm

	def form_valid(self, form):
		self.object = form.save()
		if self.request.POST['nuevo'] == "1":
			tipo = models.TipoInstrumento.objects.create(nombre=self.request.POST['new-bien'])
			self.object.nombre = tipo
			self.object.save()
		return super(AgregarInstrumento, self).form_valid(form)

class InstrumentoDesincorporar(View, GroupRequiredMixin, LoginRequiredMixin):
	group_required = [u'CN']

	def post(self, request, *args, **kwargs):
		instrumento_id = int(request.POST['id'])
		instrumento = models.Instrumento.objects.get(id=instrumento_id)
		mensaje = str(request.POST['mensaje']) 
		models.InstrumentoDesincorporado.objects.create(nombre=instrumento,mensaje=mensaje)	
		return redirect('/')

class Profesores(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'CN',u'SE']
	template_name = "profesores.html"
	paginate_by = 5
	ordering = ['-id']

	def get_queryset(self):
		profesores = models.Musico.objects.filter(tipo="P")
		if get_group(self) == 'CN':
			nucleo = get_nucleo(self)
			profesores = models.Musico.objects.filter(tipo="P",nucleo_id=nucleo)
		return profesores

class AgregarProfesor(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'SE']
	template_name = "agregar_profesor.html"
	model = models.Musico
	form_class = forms.AgregarMusicoForm

	def form_valid(self, form):
		self.object = form.save()
		user = User.objects.create_user(self.request.POST['cedula'],email=self.request.POST['email'],password=self.request.POST['cedula'])
		user.groups.set('6')
		return super(AgregarProfesor, self).form_valid(form)

class Profesor(LoginRequiredMixin, GroupRequiredMixin, ControlAccess3, generic.DetailView):
	group_required = [u'GE',u'CN',u'SE']
	model = models.Musico
	template_name = "profesor.html"

class Alumnos(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'CN',u'SE']
	template_name = "alumnos.html"
	paginate_by = 5
	ordering = ['-id']

	def get_queryset(self):
		profesores = models.Musico.objects.filter(tipo="A")
		if get_group(self) == 'CN':
			nucleo = get_nucleo(self)
			profesores = models.Musico.objects.filter(tipo="A",nucleo_id=nucleo)
		return profesores

class AgregarAlumno(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'SE']
	template_name = "agregar_alumno.html"
	model = models.Musico
	form_class = forms.AgregarMusicoForm

	def form_valid(self, form):
		print("Hola")
		self.object = form.save()
		user = User.objects.create_user(self.request.POST['cedula'],email=self.request.POST['email'],password=self.request.POST['cedula'])
		user.groups.set('7')
		return super(AgregarAlumno, self).form_valid(form)

class Alumno(LoginRequiredMixin, GroupRequiredMixin, ControlAccess3, generic.DetailView):
	group_required = [u'GE',u'CN',u'SE']
	model = models.Musico
	template_name = "alumno.html"

	def get_context_data(self, **kwargs):
		context = super(Alumno, self).get_context_data(**kwargs)
		lista = models.AlumnoRepresentante.objects.all()
		representante = ""
		for elem in lista:
			if elem.musico.id == self.object.id:
				representante = "%s %s" %(elem.representante.nombre, elem.representante.apellido)
		context['representante'] = representante
		return context

class Asignaciones(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'CN',u'SE',u'CB']
	template_name = "asignaciones.html"
	paginate_by = 5
	ordering = ['-id']

	def get_queryset(self):
		asignaciones = models.Asignacion.objects.all()
		if get_group(self) == 'CN':
			asignaciones = models.Asignacion.objects.none()
			asiAll = models.Asignacion.objects.all()
			nucleo = get_nucleo(self)
			for asignacion in asiAll:
				if asignacion.musico.nucleo_id == nucleo:
					asignaciones |= models.Asignacion.objects.filter(id=asignacion.id)
		return asignaciones

class AgregarAsignacion(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'CB']
	form_class = forms.AgregarAsignacionForm
	model = models.Asignacion
	template_name = "agregar_asignacion.html"

class Galeria(LoginRequiredMixin, GroupRequiredMixin, generic.edit.CreateView):
	group_required = [u'GE']
	form_class = forms.GaleriaForm
	model = models.Galeria
	template_name = "galeria.html"

	def get_context_data(self, **kwargs):
		context = super(Galeria, self).get_context_data(**kwargs)
		context['fotos'] = models.Galeria.objects.all().order_by('-id')
		return context

class GaleriaVisible(View, GroupRequiredMixin, LoginRequiredMixin):
	group_required = [u'GE']

	def post(self, request, *args, **kwargs):
		fotos = request.POST.getlist('f-fotos')
		for i in models.Galeria.objects.all():
			i.visible = "N"
			i.save()
		for foto in fotos:
			elem = models.Galeria.objects.get(id=int(foto))
			elem.visible = "S"
			elem.save()
		return redirect('principal:galeria')

class Desincorporaciones(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'CN']
	template_name = "desincorporaciones.html"
	paginate_by = 5
	ordering = ['-id']

	def get_queryset(self):
		bienes = models.BienDesincorporado.objects.all()
		instrumentos = models.InstrumentoDesincorporado.objects.all()
		if get_group(self) == "CN":
			bieAll = models.BienDesincorporado.objects.all()
			insAll = models.InstrumentoDesincorporado.objects.all()
			bienes = models.BienDesincorporado.objects.none()
			instrumentos = models.InstrumentoDesincorporado.objects.none()
			nucleo = get_nucleo(self)
			for bien in bieAll:
				if bien.nombre.nucleo_id == nucleo:
					bienes |= models.BienDesincorporado.objects.filter(id=bien.id)
			for instrumento in insAll:
				if instrumento.nombre.nucleo_id == nucleo:
					instrumentos |= models.InstrumentoDesincorporado.objects.filter(id=instrumento.id)
		result = sorted(chain(bienes,instrumentos), key=attrgetter('fecha'))
		queryset = result[::-1]
		return queryset

class DesincorporacionBien(LoginRequiredMixin, GroupRequiredMixin, ControlAccess2, generic.edit.UpdateView):
	group_required = [u'GE',u'CN']
	model = models.BienDesincorporado
	fields = ['status']
	template_name = "desincorporacion.html"

	def form_valid(self, form):
		self.object = form.save()
		bien = models.Bien.objects.get(id=self.object.nombre_id)
		if self.object.status == "A":
			bien.status = "DE"
			bien.save()
		return super().form_valid(form)

class DesincorporacionInstrumento(LoginRequiredMixin, GroupRequiredMixin, ControlAccess2, generic.edit.UpdateView):
	group_required = [u'GE',u'CN']
	model = models.InstrumentoDesincorporado
	fields = ['status']
	template_name = "desincorporacion.html"

	def form_valid(self, form):
		self.object = form.save()
		instrumento = models.Instrumento.objects.get(id=self.object.nombre_id)
		if self.object.status == "A":
			instrumento.status = "DE"
			bien.save()
		return super().form_valid(form)

class SolicitudesBusqueda(View, GroupRequiredMixin):
	group_required = [u'GE',u'CN',u'SE']

	def post(self, request, *args, **kwargs):
		solicitudes = []
		bienes = list(models.SolicitudBien.objects.filter(id__icontains=request.POST['suId']).values())
		instrumentos = list(models.SolicitudInstrumento.objects.filter(id__icontains=request.POST['suId']).values())
		for bien in bienes:
			bien['nucleo'] = models.SolicitudBien.objects.get(id=bien['id']).nucleo.nombre
			solicitudes.append(bien)
		for instrumento in instrumentos:
			instrumento['nucleo'] = models.SolicitudInstrumento.objects.get(id=instrumento['id']).nucleo.nombre
			solicitudes.append(instrumento)
		return JsonResponse(solicitudes, safe=False)

class Busqueda(View):

	def post(self, request, *args, **kwargs):
		if request.POST['view'] == "bienes":
			busqueda = list(models.Bien.objects.filter(id__icontains=request.POST['suId']).values())
			for elem in busqueda:
				elem['nombre'] = models.Bien.objects.get(id=elem['id']).nombre.nombre
				elem['nucleo'] = models.Bien.objects.get(id=elem['id']).nucleo.nombre
		elif request.POST['view'] == "instrumentos":
			busqueda = list(models.Instrumento.objects.filter(id__icontains=request.POST['suId']).values())
			for elem in busqueda:
				elem['nombre'] = models.Instrumento.objects.get(id=elem['id']).nombre.nombre
				elem['nucleo'] = models.Instrumento.objects.get(id=elem['id']).nucleo.nombre
		elif request.POST['view'] == "profesores":
			musicos = list(models.Musico.objects.filter(cedula__icontains=request.POST['suId']).values())
			busqueda = []
			for musico in musicos:
				if musico['tipo'] == "P":
					busqueda.append(musico)
			for elem in busqueda:
				elem['catedra'] = models.Musico.objects.get(id=elem['id']).catedra.nombre
				elem['nucleo'] = models.Musico.objects.get(id=elem['id']).nucleo.nombre
		elif request.POST['view'] == "alumnos":
			musicos = list(models.Musico.objects.filter(cedula__icontains=request.POST['suId']).values())
			busqueda = []
			for musico in musicos:
				if musico['tipo'] == "A":
					busqueda.append(musico)
			for elem in busqueda:
				elem['catedra'] = models.Musico.objects.get(id=elem['id']).catedra.nombre
				elem['nucleo'] = models.Musico.objects.get(id=elem['id']).nucleo.nombre
		elif request.POST['view'] == "asignaciones":
			busqueda = list(models.Asignacion.objects.filter(id__icontains=request.POST['suId']).values())
			for elem in busqueda:
				elem['nucleo'] = models.Musico.objects.get(id=elem['id']).nucleo.nombre
				elem['nombre'] = models.Musico.objects.get(id=elem['id']).nombre
				elem['apellido'] = models.Musico.objects.get(id=elem['id']).apellido
		elif request.POST['view'] == "desincorporaciones":
			busqueda = []
			bienes = list(models.BienDesincorporado.objects.filter(id__icontains=request.POST['suId']).values())
			instrumentos = list(models.InstrumentoDesincorporado.objects.filter(id__icontains=request.POST['suId']).values())
			for bien in bienes:
				bien['nucleo'] = models.BienDesincorporado.objects.get(id=bien['id']).nombre.nucleo.nombre
				bien['nombre'] = models.BienDesincorporado.objects.get(id=bien['id']).nombre.nombre.nombre
				busqueda.append(bien)
			for instrumento in instrumentos:
				instrumento['nucleo'] = models.InstrumentoDesincorporado.objects.get(id=instrumento['id']).nombre.nucleo.nombre
				instrumento['nombre'] = models.InstrumentoDesincorporado.objects.get(id=instrumento['id']).nombre.nombre.nombre
				busqueda.append(instrumento)
		elif request.POST['view'] == "tipos_bienes":
			busqueda = list(models.TipoBien.objects.filter(id__icontains=request.POST['suId']).values())
		elif request.POST['view'] == "tipos_instrumentos":
			busqueda = list(models.TipoInstrumento.objects.filter(id__icontains=request.POST['suId']).values())
		elif request.POST['view'] == "pagos":
			busqueda = list(models.Pago.objects.filter(id__icontains=request.POST['suId']).values())
			for elem in busqueda:
				elem['asignacion'] = models.Pago.objects.get(id=elem['id']).asignacion.__str__()
				elem['url'] = models.Pago.objects.get(id=elem['id']).imagen.url
		elif request.POST['view'] == "partituras":
			busqueda = list(models.Partitura.objects.filter(id__icontains=request.POST['suId']).values())
			for elem in busqueda:
				elem['nombre'] = models.Partitura.objects.get(id=elem['id']).__str__()
				elem['usuario'] = models.Partitura.objects.get(id=elem['id']).usuario.username
				elem['url'] = models.Partitura.objects.get(id=elem['id']).media.url
		return JsonResponse(busqueda, safe=False)

class Recuperar(SuccessMessageMixin, generic.edit.FormView):
	template_name = "recuperar.html"
	form_class = forms.RecuperarForm
	success_url = '/'
	success_message = "Se ha enviado el correo"

	def form_valid(self, form):
		try:
			a = User.objects.get(username=self.request.POST['username'])
			form.send_mail(a.email)
			return super().form_valid(form)
		except:
			form._errors[FormsModule.forms.NON_FIELD_ERRORS] = ErrorList([u'El usuario no existe'])
			return super().form_invalid(form)

	def dispatch(self, request, *args, **kwargs):
		if str(request.user) is not "AnonymousUser":
			return redirect('principal:index')
		return super(Recuperar, self).dispatch(request, *args, **kwargs)

class RecuperarCodigo(generic.edit.FormView):
	template_name = "recuperar_codigo.html"
	form_class = forms.RecuperarCodigoForm
	success_url = "/login/"

	def form_valid(self, form, **kwargs):
		codigo = self.kwargs['codigo']
		username = ""
		i = 1
		if codigo[0] == "0":
			i = 5
		while i <= 29:
			username += codigo[i]
			i += 4
		form.cambiarPassword(username, codigo)
		return super().form_valid(form)

	def dispatch(self, *args, **kwargs):
		if str(self.request.user) is "AnonymousUser":
			return redirect('principal:index')
		try:
			a = models.RecuperarPassword.objects.get(codigo=self.kwargs['codigo'])
			return super().dispatch(*args, **kwargs)
		except:
			return redirect('principal:index')

class TipoBienes(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'SE']
	template_name = "tipos_bienes.html"
	paginate_by = 5
	ordering = ['-id']
	model = models.TipoBien

	def post(self, request, *args, **kwargs):
		models.TipoBien.objects.create(nombre=request.POST['nombre'])
		return redirect('principal:tipoBienes')

class TipoInstrumentos(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'SE']
	template_name = "tipos_instrumento.html"
	paginate_by = 5
	ordering = ['-id']
	model = models.TipoInstrumento

	def post(self, request, *args, **kwargs):
		models.TipoInstrumento.objects.create(nombre=request.POST['nombre'])
		return redirect('principal:tipoInstrumentos')

class Pagos(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'CB']
	template_name = "pagos.html"
	paginate_by = 5
	ordering = ['-id']
	model = models.Pago

class AgregarPago(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'CB']
	form_class = forms.AgregarPagoForm
	model = models.Pago
	template_name = "agregar_pago.html"

class AgregarPartitura(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'CR',u'PR']
	form_class = forms.AgregarPartituraForm
	model = models.Partitura
	template_name = "agregar_partitura.html"
	success_url = '/'

	def form_valid(self, form):
		partitura = form.save(commit=False)
		partitura.usuario = self.request.user
		partitura.save()
		return redirect('principal:index')

class AgregarAutor(View):
	
	def post(self, request, *args, **kwargs):
		autor = models.Autor.objects.create(nombre=request.POST['autor-nombre']).save()
		return redirect('principal:agregarPartitura')

class AgregarVoz(View):
	
	def post(self, request, *args, **kwargs):
		voz = models.Voz.objects.create(nombre=request.POST['voz-nombre']).save()
		return redirect('principal:agregarPartitura')

class Nucleo(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE',u'SE']
	template_name = "nucleos.html"
	model = models.Nucleo

	def get_context_data(self, **kwargs):
		context = super(Nucleo, self).get_context_data(**kwargs)
		coordinadores = models.Coordinador.objects.all()
		context['coordinadores'] = coordinadores
		nucleos = models.Nucleo.objects.all()
		indices = []
		for nucleo in nucleos:
			con = False
			for coordinador in coordinadores:
				if coordinador.nucleo == nucleo.id:
					con = True
			if not con:
				indices.append(nucleo.id)
		context['indices'] = indices
		return context

	def post(self, request, *args, **kwargs):
		nucleo = models.Nucleo.objects.create(nombre=request.POST['nombre']).save()
		return redirect('principal:nucleos')

class Coordinador(LoginRequiredMixin, GroupRequiredMixin, generic.DetailView):
	group_required = [u'GE',u'SE']
	template_name = "coordinador.html"
	model = models.Coordinador

	def post(self, request, *args, **kwargs):
		print('Hola1')
		self.object = self.get_object()
		print('Hola2')
		cedula = self.object.usuario.username
		print('Hola3')
		usuario = User.objects.get(username=cedula)
		print('Hola4')
		self.object.delete()
		print('Hola5')
		usuario.delete()
		print('Hola6')
		return redirect('principal:nucleos')

class AgregarCoordinador(LoginRequiredMixin, GroupRequiredMixin, generic.CreateView):
	group_required = [u'SE']
	model = models.Coordinador
	template_name = "agregar_coordinador.html"
	fields = ['nucleo','nombre','apellido','telefono','direccion','email']

	def get_context_data(self, **kwargs):
		context = super(AgregarCoordinador, self).get_context_data(**kwargs)
		nucleos = models.Nucleo.objects.all()
		coordinadores = models.Coordinador.objects.all()
		lista = models.Nucleo.objects.none()
		for nucleo in nucleos:
			con = True
			for coordinador in coordinadores:
				if coordinador.nucleo.id == nucleo.id:
					con = False
			if con:
				lista |= models.Nucleo.objects.filter(id=nucleo.id)
		context['form'].fields['nucleo'].queryset = lista
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		cedula = self.request.POST['cedula']
		if len(User.objects.filter(username=cedula)) > 0:
			usuario = User.objects.get(username=cedula)
			nivel = usuario.groups.get()
			if str(nivel) == 'CN':
				messages.add_message(self.request, messages.INFO, 'Ya esta cédula está registrada')
				return redirect('principal:agregarCoordinador')
			else:
				usuario.groups.set('2')
				obj.usuario = usuario
				obj.save()
				return redirect("principal:nucleos")
		usuario = User.objects.create_user(self.request.POST['cedula'],email=self.request.POST['email'],password=self.request.POST['cedula'])
		usuario.groups.set('2')
		obj.usuario = usuario
		obj.save()
		return redirect("principal:nucleos")

class Secretaria(LoginRequiredMixin, GroupRequiredMixin, generic.base.TemplateView):
	group_required = [u'GE']
	template_name = "secretaria.html"

	def get_context_data(self, **kwargs):
		context = super(Secretaria, self).get_context_data(**kwargs)
		usuarios = User.objects.all()
		for usuario in usuarios:
			if usuario.username != 'admin':
				nivel = usuario.groups.get()
				if str(nivel) == 'SE':
					user = models.Perfil.objects.get(usuario_id=usuario.id)
		context['object'] = user
		return context

class AgregarSecretaria(LoginRequiredMixin, GroupRequiredMixin, generic.edit.FormView):
	group_required = [u'GE']
	template_name = "agregar_secretaria.html"
	form_class = forms.SecretariaForm
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(AgregarSecretaria, self).get_context_data(**kwargs)
		usuarios = User.objects.all()
		for usuario in usuarios:
			if usuario.username != 'admin':
				nivel = usuario.groups.get()
				if str(nivel) == 'SE':
					user = models.Perfil.objects.get(usuario_id=usuario.id)
		context['usuario'] = user
		return context

	def form_valid(self, form):
		usuarios = User.objects.all()
		for usuario in usuarios:
			if usuario.username != 'admin':
				nivel = usuario.groups.get()
				if str(nivel) == 'SE':
					user = models.Perfil.objects.get(usuario_id=usuario.id)
					user2 = usuario
					user.delete()
		if len(User.objects.filter(username=self.request.POST['cedula'])) > 0:
			user3 = User.objects.get(username=self.request.POST['cedula'])
			user3.groups.set('3')
		else:
			user2.delete()
			user5 = User.objects.create_user(self.request.POST['cedula'],password=self.request.POST['cedula'])
			user5.groups.set('3')
			user4 = form.save(commit=False)
			user4.usuario = user5
			user4.save()
			return redirect('principal:secretaria')

class Catedra(LoginRequiredMixin, GroupRequiredMixin, generic.ListView):
	group_required = [u'GE']
	template_name = "catedras.html"
	model = models.Catedra

	def post(self, request, *args, **kwargs):
		models.Catedra.objects.create(nombre=request.POST['nombre'])
		return redirect('principal:catedras')