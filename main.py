import numpy as np
import math
import random
import matplotlib.pyplot as plt
import sys

###################################################
### Expand
###################################################

def expandir(x, y):
    global contador
    global puntoAnterior
    if Tablero[x][y] == 0:
      Tablero[x][y] = 2
    
    contador+= abs(x - puntoAnterior[0]) + abs(y - puntoAnterior[1])
    puntoAnterior[0] = x
    puntoAnterior[1] = y
    hijos = []
    for i in range(x - 1, x + 2):
        if i < 0 or i > x_max - 1:
            continue
        for j in range(y - 1, y + 2):
            if j < 0 or j > y_max - 1:
                continue
            # Si la coordenada es distinta de la coordenada actual
            posicion_actual = (i, j)
            if [x, y] != posicion_actual:
                if not Tablero[posicion_actual[0], posicion_actual[1]] == 1 and posicion_actual not in visitados:
                    hijos.append(posicion_actual)
                    visitados.append(posicion_actual)

    random.shuffle(hijos)
    return hijos

###################################################
### Búsqueda a lo ancho
###################################################

def busqueda_ancho(frontera):
  estado_actual = frontera.pop(0)
#  print(f'{estado_actual}\t{Fin}')
  if goal_test(estado_actual):
    return estado_actual
  else:
    offspring = expandir(estado_actual[0], estado_actual[1])
    frontera.extend(offspring)
  return busqueda_ancho(frontera)

#def mejor_busqueda_ancho(frontera):

###################################################
### Búsqueda profundo y búsqueda de profundidad limitada e iterada
###################################################

def b_profundidad(frontera):
  estado_actual = frontera.pop(0)
  if goal_test(estado_actual):
    return True
  else:
    x = estado_actual[0]
    y = estado_actual[1]
    offspring = expandir(estado_actual[0], estado_actual[1])
    frontera = recorrerOffspring(offspring, frontera)
#    frontera.insert(0, offspring) # ponerlo al inicio del arreglo

  return b_profundidad(frontera)

def recorrerOffspring(offspring, frontera):
    for i in offspring:
      frontera.insert(0, i)
    return frontera

def b_profundidadLim(frontier, limite):
  nodo_actual = frontier.pop(0)
  edo_actual = nodo_actual[0]
  nivel_actual = nodo_actual[1]
  if goal_test(edo_actual):
    return True
  elif limite > nivel_actual:
    x = edo_actual[0]
    y = edo_actual[1]
    offspring = expandir(x, y)
    offspring = asignar_nivel(offspring, nivel_actual+1)
    frontier = recorrerOffspring(offspring, frontier)
    return b_profundidadLim(frontier, limite)

def asignar_nivel(offspring, nivel):
  listatemp = []
  for i in offspring:
    listatemp.append((i, nivel))
  return listatemp

def b_profundidadIterada():
  limite = 2
  while True:
    frontera = [(Inicio, 1)]
    resultado = b_profundidadLim(frontera.copy(), limite)
    if resultado:
      break
    visitados.clear()
    limite += 2

###################################################
### Búsqueda voraz y A*
###################################################

def busqueda_a(frontera):
  estado_actual = frontera.pop(0)
  if goal_test(estado_actual):
    return estado_actual
  else:
    offspring = expandir(estado_actual[0], estado_actual[1])
    offspring = verifica_a(offspring) 
    offspring = ordenar(offspring)  
    if offspring[0][0][0] == estado_actual[0] and offspring[0][0][1] == estado_actual[1]:
      frontera.append(offspring[1][0])  
    else:
      frontera.append(offspring[0][0])  
    return busqueda_a(frontera)

def verifica_a(offspring):
  evaluados = []
  for hijo in offspring:
    parte1 = math.sqrt((hijo[0] - Inicio[0]) ** 2 + (hijo[1] - Inicio[1])**2)
    parte2 = math.sqrt((hijo[0] - Fin[0]) ** 2 + (hijo[1] - Fin[1])**2)
    distancia = parte1 + parte2
    evaluados.append((hijo, distancia))
  return evaluados

def verifica_voraz(offspring):
  evaluados = []
  for hijo in offspring:
    distancia = math.sqrt((hijo[0] - Fin[0]) ** 2 + (hijo[1] - Fin[1])**2)
    evaluados.append((hijo, distancia))
  return evaluados

