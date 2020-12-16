"""Cine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminCine import views

#Username: amarotta Pass: amarotta1234, 
#Contraseña tambien para postgres -> Puerto 5432

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('salas/',views.listar_salas),
    path('salasSerial/<int:id_sala>',views.sala_serial),
    path('salasSerial/',views.salas_serial),
    path('buscarSala/',views.buscar_sala),
    path('resultadoSala/',views.get_sala),
    path('crearSala/',views.crear_sala),
    path('editarSala/',views.editar_sala),
    path('eliminarSala/',views.eliminar_sala),
    path('peliculas/',views.listar_peliculas),
    path('peliculasSerial/<int:rango>/<str:tiempo>',views.listar_peliculas_serial),
    path('serializarPelicula/<int:id_pelicula>/<str:f1>/<str:f2>',views.pelicula_serializer),
    path('proyeccionesSerial/',views.proyecciones_serial),
    path('proyeccionesSerial/<str:dia>',views.proyecciones_dia_serial),
    path('proyeccionesSerial/actualizar/<int:id_proyeccion>',views.proyeccion_actualizar_serial),
    path('proyeccionesSerial/<str:fecha>/<int:id_pelicula>',views.proyeccion_info_serial),
    path('butacasSerial/',views.butacas_serial),
    path('butacasSerial/<int:id_butaca>',views.butaca_serial),
    path('reportes/butacas/<str:f1>/<str:f2>',views.reporte_butacas),
    path('reportes/butacas/<str:f1>/<str:f2>/<int:id_proyeccion>',views.reporte_butacas_proyeccion),
    path('reportes/ranking/<str:f1>/<str:f2>/',views.reporte_ranking),
    path('reportes/peliculas/',views.reporte_peliculas),
    path('ranking/',views.ranking),
    path('vendidas/',views.vendidas_peliculas)


]
