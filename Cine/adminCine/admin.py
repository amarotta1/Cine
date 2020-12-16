from django.contrib import admin
from adminCine.models import Sala,Pelicula,Proyeccion,Butaca


#Para editar los datos que veo en el panel de admin
class SalaAdmin(admin.ModelAdmin):
    list_display = ("id_sala","nombre","activo")#los que aparecen en la columna de la tabla
    search_fields = ("nombre",)#para poder hacer busquedas
    list_filter = ("activo",) #filtra por activo true o false

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ("id_pelicula","nombre","duracion","estado")
    search_fields = ("nombre",)
    list_filter = ("estado","genero","clasificacion")
    date_hierarchy = "fechaComienzo"

class ProyeccionAdmin(admin.ModelAdmin):
    list_display = ("id_proyeccion","sala","pelicula","fechaInicio","estado")
    search_fields = ("pelicula",)
    date_hierarchy = "fechaInicio"
    list_filter = ("estado","sala")

class ButacaAdmin(admin.ModelAdmin):
    list_display = ("id_butaca","proyeccion","fecha","fila","asiento")



# Register your models here.
admin.site.register(Sala,SalaAdmin)
admin.site.register(Pelicula,PeliculaAdmin)
admin.site.register(Proyeccion,ProyeccionAdmin)
admin.site.register(Butaca,ButacaAdmin)