def funcionObligatoriaParaOrdenar(x):
  return x[1]

def ordenar(hijos):
  hijos.sort(key = funcionObligatoriaParaOrdenar)
  return hijos

def busqueda_voraz(frontera):
  estado_actual = frontera.pop(0)
  if goal_test(estado_actual):
    return estado_actual
  else:
    offspring = expandir(estado_actual[0], estado_actual[1])
    offspring = verifica_voraz(offspring) 
    offspring = ordenar(offspring)  
    frontera.append(offspring[0][0])  
    return busqueda_voraz(frontera)

###################################################
### Resto del programa
###################################################

def goal_test(edo_actual):
  if(edo_actual[0] == Fin[0] and edo_actual[1] == Fin[1]):
    #print(f'Meta encontrada: {edo_actual}')
    global contador
    global puntoAnterior
    contador+= abs(edo_actual[0] - puntoAnterior[0]) + abs(edo_actual[1] - puntoAnterior[1])
    return True
  else:
    return False


def hazTablero(porcentaje, x_max, y_max):
  global Tablero
  global Inicio
  global Fin
  global visitados
  global puntoAnterior
  visitados = []

  porcentajeReal = porcentaje / 100
  cero = 1 - porcentajeReal
  matriz = np.random.choice(2, p=[cero, porcentajeReal], size=(x_max, y_max))

  inicioX = math.floor(random.random() * x_max)
  inicioY = math.floor(random.random() * y_max)
  matriz[inicioX][inicioY] = 5
  Inicio = [inicioX, inicioY]
  puntoAnterior = Inicio.copy()

  metaX = math.floor(random.random() * x_max)
  metaY = math.floor(random.random() * y_max)
  matriz[metaX][metaY] = 4
  Fin = [metaX, metaY]

  Tablero = matriz

  return matriz

def mostrarTablero(matriz):
  plt.matshow(matriz)
  plt.show()

def actualizarTabla():
  global x_max
  global y_max
  global porcentaje
  print('Teclee el tamaño horizontal del tablero: ')
  x = input(x_max)
  if len(x) > 0:
    x = int(x)
  else:
    x = x_max
  print('Teclee el tamaño vertical del tablero: ')
  y = input(y_max)
  if len(y) > 0:
    y = int(y)
  else:
    y = y_max
  print('Teclee el porcentaje de obstáculos: ')
  p = input(porcentaje)
  if len(p) > 0:
    p = int(p)
  else:
    p = porcentaje
  try:
    hazTablero(p, x, y)
    x_max = x
    y_max = y
    porcentaje = p
    print('\nLa tabla ha sido actualizada exitosamente')
  except:
    print('Error al actualizar la tabla')

def reestablecerTabla(matriz):
  global visitados
  global puntoAnterior
  puntoAnterior = Inicio.copy()
  visitados = []
  for i in range(len(matriz)):
    for j in range(len(matriz[0])):
      if matriz[i][j] == 2:
        matriz[i][j] = 0

