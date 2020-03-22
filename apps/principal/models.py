from django.db import models
from django.urls import reverse
from django.utils import timezone

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

	def tipo_text(self):
		return dict(Musico.TIPOS)[self.tipo]

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
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade", default=None)
	fecha = models.DateField(default=timezone.now)

	OPCIONES = (('DI','Disponible'),('DE','Desincorporado'))

	status = models.CharField(max_length=2, choices=OPCIONES, default='DI')

	def tipo_text(self):
		return dict(Bien.OPCIONES)[self.status]

	def __str__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class SolicitudBien(models.Model):
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")

	STATUS = (('L','Lista'),('E','En espera'))

	fecha = models.DateField()
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

	def __str__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.nombre, self.marca)

class SolicitudInstrumento(models.Model):
	nucleo = models.ForeignKey(Nucleo, on_delete="cascade")

	STATUS = (('L','Lista'),('E','En espera'))

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
	fecha_fin = models.DateField(default=None)

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