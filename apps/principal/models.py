from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Nucleo(models.Model):
	nombre = models.CharField(max_length=30)

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Catedra(models.Model):
	nombre = models.CharField(max_length=30)

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Musico(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)
	fecha = models.DateField()
	fecha_ing = models.DateField()

	SEXOS = (('M','Masculino'),('F','Femenino'))
	TIPOS = (('A', 'Alumno'),('P','Profesor'))

	sexo = models.CharField(max_length=1,choices=SEXOS)
	tipo = models.CharField(max_length=1,choices=TIPOS)
	catedra = models.ForeignKey(Catedra, on_delete="cascade")
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")
	foto = models.ImageField(upload_to="perfiles/", default="perfiles/profile.png")

	def tipo_text(self):
		return dict(Musico.TIPOS)[self.tipo]

	def get_absolute_url(self):
		return reverse('principal:index')

	def __str__(self):
		cadena = "{0} {1} - {2}, {3}, {4}"
		return cadena.format(self.nombre, self.apellido, self.nucleo, self.catedra, self.tipo_text())

class Representante(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)

	def __str__(self):
		cadena = "{0} {1}"
		return cadena.format(self.nombre, self.apellido)

class AlumnoRepresentante(models.Model):
	musico = models.ForeignKey(Musico, on_delete="cascade")
	representante = models.ForeignKey(Representante, on_delete="cascade")

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.musico, self.representante)

class TipoBien(models.Model):
	nombre = models.CharField(max_length=30)

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Bien(models.Model):
	codigo = models.BigIntegerField()
	nombre = models.ForeignKey(TipoBien, on_delete="cascade")
	marca = models.CharField(max_length=50, default=None)
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")
	fecha = models.DateField(default=timezone.now)
	caracteristicas = models.TextField(blank=True, null=True)

	OPCIONES = (('DI','Disponible'),('DE','Desincorporado'))

	status = models.CharField(max_length=2, choices=OPCIONES, default='DI')

	def tipo_text(self):
		return dict(Bien.OPCIONES)[self.status]

	def get_absolute_url(self):
		return reverse('principal:bienes')

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class SolicitudBien(models.Model):
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")

	STATUS = (('L','Lista'),('E','En espera'),('A','Aceptada'))

	fecha = models.DateField(default=timezone.now)
	mensaje = models.TextField()
	status = models.CharField(max_length=1, choices=STATUS, default="E")
	tipo = models.CharField(max_length=1, default="B")

	def get_absolute_url(self):
		return reverse('principal:solicitudes')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.nucleo, self.fecha)

class SolicitudTipoBien(models.Model):
	solicitud = models.ForeignKey(SolicitudBien, on_delete="cascade")
	bien = models.ForeignKey(TipoBien, on_delete="cascade")
	cantidad_solicitada = models.IntegerField()
	cantidad_aprobada = models.IntegerField(default=0)

	def __str__(self):
		cadena = "{0} - {1} - {2} - {3}"
		return cadena.format(self.solicitud, self.bien, self.cantidad_solicitada, self.cantidad_aprobada)

class TipoInstrumento(models.Model):
	nombre = models.CharField(max_length=30)

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Instrumento(models.Model):
	codigo = models.BigIntegerField(default=None)
	nombre = models.ForeignKey(TipoInstrumento, on_delete="cascade")
	marca = models.CharField(max_length=50, default=None)
	caracteristicas = models.TextField(default=None)
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade", default=None)
	fecha = models.DateField(default=timezone.now)

	opciones = (('DI','Disponible'),('DE','Desincorporado'))

	status = models.CharField(max_length=2, choices=opciones, default='DI')

	def tipo_text(self):
		return dict(Bien.OPCIONES)[self.status]

	def get_absolute_url(self):
		return reverse('principal:instrumentos')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.nombre, self.marca)

class SolicitudInstrumento(models.Model):
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")

	STATUS = (('L','Lista'),('E','En espera'),('A','Aceptada'))

	fecha = models.DateField()
	mensaje = models.TextField()
	status = models.CharField(max_length=1, choices=STATUS, default="E")
	tipo = models.CharField(max_length=1, default="I")

	def get_absolute_url(self):
		return reverse('principal:solicitudes')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.nucleo, self.fecha)

class SolicitudTipoInstrumento(models.Model):
	solicitud = models.ForeignKey(SolicitudInstrumento, on_delete="cascade")
	instrumento = models.ForeignKey(TipoInstrumento, on_delete="cascade")
	cantidad_solicitada = models.IntegerField()
	cantidad_aprobada = models.IntegerField(default=0)

	def __str__(self):
		cadena = "{0} - {1} - {2}"
		return cadena.format(self.solicitud, self.instrumento, self.cantidad_solicitada)