def buscaEnTodas(puntoInicial):
  global contador
  global puntoAnterior
  contador = 0
  minimo = 0
  mejorBusqueda = 1
  reestablecerTabla(Tablero)
  print('Haciendo el recorrido en los métodos...')
  print('[                                    ]')
  busqueda_ancho([puntoInicial]) #1
  minimo = contador
  contador = 0
  reestablecerTabla(Tablero)
  print('[******                              ]')
  b_profundidad([Inicio]) #2
  if minimo > contador:
    minimo = contador
    mejorBusqueda = 2
  contador = 0
  reestablecerTabla(Tablero)
  print('[************                        ]')
  b_profundidadLim([(Inicio, 1)], 420666) #3
  if minimo > contador:
    minimo = contador
    mejorBusqueda = 3
  contador = 0
  reestablecerTabla(Tablero)
  print('[******************                  ]')
  b_profundidadIterada() #4
  if minimo > contador:
    minimo = contador
    mejorBusqueda = 4
  contador = 0
  reestablecerTabla(Tablero)
  print('[************************            ]')
  anteriorMinimo = minimo
  anteriorMejor = mejorBusqueda
  try:
    busqueda_voraz([Inicio]) #5
    if minimo > contador:
      minimo = contador
      mejorBusqueda = 5
    contador = 0
    reestablecerTabla(Tablero)
  except:
    print('falló la búsqueda voraz')
    minimo = anteriorMinimo
    mejorBusqueda = anteriorMejor
  anteriorMinimo = minimo
  anteriorMejor = mejorBusqueda
  print('[******************************      ]')
  try:
    busqueda_a([Inicio]) #6
    if minimo > contador:
      minimo = contador
      mejorBusqueda = 6
    contador = 0
    reestablecerTabla(Tablero)
  except:
    print('falló la búsqueda A*')
    minimo = anteriorMinimo
    mejorBusqueda = anteriorMejor
  print('[************************************]\n')
  if mejorBusqueda == 1:
    print('Búsqueda a lo ancho es lo mejor') #lmao, esto jamás pasará
    busqueda_ancho([Inicio])
  elif mejorBusqueda == 2:
    print('Búsqueda profunda es la mejor') #lmao, esto jamás pasará
    b_profundidad([Inicio])
  elif mejorBusqueda == 3:
    print('Búsqueda de profundidad limitada es la mejor') #lmao, esto jamás pasará
    b_profundidadLim([(Inicio, 1)], 420666)
  elif mejorBusqueda == 4:
    print('Búsqueda de profundidad iterada es la mejor') #lmao, esto jamás pasará
    b_profundidadIterada()
  elif mejorBusqueda == 5:
    print('Búsqueda voraz es la mejor') #puede ser
    busqueda_voraz([Inicio])
  elif mejorBusqueda == 6:
    print('Búsqueda de a* es la mejor') #quizá
    busqueda_a([Inicio])
  print(f'Movimientos: {minimo}')
  mostrarTablero(Tablero)

###################################################
### Main
###################################################

def Busqueda():
  linea = '###################################################'
  global x_max
  global y_max
  global porcentaje
  global contador
  contador = 0
  x_max = y_max = 100
  porcentaje = 15
  opcion = -1
  hazTablero(porcentaje, x_max, y_max)
  while opcion != 0:
    reestablecerTabla(Tablero)
    while opcion < 0 or opcion > 7:
      print(f'\n{linea}\n')
      print('Seleccione una opción del menú.')
      print('\t1: Búsqueda ancho')
      print('\t2: Búsqueda profundo')
      print('\t3: Búsqueda profundidad limitada')
      print('\t4: Búsqueda profundidad iterada')
      print('\t5: Búsqueda voraz')
      print('\t6: Búsqueda A*')
      print('\t7: Modificar tabla')
      print('\t8: Información de tabla')
      print('\t9: Obtener la mejor búsqueda')
      print('')
      print('\t0: Salir')

      opcion = input('Opción: ')
      if(len(opcion) == 0):
        opcion = -1
        continue
      opcion = int(opcion)
      if 0 <= opcion <= 7:
        break
      elif opcion == 8:
        print(f'\n{linea}\n')
        print(f'Tabla\n\t{porcentaje}% de obtáculos')
        print(f'\tDimensiones {x_max}x{y_max}')
      elif opcion == 9:
        buscaEnTodas(Inicio)
      else:
        print('\nSólo se aceptan valores del 0 al 8')

    print(f'\n{linea}\n')
    if opcion == 1:
      print('Búsqueda a lo ancho')
      busqueda_ancho([Inicio])
    elif opcion == 2:
      print('Búsqueda profundo')
      b_profundidad([Inicio])
    elif opcion == 3:
      print('Búsqueda profundidad limitada')
      b_profundidadLim([(Inicio, 1)], 420666)
    elif opcion == 4:
      print('Búsqueda profundidad iterada')
      b_profundidadIterada()
    elif opcion == 5:
      print('Búsqueda voraz')
      try:
        busqueda_voraz([Inicio])
      except:
        print('falló la búsqueda voraz')
    elif opcion == 6:
      print('Búsqueda A*')
      try:
        busqueda_a([Inicio])
      except:
        print('falló la búsqueda A*')
    elif opcion == 7:
      actualizarTabla()
    else:
      print('y se marchó, y a su barco le llamó libertad')
      break

    if 0 < opcion < 7:
      #print(Tablero)
      mostrarTablero(Tablero)
      #print(visitados)

    opcion = -1
    print('\n')


if __name__ == '__main__':
  sys.setrecursionlimit(100000)
  Busqueda()
