from django.urls import path

from . import views

app_name = "principal"
urlpatterns = [
	path('',views.Index.as_view(),name="index"),
	path('login/',views.Login.as_view(),name="login"),
	path('logout/',views.Logout.as_view(),name="logout"),
	path('nosotros/',views.Nosotros.as_view(),name="nosotros"),
	path('perfil/',views.Perfil.as_view(),name="perfil"),
	path('perfil/modificar',views.ModificarPerfil.as_view(),name="modificarPerfil"),
	path('bienes/agregar/',views.AgregarBien.as_view(),name="agregarBien"),
	path('solicitudes/',views.Solicitudes.as_view(),name="solicitudes"),
	path('solicitudes/bienes/<int:pk>/',views.SolicitudBien.as_view(),name="solicitudBien"),
	path('solicitudes/instrumentos/<int:pk>/',views.SolicitudInstrumento.as_view(),name="solicitudInstrumento"),
	path('bienes/',views.Bienes.as_view(),name="bienes"),
	path('bienes/<int:pk>',views.Bien.as_view(),name="bien"),
	path('instrumentos/',views.Instrumentos.as_view(),name="instrumentos"),
	path('instrumentos/<int:pk>/',views.Instrumento.as_view(),name="instrumento"),
	path('profesores/',views.Profesores.as_view(),name="profesores"),
	path('profesores/<int:pk>/',views.Profesor.as_view(),name="profesor"),
	path('alumnos/',views.Alumnos.as_view(),name="alumnos"),
	path('alumnos/<int:pk>/',views.Alumno.as_view(),name="alumno"),
	path('asignaciones/',views.Asignaciones.as_view(),name="asignaciones"),
	path('galeria/',views.Galeria.as_view(),name="galeria"),
	path('galeria/visibles/',views.GaleriaVisible.as_view(),name="galeriaVisible"),
	path('bienesDes/',views.BienesDes.as_view(),name="bienesDes"),
	path('instrumentosDes/',views.InstrumentosDes.as_view(),name="instrumentosDes"),
]