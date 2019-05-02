from tda_grafo import Grafo
from otros_tdas import Pila,Cola,Heap
import operator
import random
import auxiliares_lib


# Listar Operaciones

def listar_operaciones():
	for operacion in ['camino_mas','centralidad','vacaciones','camino_escalas','nueva_aerolinea','itinerario','exportar_kml']: print(operacion)

# Camino más rápido/barato (★)

def camino_mas(grafo,parametro,ciudad_origen,ciudad_destino,info_ciudad_aeropuerto):
	camino_minimo = None;
	peso_minimo = float("+inf")
	if parametro == 'barato':
		num_param = 1
	else: num_param = 0
	for aero_origen in info_ciudad_aeropuerto[ciudad_origen]:
		for aero_destino in info_ciudad_aeropuerto[ciudad_destino]:
			camino,peso_total = auxiliares_lib.camino_minimo_dijkstra(grafo,aero_origen,aero_destino,num_param,False)
			if not camino:
				print("Las ciudades no pueden conectarse")
				return
			if peso_total < peso_minimo:
				camino_minimo = camino
				peso_minimo = peso_total
	auxiliares_lib.imprimir_camino(camino_minimo,False)
	return camino


# Camino con menor cantidad de escalas (★)

def camino_escalas(grafo, ciudad_origen,ciudad_destino,info_ciudad_aeropuerto):
	cantidad_minima = float("+inf")
	padres_minimos = {}
	for aero_origen in info_ciudad_aeropuerto[ciudad_origen]:
		for aero_destino in info_ciudad_aeropuerto[ciudad_destino]:
			padres,cantidad_de_escalas = auxiliares_lib.camino_minimo_bfs(grafo,aero_origen,aero_destino)
			if cantidad_de_escalas < cantidad_minima:
				padres_minimos = padres
				cantidad_minima = cantidad_de_escalas
				aero_origen_optimo = aero_origen
				aero_destino_optimo = aero_destino
	camino = auxiliares_lib.calcular_camino(padres_minimos,aero_destino_optimo)
	if not camino: print("No se encontro recorrido")
	else: auxiliares_lib.imprimir_camino(camino, False)
	return camino


#Itinerario cultural (★★)


import csv
def itinerario_cultural(grafo,ruta,info_ciudad_aeropuerto):
	restricciones = Grafo(1)
	with open(ruta) as archivo:
		datos_csv = csv.reader(archivo)
		lugares = next(datos_csv)
		for lugar in lugares:
			restricciones.agregar_vertice(lugar)
		for destino_necesario, destino in datos_csv:
			restricciones.agregar_arista(destino_necesario, destino, 0)
	itinerario = auxiliares_lib.orden_topologico(restricciones)
	resultado = ", ".join(destino for destino in itinerario)
	print(resultado)
	origen = itinerario[0]
	camino = []
	for destino in itinerario[1:]:
		camino.extend(camino_mas(grafo,"barato", origen, destino,info_ciudad_aeropuerto))
		origen = destino
	return camino


# Optimización de rutas para nueva aerolínea (★★)

def nueva_aerolinea(grafo,ruta_de_salida):
	visitados = set()
	origen = grafo.obtener_vertice_aleatorio()
	visitados.add(origen)
	heap = Heap(2)
	vertice = origen
	for adyacente in grafo.obtener_adyacentes(vertice):
		peso_arista = auxiliares_lib.obtener_precio(grafo,vertice,adyacente)
		heap.encolar([vertice,adyacente,peso_arista])
	with open(ruta_de_salida,'w') as archivo:
		while not heap.esta_vacio():
			vertice,adyacente,peso = heap.desencolar()
			if adyacente in visitados: continue
			tiempo,precio,cant_de_vuelos = grafo.obtener_informacion(vertice,adyacente)
			archivo.write(vertice+","+adyacente+","+tiempo+","+precio+","+cant_de_vuelos)
			visitados.add(adyacente)
			for nuevo_adyacente in grafo.obtener_adyacentes(adyacente):
				if not nuevo_adyacente in visitados:
					peso_arista = auxiliares_lib.obtener_precio(grafo,adyacente,nuevo_adyacente)
					heap.encolar([adyacente,nuevo_adyacente,peso_arista])
		print("OK")


# Vacaciones (★★★)

def vacaciones(grafo,origen,n,info_ciudad_aeropuerto):
	camino = None
	for aeropuerto_origen in info_ciudad_aeropuerto[origen]:
		camino = auxiliares_lib.lugares_orden_n(grafo,aeropuerto_origen,n-1)
		if camino: break
	if not camino: print("No se encontro recorrido")
	else: auxiliares_lib.imprimir_camino(camino,True)
	return camino


# Centralidad (★★★)

def centralidad(grafo,n):
	lista = []
	centralidad = auxiliares_lib.calcular_centralidad(grafo,2)
	for aeropuerto in centralidad:
		lista.append([aeropuerto,centralidad[aeropuerto]])
		lista.sort(key=operator.itemgetter(1),reverse=True)
	cadena = ""
	separador = ""
	for i in range(0,n):
		cadena += separador + lista[i][0]
		separador = ", "
	print(cadena)
