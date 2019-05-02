from tda_grafo import Grafo
from otros_tdas import Pila,Cola,Heap
import operator
import random



# Auxiliares Camino Mínimo / Vacaciones / Caminos con Menor Cantidad de Escalas


def calcular_camino(padres,destino,dist=None):
	camino = [destino]
	vertice = destino
	while True:
		if not vertice in padres: return None,None
		vertice = padres[vertice]
		camino.insert(0,vertice)
		if not padres[vertice]:
			if dist: return camino,dist[destino]
			return camino


def camino_minimo_dijkstra(grafo,origen,destino,parametro,invertir_parametro):
	''' Devuelve el camino mínimo a partir de un vértice origen.
		El parámetro destino es opcional, si se agrega devuelve el camino mínimo entre el origen y el destino.
		Si no se agrega, devuelve dos diccionarios, uno de padres y otro de distancias mínimas.
	'''
	dist = {}
	padres = {}
	for vertice in grafo.obtener_vertices():
		dist[vertice] = float("+inf")
	dist[origen] = 0
	padres[origen] = None
	heap = Heap(3)
	heap.encolar([origen,dist[origen]])
	while not heap.esta_vacio():
		vertice,distancia = heap.desencolar()
		if destino and vertice == destino: return calcular_camino(padres,destino,dist)
		for adyacente in grafo.obtener_adyacentes(vertice):
			peso_conexion = int(grafo.obtener_informacion(vertice,adyacente)[parametro])
			if invertir_parametro: peso_conexion = 1/peso_conexion
			if distancia + peso_conexion < dist[adyacente]:
				dist[adyacente] = distancia + peso_conexion
				padres[adyacente] = vertice
				heap.actualizar([adyacente,dist[adyacente]])
	return padres,dist


def camino_minimo_bfs(grafo,vertice_inicial,vertice_final):
	''' Devuelve el camino mínimo a partir de un vértice origen.
		Devuelve dos diccionarios, uno de padres y otro de distancias mínimas (orden).
	'''
	visitados = set()
	padres = {}
	orden = {}
	cola = Cola()
	visitados.add(vertice_inicial)
	padres[vertice_inicial] = None
	orden[vertice_inicial] = 0
	cola.encolar(vertice_inicial)
	while not cola.esta_vacia():
		vertice = cola.desencolar()
		adyacentes = grafo.obtener_adyacentes(vertice)
		if not adyacentes:
			continue
		for adyacente in adyacentes:
			if not adyacente in visitados:
				visitados.add(adyacente)
				padres[adyacente] = vertice
				orden[adyacente] = orden[vertice]+1
				cola.encolar(adyacente)
				if adyacente == vertice_final:
					return padres, orden[adyacente]


# Auxiliares Nueva Aerolínea


def arbol_de_tendido_minimo(grafo,parametro,origen):
	# Devuelve el árbol de tendido mínimo de un grafo
	visitados = set()
	visitados.add(origen)
	heap = Heap(2)
	vertice = origen
	for adyacente in grafo.obtener_adyacentes(vertice):
		lista_de_info = grafo.obtener_informacion(vertice,adyacente)
		peso_arista = lista_de_info[parametro]
		heap.encolar([vertice,adyacente,peso_arista])
	arbol = Grafo()
	while not heap.esta_vacio():
		vertice,adyacente,peso = heap.desencolar()
		if adyacente in visitados: continue
		arbol.agregar_arista(vertice,adyacente,[peso])
		if adyacente == destino: break
		visitados.add(adyacente)
		for nuevo_adyacente in grafo.obtener_adyacentes(adyacente):
			if not nuevo_adyacente in visitados:
				lista_de_info = grafo.obtener_informacion(adyacente,nuevo_adyacente)
				peso_arista = lista_de_info[parametro]
				heap.encolar([adyacente,nuevo_adyacente,peso_arista])
	return arbol


# Auxiliares Vacaciones


