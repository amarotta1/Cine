from datetime import datetime , timedelta
import operator

""" ahora = datetime.now().date()

pasado = ahora - timedelta(days=20)

dias = ahora - pasado

lista = [str(ahora),pasado]

valor = lista

print(ahora,pasado , dias.days, valor)
 """

vendidas = {'1':1, '2':5,'3':2,'4':6,'5':5,'6':8,'7':3,'8':1,}

hola = vendidas
print(hola)
vendidas['1'] += 10

print(vendidas['sd'])

vendidas = sorted(vendidas.items(), key=operator.itemgetter(1), reverse=True)

for i in range(5):
    print(vendidas[i])


