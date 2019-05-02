'''
El grafo está implementado como un diccionario de diccionarios:
	- Cada vértice es una clave del diccionario principal, y su valor es un diccionario
	- Cada adyacente de un vértice es una clave del diccionario correspondiente al vértice
	- Los valores de los diccionarios secundarios son listas [tiempo_promedio,precio,vuelos]
'''

import random

class Grafo:
	'''
	tipo 0 grafo no dirigido
	tipo 1 grafo dirigido
	'''
	def __init__(self,tipo_de_grafo):
		self.vertices = {}
		self.cant_vertices = 0
		self.cant_aristas = 0
		self.tipo = tipo_de_grafo

	def __iter__(self):
		return iter(self.vertices)

	def __str__(self):
		cadena = ''
		for vertice in self.vertices.keys():
			cadena += vertice + ':\n'
			for conexion in self.vertices[vertice].keys():
				cadena += conexion + ' - '
				info = ' - '.join(str(campo) for campo in self.vertices[vertice][conexion])
				cadena += info
				if (cadena[-1:] != '\n'): cadena += '\n'
			cadena += '\n'	
		return cadena[:-2]

	def agregar_vertice(self,vertice):
		if not vertice in self.vertices:
			self.vertices[vertice] = {}
			self.cant_vertices +=1

	def borrar_vertice(self,vertice):
		self.vertices.pop(vertice)

	def agregar_arista(self,vertice_1,vertice_2,peso):
		if not vertice_1 in self.vertices:
			self.agregar_vertice(vertice_1)
		if not vertice_2 in self.vertices:
			self.agregar_vertice(vertice_2)
		if not vertice_2 in self.vertices[vertice_1] or int(peso[1]) < int(self.vertices[vertice_1][vertice_2][1]):
			self.vertices[vertice_1][vertice_2] = peso
			if self.tipo == 0:
				self.vertices[vertice_2][vertice_1] = peso
		self.cant_aristas +=1

	def borrar_arista(self,arista):
		vertice = lista_de_info[0]
		conexion = lista_de_info[1]
		if (not vertice in self.vertices or not conexion in self.vertices[vertice]):
			return None
		return self.vertices[vertice].pop(conexion)

	def vertice_en_grafo(self,vertice):
		return vertice in self.vertices

	def obtener_informacion(self,vertice,conexion):
		if not vertice in self.vertices or not conexion in self.vertices[vertice]:
			return None
		return self.vertices[vertice][conexion]

	def obtener_vertices(self):
		return self.vertices.keys()

	def obtener_vertice_aleatorio(self):
		return random.choice(list(self.vertices))

	def obtener_adyacentes(self,vertice):
		if (not vertice in self.vertices):
			return []
		return self.vertices[vertice].keys()

	def cantidad_vertices(self):
		return self.cant_vertices

	def cantidad_aristas(self):
		return self.cant_aristas








