from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
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
				'tipo': str(request.user.groups.get()),
				'bienes': str(len(models.Bien.objects.all())),
				'instrumentos': str(len(models.Instrumento.objects.all())),
				'profesores': str(len(models.Musico.objects.filter(tipo="P"))),
				'alumnos': str(len(models.Musico.objects.filter(tipo="A"))),
				'asignaciones': str(len(models.Asignacion.objects.all())),
				'galeria': str(len(models.Galeria.objects.all()))
			}
			return render(request, "dashboard.html", context)

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

class ModificarPerfil(generic.base.TemplateView):
	template_name = "modificarPerfil.html"

class AgregarBien(generic.base.TemplateView):
	template_name = "agregarBien.html"

class Solicitudes(LoginRequiredMixin, generic.ListView):
	model = models.SolicitudBien
	paginate_by = 5
	template_name = "solicitudes.html"
	
	def get_context_data(self, **kwargs):
		context = super(Solicitudes, self).get_context_data(**kwargs)
		bienes = models.SolicitudBien.objects.all()
		instrumentos = models.SolicitudInstrumento.objects.all()
		result = sorted(chain(bienes,instrumentos), key=attrgetter('fecha'))
		context['solicitudes'] = result
		return context

class SolicitudBien(LoginRequiredMixin, generic.edit.UpdateView):
	model = models.SolicitudBien
	fields = ['status']
	template_name = "solicitud.html"

	def get_context_data(self, **kwargs):
		context = super(SolicitudBien, self).get_context_data(**kwargs)
		context['bienes'] = models.SolicitudTipoBien.objects.filter(solicitud_id=self.object.id)
		return context

	def form_valid(self, form):
		for bien in models.SolicitudTipoBien.objects.filter(solicitud_id=self.object.id):
			bien.cantidad_aprobada = self.request.POST.get('ctd%i' %(bien.id))
			bien.save()
		return super().form_valid(form)

class SolicitudInstrumento(LoginRequiredMixin, generic.edit.UpdateView):
	model = models.SolicitudInstrumento
	fields = ['status']
	template_name = "solicitud.html"

	def get_context_data(self, **kwargs):
		context = super(SolicitudInstrumento, self).get_context_data(**kwargs)
		context['bienes'] = models.SolicitudTipoInstrumento.objects.filter(solicitud_id=self.object.id)
		return context

	def form_valid(self, form):
		for instrumento in models.SolicitudTipoInstrumento.objects.filter(solicitud_id=self.object.id):
			instrumento.cantidad_aprobada = self.request.POST.get('ctd%i' %(instrumento.id))
			instrumento.save()
		return super().form_valid(form)

class Bien(LoginRequiredMixin, generic.DetailView):
	model = models.Bien
	template_name = "bien.html"

class Bienes(LoginRequiredMixin, generic.ListView):
	model = models.Bien
	paginate_by = 5
	template_name = "bienes.html"

class Instrumentos(LoginRequiredMixin, generic.ListView):
	model = models.Instrumento
	paginate_by = 5
	template_name = "instrumentos.html"

class Instrumento(LoginRequiredMixin, generic.DetailView):
	model = models.Instrumento
	template_name = "instrumento.html"

class Profesores(LoginRequiredMixin, generic.ListView):
	model = models.Musico
	template_name = "profesores.html"

class Profesor(LoginRequiredMixin, generic.DetailView):
	model = models.Musico
	template_name = "profesor.html"

class Alumnos(LoginRequiredMixin, generic.ListView):
	model = models.Musico
	template_name = "alumnos.html"

class Alumno(LoginRequiredMixin, generic.DetailView):
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

class Asignaciones(LoginRequiredMixin, generic.ListView):
	model = models.Asignacion
	template_name = "asignaciones.html"

class Galeria(LoginRequiredMixin, generic.edit.CreateView):
	form_class = forms.GaleriaForm
	model = models.Galeria
	template_name = "galeria.html"

	def get_context_data(self, **kwargs):
		context = super(Galeria, self).get_context_data(**kwargs)
		context['fotos'] = models.Galeria.objects.all()
		return context

class GaleriaVisible(View, LoginRequiredMixin):

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

class BienesDes(generic.base.TemplateView):
	template_name = "bienesDes.html"

class InstrumentosDes(generic.base.TemplateView):
	template_name = "instrumentosDes.html"