def lugares_orden_n(grafo,origen,n):
	# Devuelve el camino a un aeropuerto que se encuentra a n-1 vuelos del origen, None en caso de que éste no exista
	camino = [origen]
	visitados = [origen]
	for adyacente in grafo.obtener_adyacentes(origen):
		if _lugares_orden_n(grafo,origen,adyacente,n,visitados,camino):
			return camino
	return None



def _lugares_orden_n(grafo,origen,vertice,n,visitados,camino):
	# (Rec) Devuelve el camino a un aeropuerto que se encuentra a n-1 vuelos del origen, None en caso de que éste no exista
	if len(camino)-1 == n: return True
	if len(visitados) == len(grafo.obtener_vertices()): return False
	if n == 1:
		if origen in grafo.obtener_adyacentes(vertice):
			camino.append(vertice)
			return True
	if n <= 1:
		return False
	visitados.append(vertice)
	for adyacente in grafo.obtener_adyacentes(vertice):
		if not adyacente in visitados:
			if _lugares_orden_n(grafo,origen,adyacente,n-1,visitados,camino): 
				camino.insert(1,vertice)
				return True
	visitados.remove(vertice)
	return False


# Auxiliares Centralidad Exacta

def ordenar_vertices(grafo,distancias):
	# Devuelve una lista de los vértices del grafo ordenados de mayor a menor por distancia
	resultado = []
	for vertice in grafo.obtener_vertices():
		distancia = distancias[vertice]
		resultado.append([vertice,distancia])
	resultado.sort(key=operator.itemgetter(1),reverse=True)
	return resultado

def calcular_centralidad(grafo,parametro):
    cent = {}
    for vertice in grafo: cent[vertice] = 0
    for vertice_1 in grafo:
    	padres,distancias = camino_minimo_dijkstra(grafo,vertice_1,None,parametro,True)
    	cent_aux = {}
    	for vertice_2 in grafo: cent_aux[vertice_2] = 0
    	vertices_ordenados = ordenar_vertices(grafo,distancias)
    	for vertice_2,distancia in vertices_ordenados:
    		if padres[vertice_2]:
    			cent[padres[vertice_2]] += cent_aux[vertice_2] + 1
    	for vertice_2 in grafo:
    		if vertice_2 == vertice_1: continue
    		cent[vertice_2] += cent_aux[vertice_2]
    return cent

# Auxiliares Generales

def imprimir_camino(camino,incluir_vertice_inicial):
	# Imprime un camino que ingresa como lista. Si el segundo es parámetro es True, agrega al final el vértice inicial (vacaciones)
	if not camino: return
	if incluir_vertice_inicial: camino.append(camino[0])
	cadena = (' -> ').join(vertice for vertice in camino)
	print(cadena)


def orden_topologico(grafo):
	grados = {}
	for v in grafo: 
		grados[v] = 0
	for v in grafo:
		for w in grafo.obtener_adyacentes(v):
			grados[w]+=1
	cola_aux = Cola()
	for v in grafo:
		if grados[v] == 0:
			cola_aux.encolar(v)
	resultado = []
	while not cola_aux.esta_vacia():
		v = cola_aux.desencolar()
		resultado.append(v)
		for w in grafo.obtener_adyacentes(v):
			grados[w]-=1
			if grados[w]==0:
				cola_aux.encolar(w)
	if len(resultado) == grafo.cantidad_vertices():
		return resultado
	else:
		return None

def obtener_tiempo(grafo,vertice,conexion):
	if not grafo.obtener_informacion(vertice,conexion): return None
	return int(grafo.obtener_informacion(vertice,conexion)[0])

def obtener_precio(grafo,vertice,conexion):
	if not grafo.obtener_informacion(vertice,conexion): return None
	return int(grafo.obtener_informacion(vertice,conexion)[1])

def obtener_cant_vuelos(grafo,vertice,conexion):
	if not grafo.obtener_informacion(vertice,conexion): return None
	return int(grafo.obtener_informacion(vertice,conexion)[2])



