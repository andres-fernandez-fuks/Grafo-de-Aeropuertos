import os
import grafos_lib
from tda_grafo import Grafo

def establecer_datos_aeropuertos(nom_archivo):
	'''
	Devuelve dos diccionarios:
	- Uno con ciudades como clave y una lista de aeropuertos como valor
	- Uno con aeropuertos como clave y el tiempo_promedio y el precio de vuelos como valor
	'''
	dir_actual = os.getcwd()
	ruta_archivo = dir_actual + "/" + nom_archivo
	info_ciudad_aeropuertos = {}
	info_aeropuertos_pos = {}
	with open(ruta_archivo) as archivo_aeropuertos:
		for linea in archivo_aeropuertos:
			lista_de_info = linea.split(',')
			ciudad,aeropuerto = lista_de_info[0],lista_de_info[1]
			info_aeropuertos_pos[aeropuerto] = lista_de_info[2],lista_de_info[3].rstrip("\n")
			info_ciudad_aeropuertos[ciudad] = info_ciudad_aeropuertos.get(ciudad,[]) + [aeropuerto]
	return info_ciudad_aeropuertos, info_aeropuertos_pos

def establecer_datos_vuelos(nom_archivo):
	'''
	Devuelve un grafo armado a partir de un archivo de vuelos entre aeropuertos.
	La información que contienen las aristas es una lista [tiempo_promedio,precio,cant_vuelos]
	'''
	dir_actual = os.getcwd()
	ruta_archivo = dir_actual + "/" + nom_archivo
	grafo = Grafo(0)
	with open(ruta_archivo) as archivo_vuelos:
		for linea in archivo_vuelos:
			lista_de_info = linea.split(',')
			aero_1,aero_2 = lista_de_info[0],lista_de_info[1]
			informacion = [lista_de_info[2],lista_de_info[3],lista_de_info[4]]
			grafo.agregar_vertice(aero_1)
			grafo.agregar_arista(aero_1,aero_2,informacion)
	return grafo


def separar_input_camino_mas(input_string):
	resultado = ["camino_mas"]
	parametro = input_string[11:17]
	if parametro != "rapido" and parametro != "barato": return None
	resultado.append(parametro)
	input_list = input_string.split(",")
	if len(input_list) != 3: return None
	ciudad_1 = input_list[1]
	ciudad_2 = input_list[2]
	resultado.append(ciudad_1)
	resultado.append(ciudad_2)
	return resultado

def separar_input_camino_escalas(input_string):
	resultado = ["camino_escalas"]
	parametros = input_string[input_string.find(" ")+1:]
	parametros_lista = parametros.split(",")
	if len(parametros_lista) != 2: return None
	for parametro in parametros_lista: resultado.append(parametro)
	return resultado

def separar_input_centralidad(input_string):
	resultado = input_string.split(" ")
	if len(resultado) != 2 or not resultado[1].isdigit(): return None
	resultado[1] = int(resultado[1])
	return resultado

def separar_input_nueva_aerolinea(input_string):
	resultado = input_string.split(" ")
	if len(resultado) != 2: return None
	return resultado

def separar_input_vacaciones(input_string):
	resultado = ["vacaciones"]
	origen = input_string[input_string.find(" ")+1:input_string.find(",")]
	n = input_string[input_string.find(",")+1:]
	if not n.isdigit(): return None
	n = int(n)
	resultado.append(origen)
	resultado.append(n)
	return resultado

def separar_input_itinerario(input_string):
	resultado = ["itinerario"]
	parametros = input_string[len("itinerario")+1:]
	parametros_lista = parametros.split(" ")
	if len(parametros_lista) != 1: return None #return validar_archivo_ciudades(resultado)
	for parametro in parametros_lista: resultado.append(parametro) 
	return resultado


def separar_input(input_string):
	if input_string.find("camino_mas") > -1:
		return separar_input_camino_mas(input_string)
	elif input_string.find("camino_escalas") >-1:
		return separar_input_camino_escalas(input_string)
	elif input_string.find("centralidad") > -1:
		return separar_input_centralidad(input_string)
	elif input_string.find("nueva_aerolinea") > -1:
		return separar_input_nueva_aerolinea(input_string)
	elif input_string.find("vacaciones") > -1:
		return separar_input_vacaciones(input_string)
	elif input_string.find("itinerario") > -1:
		return separar_input_itinerario(input_string)
	elif input_string == "listar_operaciones":
		return ['operaciones']
	else: return None

def recibir_comandos(input_linea,info_ciudad_aeropuertos,grafo,info_aeropuertos_pos,ultimo_camino):
	input_list = separar_input(input_linea)
	if not input_list:
		print("Error en Comando")
		return None
	if input_list[0] == "camino_mas":
		return grafos_lib.camino_mas(grafo,input_list[1],input_list[2],input_list[3],info_ciudad_aeropuertos)
	elif input_list[0] == "camino_escalas":
		return  grafos_lib.camino_escalas(grafo,input_list[1],input_list[2],info_ciudad_aeropuertos)
		print(ultimo_camino)
	elif input_list[0] == "centralidad":
		grafos_lib.centralidad(grafo,input_list[1])
	elif input_list[0] == "nueva_aerolinea":
		grafos_lib.nueva_aerolinea(grafo,input_list[1])
	elif input_list[0] == "vacaciones":
		return grafos_lib.vacaciones(grafo,input_list[1],input_list[2],info_ciudad_aeropuertos)
	elif input_list[0] == "itinerario":
		return grafos_lib.itinerario_cultural(grafo,input_list[1],info_ciudad_aeropuertos)
	elif input_list[0] == "operaciones":
		grafos_lib.listar_operaciones()