class Asignacion(models.Model):
	musico = models.ForeignKey(Musico, on_delete="cascade")
	instrumento = models.ForeignKey(Instrumento, on_delete="cascade")
	fecha_ini = models.DateField(default=timezone.now)
	fecha_fin = models.DateField(null=True,blank=True)
	status = models.CharField(max_length=1, default="A")

	def get_absolute_url(self):
		return reverse('principal:asignaciones')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.musico, self.instrumento)

class Galeria(models.Model):
	imagen = models.ImageField(upload_to="galeria/")
	descripcion = models.TextField()
	fecha = models.DateField()

	TIPO = (('S','Si'),('N','No'))

	visible = models.CharField(max_length=1, choices=TIPO)

	def get_absolute_url(self):
		return reverse('principal:galeria')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.descripcion, self.fecha)

class RecuperarPassword(models.Model):
	usuario = models.ForeignKey(User, on_delete="cascade")
	codigo = models.CharField(max_length=50)
	fecha = models.DateField(default=timezone.now)

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.usuario, self.fecha)

class Coordinador(models.Model):
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")
	usuario = models.ForeignKey(User, on_delete="cascade")
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)
	foto = models.ImageField(upload_to="perfiles/", default="perfiles/profile.png")

	def __str__(self):
		cadena = "{0} {1}"
		return cadena.format(self.nombre, self.apellido)

class BienDesincorporado(models.Model):
	nombre = models.ForeignKey(Bien, on_delete="cascade")
	mensaje = models.TextField()
	fecha = models.DateField(default=timezone.now)
	tipo = models.CharField(max_length=1, default="B")

	STATUS = (('A','Apobada'),('E','En espera'),('R','Rechazada'))

	status = models.CharField(max_length=1, choices=STATUS, default="E")

	def get_absolute_url(self):
		return reverse('principal:index')

	def __str__(self):
		cadena = "{0} - {1} - {2}"
		return cadena.format(self.nombre, self.fecha, self.status)

class InstrumentoDesincorporado(models.Model):
	nombre = models.ForeignKey(Instrumento, on_delete="cascade")
	mensaje = models.TextField()
	fecha = models.DateField(default=timezone.now)
	tipo = models.CharField(max_length=1, default="I")

	STATUS = (('A','Apobada'),('E','En espera'),('R','Rechazada'))

	status = models.CharField(max_length=1, choices=STATUS, default="E")

	def get_absolute_url(self):
		return reverse('principal:index')

	def __str__(self):
		cadena = "{0} - {1} - {2}"
		return cadena.format(self.nombre, self.fecha, self.status)

class Pago(models.Model):
	asignacion = models.ForeignKey(Asignacion, on_delete="cascade")
	fecha = models.DateField()
	imagen = models.ImageField(upload_to="pagos/")

	def get_absolute_url(self):
		return reverse('principal:pagos')

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.asignacion, self.fecha)

class Autor(models.Model):
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre

class Voz(models.Model):
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre

class Partitura(models.Model):
	TONOS = (('E','E'),('C','C'))

	nombre = models.CharField(max_length=50)
	autor = models.ForeignKey(Autor, on_delete="cascade")
	voz = models.ForeignKey(Voz, on_delete="cascade")
	tonalidad = models.CharField(max_length=5, choices=TONOS)
	fecha = models.DateField(default=timezone.now)
	usuario = models.ForeignKey(User, on_delete="cascade")
	media = models.FileField(upload_to="partituras/")

	def __str__(self):
		cadena = "{0} - {1} - {2} - {3}"
		return cadena.format(self.nombre, self.autor, self.voz, self.tonalidad)

class PartituraMusico(models.Model):
	partitura = models.ForeignKey(Partitura, on_delete="cascade")
	musico = models.ForeignKey(Musico, on_delete="cascade")

	def __str__(self):
		cadena = "{0} {1}"
		return cadena.format(self.partitura,self.musico)

class Perfil(models.Model):
	usuario = models.ForeignKey(User, on_delete="cascade")
	nombre = models.CharField(max_length=50,blank=True,null=True)
	apellido = models.CharField(max_length=50,blank=True,null=True)
	telefono = models.BigIntegerField(blank=True,null=True)
	direccion = models.TextField(blank=True,null=True)
	foto = models.ImageField(upload_to="perfiles/", default="perfiles/profile.png")

	def __str__(self):
		return self.usuario.__str__()