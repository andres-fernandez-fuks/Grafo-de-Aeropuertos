#!/usr/bin/python3
import interfaz
import sys

def main():
	cant_parametros = len(sys.argv)
	if cant_parametros < 3 or cant_parametros >= 5:
		print("Cantidad de parámetros incorrecta")
		return
	else:
		archivo_aeropuertos = sys.argv[1]
		archivo_vuelos = sys.argv[2]
	info_ciudad_aeropuertos,info_aeropuertos_pos = interfaz.establecer_datos_aeropuertos(archivo_aeropuertos)
	grafo = interfaz.establecer_datos_vuelos(archivo_vuelos)
	ultimo_camino = []
	while True:
		try:
			input_linea = input()
			if not input_linea: break
		except EOFError: return
		resultado = interfaz.recibir_comandos(input_linea,info_ciudad_aeropuertos,grafo,info_aeropuertos_pos,ultimo_camino)
		if resultado:
			ultimo_camino = resultado

main()



 
