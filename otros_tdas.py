import operator

class Cola:
    def __init__(self):
        self.estado = []
    def encolar(self,elemento):
        self.estado.append(elemento)
    def desencolar(self):
    	if self.esta_vacia():
    		raise IndexError("La cola está vacía")
    	return self.estado.pop(0)
    def ver_primero(self):
        return self.estado[0]
    def esta_vacia(self):
        return len(self.estado) == 0
    def ordenar(self,metodo):
        lista = quick_sort_metodo(self.estado,metodo)

class Heap:
    def __init__(self,tipo_de_heap):
        '''
        tipo 0: Heap de Máximos
        tipo 1: Heap de Mínimos
        tipo 2: Heap de Prim (listas(mín))
        '''
        self.estado = []
        self.tipo = tipo_de_heap
        self.cantidad = 0

    def __str__(self):
        cadena = "["
        separador = ""
        for elemento in self.estado:
            cadena += separador + str(elemento)
            separador = ","
        cadena += "]"
        return cadena

    def encolar(self,elemento):
        self.estado.append(elemento)
        self.cantidad +=1
        if self.tipo == 0:
            self.estado.sort(reverse=True)
        elif self.tipo == 1:
            self.estado.sort(reverse=False)
        elif self.tipo == 2:
            self.estado.sort(key=operator.itemgetter(2))
        elif self.tipo == 3:
            self.estado.sort(key=operator.itemgetter(1))

    def actualizar(self,elemento):
        vertice = elemento[0]
        for cada_elemento in self.estado:
            if cada_elemento[0] == vertice:
                cada_elemento[1] = elemento[1]
                return True
        self.encolar(elemento)
        return False
        
    def desencolar(self):
        if self.esta_vacio():
            raise IndexError("La cola está vacía")
        self.cantidad -=1
        return self.estado.pop(0)
    def ver_max(self):
        return self.estado[0]
    def cantidad(self):
        return self.cantidad
    def esta_vacio(self):
        return len(self.estado) == 0
    def ordenar(self,metodo):
        lista = quick_sort_metodo(self.estado,metodo)




class Pila:
    def __init__(self):
        self.estado = []
    def apilar(self,elemento):
        self.estado.append(elemento)
    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.estado.pop()
    def ver_ultimo(self):
        return self.estado[len(self.estado)-1]
    def esta_vacia(self):
        return len(self.estado) == 0
    def largo(self):
        pila_aux = Pila()
        contador = 0
        while not self.esta_vacia():
            pila_aux.apilar(self.desapilar())
            contador += 1
        while not pila_aux.esta_vacia():
            self.apilar(pila_aux.desapilar())
        return contador


class LE:
    def __init__(self,prim = None):
        self.prim = prim

    def __str__(self):
        cadena = '['
        separador = ''
        nodo = self.prim
        while nodo:
            cadena += separador + str(nodo.dato)
            separador = ','
            nodo = nodo.prox
        return cadena + ']'

    def __iter__(self):
        return _IteradorListaEnlazada(self.prim)

    def insertar_ordenado(self,elemento):
        nodo = self.prim
        if not self.prim:
            self.prim = Nodo(elemento,None)
        else:
            while nodo.prox.dato < elemento:
                nodo = nodo.prox
            nodo.prox = Nodo(elemento,nodo.prox)

    def append(self,nodo):
        nodo_aux = Nodo(nodo.dato)
        if not self.prim:
            self.prim = nodo_aux
        else:
            actual = self.prim
            while actual.prox:
                actual = actual.prox
            actual.prox = nodo_aux

    def hacer_circular(self):
        if self.prim:
            actual = self.prim
            while actual.prox:
                actual = actual.prox
            actual.prox = self.prim

    def deshacer_circular(self):
        if self.prim:
            actual = self.prim
            while actual.prox != self.prim:
                actual = actual.prox
            actual.prox = None

    def reduce(self,funcion):
        if not self.prim:
            raise Exception("La lista esta vacia")
        resultado = 0
        actual = self.prim
        while actual:
            if actual.prox:
                resultado += funcion(actual.dato,actual.prox.dato)
                actual = actual.prox.prox
            else:
                resultado += funcion(actual.dato)
                actual = actual.prox
        return resultado

class _IteradorListaEnlazada:
    def __init__(self, prim):
        self.actual = prim

    def __next__(self):
        if not self.actual:
            raise StopIteration()
        dato = self.actual.dato
        self.actual = self.actual.prox
        return dato


class Nodo:
    def __init__(self,dato,prox = None):
        self.dato = dato
        self.prox = prox


N3 = Nodo(3)
N2 = Nodo(2,N3)
N1 = Nodo(1,N2)


def quick_sort_metodo(lista,metodo):
    if len(lista) <= 1:
        return lista
    pivote = lista[0]
    menores = []
    mayores = []
    for i in range(1,len(lista)):
        if lista[i].metodo > pivote.metodo:
            menores.append(lista[i])
        else:
            mayores.append(lista[i])
    return quick_sort_metodo(menores)+[pivote]+quick_sort_metodo(mayores)



