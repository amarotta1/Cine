from django.shortcuts import render,HttpResponse
from adminCine.models import Sala , Pelicula, Proyeccion , Butaca
from adminCine.forms import FormularioSalas
from datetime import datetime, timedelta
from django.core import serializers
import json
import operator

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from adminCine.cine_serializer import SalaSerializer ,ProyeccionSerializer, ButacaSerializer, PeliculaSerializer


#El proyecto tiene 2 partes, la primera corresponde a lo pedido en el practico, retornando los objetos JSON solicitados
#En la segunda parte probe con crear una interfaz web sencilla.

#ENDPOINT PELICULA

#Funcion que busca todos los dias que esta disponible una pelicula en un rango de tiempo
#Ejemplo: http://localhost:8000/serializarPelicula/2/2002-02-05/2002-02-12
@api_view(['GET']) 
def pelicula_serializer(request,id_pelicula,f1,f2):
    
    #busco la pelicula por su id
    try:
        pelicula = Pelicula.objects.get(id_pelicula = id_pelicula) 
    except:
        return JsonResponse({'message': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND) 

    #serializo los datos obtenidos en formato json
    lista = serializers.serialize('json',(pelicula,)) 
    #lo paso a una lista de python
    jsonData = lista
    jsonToPython = json.loads(jsonData)
    #agrego las fechas a mostrar
    jsonToPython[0].setdefault('desde',f1)
    jsonToPython[0].setdefault('hasta',f2)
    #paso las fechas en str a tipo date
    f1 = datetime.strptime(f1, '%Y-%m-%d').date()
    f2 = datetime.strptime(f2, '%Y-%m-%d').date()
    #Obtengo la fecha de inicio y fin de la pelicula
    fc = pelicula.fechaComienzo
    ff = pelicula.fechaFinalizacion
    #Calculo el rango y verifico los dias disponibles
    rango = f2 - f1
    dias_disponible = []    
    for i in range(rango.days + 1):
        if f1 >= fc and f1 <= ff:
            dias_disponible.append(str(f1))
        f1 = f1 + timedelta(days=1)    #le sumo un dia hasta llegar a la fecha2      
    #agrego la lista con los dias diponibles
    jsonToPython[0].setdefault('diasDisponible',dias_disponible)
    #lo vuelvo a pasar a formato json para enviarlo
    lista = json.dumps(jsonToPython )
    return HttpResponse(lista,content_type = 'aplication/json')

#listado de todas las peliculas disponibles en un rango de tiempo pasado, presente o futuro
#Ejemplo: http://localhost:8000/peliculasSerial/100/pasado
@api_view(['GET']) 
def listar_peliculas_serial(request,rango,tiempo):
    fecha_actual = datetime.now().date()

    if tiempo == 'pasado': #como voy para atras tengo en cuenta la fecha de finalizacion
        fecha = fecha_actual - timedelta(days=rango) 
        peliculas_disponible = Pelicula.objects.filter(fechaFinalizacion__gte= fecha,fechaComienzo__lte=fecha_actual)        

        return JsonResponse(PeliculaSerializer(peliculas_disponible, many=True).data, safe=False, status=status.HTTP_200_OK)

    elif tiempo == "futuro":#como voy para adelante tengo en cuenta la fecha de comienzo
        fecha = fecha_actual + timedelta(days=rango) 
        peliculas_disponible = Pelicula.objects.filter(fechaFinalizacion__gte= fecha_actual,fechaComienzo__lte=fecha)        

        return JsonResponse(PeliculaSerializer(peliculas_disponible, many=True).data, safe=False, status=status.HTTP_200_OK)

      
#ENDPOINT SALA

#GET ALL y POST
#http://localhost:8000/salasSerial/
@api_view(['GET', 'POST'])
def salas_serial(request):
    if request.method == "GET":     
        return JsonResponse(SalaSerializer(Sala.objects.all(),many = True).data,safe = False,status = status.HTTP_200_OK) 

    elif request.method == 'POST':
        #Responde al modelo que cree
        sala_serializer = SalaSerializer(data=JSONParser().parse(request))

        if sala_serializer.is_valid():
            sala_serializer.save()
            return JsonResponse(sala_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Una sala en especifico
#http://localhost:8000/salasSerial/1  Es igual al anterior pero pasandole un id      
@api_view(['GET', 'PUT', 'DELETE'])  
def sala_serial(request,id_sala):
    try:
        sala = Sala.objects.get(id_sala = id_sala )
    except:
        return JsonResponse({'message': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET': 
        return JsonResponse(SalaSerializer(sala) .data)

    elif request.method == 'PUT': #tengo que enviar toda la informacion para que lo valide
        sala_data = JSONParser().parse(request) 
        sala_serializer = SalaSerializer(sala, data=sala_data) 
        if sala_serializer.is_valid(): 
            sala_serializer.save() 
            return JsonResponse(sala_serializer.data) 
        return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    elif request.method == 'DELETE': 
        sala.delete() 
        return JsonResponse({'message': 'La sala fue eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

#ENDPOINT PROYECCIONES
#http://localhost:8000/proyeccionesSerial/
@api_view(['GET', 'POST'])
def proyecciones_serial(request):
    if request.method == "GET":
        proy = Proyeccion.objects.all()
        lista = []
        for p in proy:
            if p.estado == True: #solo devolver las activas 
                proy_json = ProyeccionSerializer(p)          
                lista.append(proy_json.data)
        proyecciones_json = json.dumps(lista)
        return HttpResponse(proyecciones_json,content_type = 'aplication/json') 
    
    elif request.method == 'POST':
        proy_data = JSONParser().parse(request)
        #Responde al modelo que creé
        proy_serializer = ProyeccionSerializer(data=proy_data)

        if proy_serializer.is_valid():
            proy_serializer.save()
            return JsonResponse(proy_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(proy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
""" Ejemplo
{
        "sala": 11,
        "pelicula": 6,
        "fechaInicio": "2020-12-01",
        "fechaFin": "2020-12-31",
        "hora": "22:00",
        "estado": true
      }"""
 
#COLOCO GET Y PUT EN FUNCIONES DISTINTAS PORQUE SE SOLICITAN CON DATOS DIFERENTES
#http://localhost:8000/proyeccionesSerial/2020-10-08
@api_view(['GET'])
def proyecciones_dia_serial(request,dia):
    dia = datetime.strptime(dia, '%Y-%m-%d').date()
    proyecciones = Proyeccion.objects.filter(fechaInicio__lte=dia,fechaFin__gte=dia,estado=True)

    return JsonResponse(ProyeccionSerializer(proyecciones, many=True).data, safe=False, status=status.HTTP_200_OK)
     

#http://localhost:8000/proyeccionesSerial/actualizar/8
@api_view(['PUT'])  
def proyeccion_actualizar_serial(request,id_proyeccion):
    try:
        proy = Proyeccion.objects.get(id_proyeccion = id_proyeccion )
    except:
        return JsonResponse({'message': 'La proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND) 

    
    #tengo que enviar toda la informacion para que lo valide 
    proy_data = JSONParser().parse(request) 
    proy_serializer = ProyeccionSerializer(proy, data=proy_data) 
    if proy_serializer.is_valid(): 
        proy_serializer.save() 
        return JsonResponse(proy_serializer.data) 
    return JsonResponse(proy_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#http://localhost:8000/proyeccionesSerial/2020-10-08/3
@api_view(['GET'])  
def proyeccion_info_serial(request,fecha,id_pelicula):

    try:
        pelicula = Pelicula.objects.get(id_pelicula = id_pelicula )
    except:
        return JsonResponse({'message': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND) 

    peli = serializers.serialize('json',(pelicula,)) 
    peli_json = json.loads(peli)
    peli_json = peli_json[0]['fields']
    peli_json.setdefault('Dia solicitado',fecha)
    
    proyecciones = Proyeccion.objects.filter(pelicula=id_pelicula)
    dia = datetime.strptime(fecha, '%Y-%m-%d').date()
            
    for p in proyecciones:
        if dia >= p.fechaInicio and dia <= p.fechaFin:
            #sala = Sala.objects.get(id_sala = p.sala.id_sala) 
            sala = serializers.serialize('json',(p.sala,))  
            nombre_sala = f'Sala {p.sala.nombre}'   
            sala = json.loads(sala)
            sala = sala[0]['fields']
            butacas = Butaca.objects.filter(proyeccion=p.id_proyeccion,fecha = fecha)
            lista_butacas = []
            for b in butacas:
                but_s = serializers.serialize('json',(b,))                    
                butaca= json.loads(but_s)
                lista_butacas.append(butaca[0]['fields'])
            sala['butacas reservadas'] = lista_butacas
            peli_json.setdefault(nombre_sala,sala)                     

    lista = json.dumps(peli_json)
    return HttpResponse(lista,content_type = 'aplication/json')        



#ENDPOINT BUTACAS
#http://localhost:8000/butacasSerial/
@api_view(['GET', 'POST'])
def butacas_serial(request):
    if request.method == "GET":
        return JsonResponse(ButacaSerializer(Butaca.objects.all(),many = True).data,safe = False,status = status.HTTP_200_OK) 
    
    elif request.method == 'POST':
        butaca_data = JSONParser().parse(request)

        #Responde al modelo que cree, veo si es valido
        butaca_serializer = ButacaSerializer(data=butaca_data) 

        if butaca_serializer.is_valid():

            #busco la proyeccion para ver si es activa o las fechas son validas
            proyeccion = Proyeccion.objects.get(id_proyeccion = butaca_data['proyeccion'])

            #paso las fechas en str a tipo date
            fecha_reserva = datetime.strptime(butaca_data['fecha'], '%Y-%m-%d').date()
        

            if proyeccion.estado == False:
                return JsonResponse({'message': 'La proyeccion no esta activa'}, status=status.HTTP_409_CONFLICT)
            elif fecha_reserva < proyeccion.fechaInicio or fecha_reserva > proyeccion.fechaFin:
                return JsonResponse({'message': 'La proyeccion no esta disponible en esa fecha'}, status=status.HTTP_409_CONFLICT)
        
            #debo filtrar las butacas por proyeccion y dia y ver si en esa fila y asiento ya hay reserva
            butacas = Butaca.objects.filter(proyeccion=butaca_data['proyeccion'],fecha=butaca_data['fecha'])

            reservada = False
            for b in butacas:              
                if b.fila == int(butaca_data['fila']) and b.asiento == int(butaca_data['asiento']):
                    reservada = True
                    break                     
                     
            if reservada == False:
                butaca_serializer.save()            
                return JsonResponse(butaca_serializer.data, status=status.HTTP_201_CREATED) 
            else:
                return JsonResponse({'message': 'La butaca no esta disponible'}, status=status.HTTP_409_CONFLICT)

        else:    
            return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

#http://localhost:8000/butacasSerial/1
@api_view(['GET', 'PUT'])
def butaca_serial(request,id_butaca):
    try:
        butaca = Butaca.objects.get(id_butaca = id_butaca )
    except:
        return JsonResponse({'message': 'La butaca no existe'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET': 
        return JsonResponse(ButacaSerializer(butaca).data)
    if request.method == 'PUT': 
        butaca_data = JSONParser().parse(request) 
        butaca_serializer = ButacaSerializer(butaca, data=butaca_data) 
        if butaca_serializer.is_valid(): 
            butaca_serializer.save() 
            return JsonResponse(butaca_serializer.data) 
        return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#ENDPOINT REPORTES
#butacas vendidas en un rango de timepo
#localhost:8000/reportes/butacas/2000-01-01/2020-10-08
@api_view(['GET'])
def reporte_butacas(request,f1,f2):
    f1 = datetime.strptime(f1, '%Y-%m-%d').date()
    f2 = datetime.strptime(f2, '%Y-%m-%d').date()

    return JsonResponse(ButacaSerializer(Butaca.objects.filter(fecha__gte=f1,fecha__lte=f2),many = True).data,safe = False,status = status.HTTP_200_OK) 


#butacas vendidas en un rango de tiempo de una proyeccion en particular
#localhost:8000/reportes/butacas/2000-01-01/2020-10-08/4
@api_view(['GET'])
def reporte_butacas_proyeccion(request,f1,f2,id_proyeccion):
    f1 = datetime.strptime(f1, '%Y-%m-%d').date()
    f2 = datetime.strptime(f2, '%Y-%m-%d').date()  

   
    return JsonResponse(ButacaSerializer(Butaca.objects.filter(fecha__gte=f1,fecha__lte=f2,proyeccion=id_proyeccion),many = True).data,safe = False,status = status.HTTP_200_OK) 

#Ranking de las 5 peliculas mas vendidas en un rango de tiempo
#localhost:8000/reportes/ranking/2000-01-01/2020-12-31/
@api_view(['GET'])
def reporte_ranking(request,f1,f2):
    f1 = datetime.strptime(f1, '%Y-%m-%d').date()
    f2 = datetime.strptime(f2, '%Y-%m-%d').date()

    butacas = Butaca.objects.filter(fecha__gte=f1,fecha__lte=f2)
    vendidas = {}

    for b in butacas:        
        #si existe que le agrege 1, sino que le ponga un 1
        if b.proyeccion in vendidas:
            vendidas[b.proyeccion] += 1
        else:
            vendidas[b.proyeccion] = 1

    #las ordeno de mayor a menor, me devuelve una lista de tuplas
    vendidas = sorted(vendidas.items(), key=operator.itemgetter(1), reverse=True)

    ranking = {}

    # Puede que en ese rango de tiempo existan menos de 5 proyecciones con butacas vendidas
    for i in range(len(vendidas)):
        nombre = f'Proyeccion {vendidas[i][0].id_proyeccion}'
        valor = f'Vendidas {vendidas[i][1]}'
        ranking[nombre] = valor
        if i >= 5:
            break

    ranking = json.dumps(ranking)

    return HttpResponse(ranking,content_type = 'aplication/json')


# De las películas que se encuentran activas, detallar las entradas que se han vendido hasta el momento.
@api_view(['GET'])
def reporte_peliculas(request):
    peliculas  = Pelicula.objects.filter(estado=True)

    detalle = {}

    for p in peliculas:
        #por cada una de las peliculas creo una lista con su nombre
        detalle[p.nombre] = []
        
        #obtengo la lista de todas las proyecciones de esa pelicula        
        proyecciones = Proyeccion.objects.filter(pelicula=p)

        for proy in proyecciones:
            #dentro de la lista creo diccionarios con un campo proyeccion y otro butacas          
            butacas = Butaca.objects.filter(proyeccion=proy).order_by('-fecha')
            lista_butacas = []

            for b in butacas:
                butaca = ButacaSerializer(b)
                #obtengo los datos que me interesan
                data = dict(fecha= butaca.data['fecha'],fila= butaca.data['fila'],asiento= butaca.data['asiento'])
                lista_butacas.append(data)
            
            detalle[p.nombre].append({'proyeccion':proy.id_proyeccion,'butacas':lista_butacas})

    detalle = json.dumps(detalle)
    return HttpResponse(detalle,content_type = 'aplication/json')


#-------------------Administracion desde la pagina web---------------------#

#index

def index(request):
    if request.method == 'GET':
        return render(request,"index.html")

#ADMINISTRAR SALAS 
def listar_salas(request):
    if request.method == 'GET': 
        salas = Sala.objects.all()
        return render(request,"lista_salas.html",{'salas':salas})

def buscar_sala(request):
    return render(request,'busqueda_sala.html')


def get_sala(request):
    if request.method == 'GET':
        try:
            if request.GET["sala"]:
                sala_pedida = request.GET["sala"]
                sala = Sala.objects.get(id_sala = sala_pedida)
                return render(request,'resultado_sala.html',{'sala':sala})
            else:
                return render(request,'not_valid.html')
        except:
            return render(request,'not_valid.html')

def crear_sala(request):
    if request.method == 'POST':
        formulario = FormularioSalas(request.POST)

        if formulario.is_valid():
            formulario.save()
            info = formulario.data
            return render(request,"sala_creada.html",{'nombre':info['nombre'],'filas':info['filas'],'asientos':info['asientos']})
    else:
        formulario = FormularioSalas()
    return render(request,"crear_sala.html",{"formulario":formulario})



def editar_sala(request):
    formulario = None
    if request.method == 'GET':    
        try:
            id_sala = request.GET['id_sala']  
            sala = Sala.objects.get(id_sala = id_sala)
            formulario = FormularioSalas(instance=sala)
            print(request.method + "GET")
        except:
            pass
    elif request.method == 'POST':
        print(request.method + "POST")
        print(request.POST)
        sala = Sala.objects.get(id_sala = request.POST['id_sala'])
        formulario = FormularioSalas(request.POST, instance=sala)
        if formulario.is_valid():
            formulario.save()
            
        return render(request,"sala_editada.html",{'sala':sala})
    return render(request,"editar_sala.html",{'formulario': formulario})  

def eliminar_sala(request):
    sala = None
    if request.method == 'GET':    
        try:
            id_sala = request.GET['id_sala']  
            sala = Sala.objects.get(id_sala = id_sala)
            return render(request,'eliminar_sala.html',{'sala': sala})            
        except:
            pass
    elif request.method == 'POST':
        id_sala = request.POST['id_sala2']  
        sala = Sala.objects.get(id_sala = id_sala)
        nombre = sala.nombre
        sala.delete()
        return render(request,"sala_eliminada.html",{"id":id_sala,"nombre":nombre})
    return render(request,'eliminar_sala.html',{'sala': sala}) 
    


#ADMINISTRAR PELICULAS 
# http://127.0.0.1:8000/peliculas/100/pasado
def listar_peliculas(request):
    fecha_actual = datetime.now().date()
    peliculas = Pelicula.objects.all()
    peliculas_disponibles = []
    
    for pelicula in peliculas: 
        if (pelicula.fechaComienzo <= fecha_actual) and (pelicula.fechaFinalizacion >= fecha_actual):
            peliculas_disponibles.append(pelicula)
    
    return render(request,"listar_peliculas.html",{"disponibles":peliculas_disponibles,"hoy":fecha_actual})

   
#REPORTES

@api_view(['GET'])
def ranking(request):

    ranking = None
    try:
        
        f1 = datetime.strptime(request.GET['f1'], '%Y-%m-%d').date()
        f2 = datetime.strptime(request.GET['f2'], '%Y-%m-%d').date()

        butacas = Butaca.objects.all()
        vendidas = {}

        for b in butacas:
            if b.fecha >= f1 and b.fecha <= f2:
                #si existe que le agrege 1, sino que le ponga un 1
                if b.proyeccion in vendidas:
                    vendidas[b.proyeccion] += 1
                else:
                    vendidas[b.proyeccion] = 1

        #las ordeno de mayor a menor, me devuelve una lista de tuplas
        vendidas = sorted(vendidas.items(), key=operator.itemgetter(1), reverse=True)

        ranking = {}

        # Puede que en ese rango de tiempo existan menos de 5 proyecciones con butacas vendidas
        for i in range(len(vendidas)):
            nombre = f'Proyeccion {vendidas[i][0].id_proyeccion}'
            valor = f'Pelicula: {vendidas[i][0].pelicula}, Vendidas: {vendidas[i][1]}'
            ranking[nombre] = valor
            if i >= 5:
                break
        return render(request,"ranking.html",{"ranking":ranking.items()})
    except:
        return render(request,"ranking.html",{"ranking":ranking})

@api_view(['GET'])
def vendidas_peliculas(request):
    peliculas  = Pelicula.objects.filter(estado=True)

    detalle = {}

    for p in peliculas:
        #por cada una de las peliculas creo una lista con su nombre
        detalle[p.nombre] = []
        
        #obtengo la lista de todas las proyecciones de esa pelicula        
        proyecciones = Proyeccion.objects.filter(pelicula=p)

        for proy in proyecciones:
            #dentro de la lista creo diccionarios con un campo proyeccion y otro butacas          
            butacas = Butaca.objects.filter(proyeccion=proy).order_by('-fecha')
            lista_butacas = []

            for b in butacas:
                butaca = ButacaSerializer(b)
                #obtengo los datos que me interesan
                data = dict(fecha= butaca.data['fecha'],fila= butaca.data['fila'],asiento= butaca.data['asiento'])
                lista_butacas.append(data)
            
            detalle[p.nombre].append({'proyeccion':proy.id_proyeccion,'butacas':lista_butacas})

    print(detalle)

    return render(request,"vendidas.html",{'vendidas': detalle.items()})  

        