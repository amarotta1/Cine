from rest_framework import serializers
from adminCine.models import Sala , Proyeccion , Butaca
 
 
class SalaSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Sala
        fields = ('id_sala',
                  'nombre',
                  'activo',
                  'filas',
                  'asientos')

class ProyeccionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Proyeccion
        fields = ('id_proyeccion',
                  'sala',
                  'pelicula',
                  'fechaInicio',
                  'fechaFin',
                  'hora',
                  'estado')

class ButacaSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Butaca
        fields = ('id_butaca',
                  'proyeccion',
                  'fecha',
                  'fila',
                  'asiento'
                  )


