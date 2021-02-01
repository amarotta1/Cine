import requests
from datetime import datetime
import os
import django

#Le digo en que entorno va a trabajar
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Cine.settings")
django.setup()

from adminCine.models import Pelicula

def api_peliculas():
    peliculas = requests.get('http://localhost:5000/api/pelicula/').json()
    
    #Adaptarlas a lo que ya habia hecho
    for pelicula in peliculas:
        
        pelicula['fechaComienzo'] = datetime.date(datetime.strptime(pelicula['fechaComienzo'], '%Y-%m-%dT%H:%M:%S+%f'))
        pelicula['fechaFinalizacion'] = datetime.date(datetime.strptime(pelicula['fechaFinalizacion'],'%Y-%m-%dT%H:%M:%S+%f'))
        
        if (pelicula['estado'] == "Activa"):
            pelicula['estado'] = True
        else:
            pelicula['estado'] = False

    return peliculas

def actualizar(pelicula):
    Pelicula.objects.update_or_create(
        id_pelicula=pelicula.get('id'),
        defaults={
            'nombre': pelicula.get('nombre'),
            'duracion': pelicula.get('duracion'),
            'descripcion': pelicula.get('descripcion'),
            'detalle': pelicula.get('detalle'),
            'genero': pelicula.get('genero'),
            'clasificacion': pelicula.get('clasificacion'),
            'estado': pelicula.get('estado'),
            'fechaComienzo': pelicula.get('fechaComienzo'),
            'fechaFinalizacion': pelicula.get('fechaFinalizacion')
        })

def inactiva(pelicula):
    pelicula = Pelicula.objects.get(id_pelicula = pelicula.get('id_pelicula')) 
    pelicula.estado = False
    pelicula.save()


def main():

    servicio = api_peliculas()
    baseDatos = list(Pelicula.objects.all().values())

    #Si alguna pelicula del servicio no esta o es diferente a la de la BD, esta se agrega o actualiza

    for pelicula in servicio:
        if pelicula not in baseDatos:
            actualizar(pelicula)

    #Si ya no esta en el Servicio no se elimina, se coloca como inactiva
    for pelicula in baseDatos:
        if pelicula not in servicio:
            inactiva(pelicula)









