from django.db import models

# Create your models here.
class Sala(models.Model):
   id_sala = models.AutoField(primary_key=True) 
   nombre = models.CharField(max_length=10,blank=False,null=False)
   activo = models.BooleanField(default=False)
   filas = models.IntegerField(blank=False,null=False)
   asientos = models.IntegerField(blank=False,null=False)

   def __str__(self):
      return self.nombre

class Pelicula(models.Model):
   id_pelicula = models.AutoField(primary_key=True) 
   nombre = models.CharField(max_length=60,blank=False,null=False) #La mas larga que se me ocurrio tenia 50
   duracion = models.IntegerField(blank=False,null=False)
   descripcion = models.CharField(max_length=10000,blank=False,null=False)
   detalle = models.CharField(max_length=10000,blank=False,null=False)
   genero = models.CharField(max_length=30,blank=False,null=False)
   clasificacion = models.CharField(max_length=30,blank=False,null=False)
   estado = models.BooleanField(default=False)
   fechaComienzo = models.DateField()
   fechaFinalizacion = models.DateField()

   def __str__(self):
      return self.nombre


class Proyeccion(models.Model):
   id_proyeccion = models.AutoField(primary_key=True) 
   sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null = False, blank=False)
   pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, null = False, blank=False)
   fechaInicio = models.DateField()
   fechaFin = models.DateField()
   hora = models.CharField(max_length=5,blank=False,null=False)
   estado = models.BooleanField(default=False)

   def __str__(self):
      return "ID: {} Sala:{} - Pelicula:{} - Fecha:{}/{}".format(self.id_proyeccion,self.sala,self.pelicula,self.fechaInicio,self.fechaFin)


class Butaca(models.Model):
   id_butaca = models.AutoField(primary_key=True)
   proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE, null = False, blank=False)
   fecha = models.DateField()
   fila = models.IntegerField(blank=False,null=False)
   asiento = models.IntegerField(blank=False,null=False)

   def __str__(self):
      return "ID: {}".format(self.id_butaca)

