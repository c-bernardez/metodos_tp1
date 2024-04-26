# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None #nodo padre
        self.longitud = 0 
        
        self.current = self.Nodo(None, self.raiz) #el primer elemento tomará el valor: par(c,n)

    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)    
    
        nuevoNodo = self.Nodo( valor, self.raiz ) #crea el nodo
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:      
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self
    
    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None
        
        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')
        
        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')
            
        return nodoActual
        
    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor
    
    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor
            self.siguiente = siguiente


class MatrizRala:
    def __init__( self, M, N ):
        self.filas = {} #diccionario con filas como clave
        self.shape = (M, N)

    def __getitem__(self, Idx):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        m, n = Idx
        if m in self.filas: 
            fila = self.filas[m]
            nodo_actual = fila.raiz
            while nodo_actual is not None:
                columna, valor = nodo_actual.valor
                if columna == n:
                    return valor
                nodo_actual = nodo_actual.siguiente
        return 0

        
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        m, n = Idx
        if m in self.filas:
            fila = self.filas[m]
            nodo_actual = fila.raiz
            nodo_anterior = None
            while nodo_actual is not None: 
                columna = nodo_actual.valor[0] 
                if columna == n:
                    nodo_actual.valor = (n, v)  #si el nodo ya tiene un valor, se actualiza
                    return
                elif columna > n:
                    if nodo_anterior is None:
                        fila.insertarFrente((n, v))  # Inserta al frente si es el primer nodo en la fila
                    else:
                        fila.insertarDespuesDeNodo((n, v), nodo_anterior)  # Inserta después del nodo anterior
                    return
                nodo_anterior = nodo_actual
                nodo_actual = nodo_actual.siguiente
            fila.push((n, v)) #si se termina la lista, se inserta al final
        else:
            # Si la fila no existe, crea una nueva fila con un solo nodo
            nueva_fila = ListaEnlazada()
            nueva_fila.insertarFrente((n, v))
            self.filas[m] = nueva_fila

    def __mul__( self, k ):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        resultado = MatrizRala(*self.shape)
        
        # Recorrer cada elemento de la matriz actual
        for fila, lista_enlazada in self.filas.items():
            nodo_actual = lista_enlazada.raiz
            while nodo_actual is not None:
                columna, valor = nodo_actual.valor
                # Multiplicar el valor por el escalar k y asignarlo en la nueva matriz
                resultado.__setitem__((fila, columna), valor * k)
                nodo_actual = nodo_actual.siguiente
                
        return resultado
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise ValueError("Las matrices deben tener la misma forma para poder sumarlas")
        
        resultado = MatrizRala(*self.shape)  # Crear una nueva matriz para almacenar el resultado

        for m, fila in self.filas.items():
            # Iterar sobre los elementos de la fila
            for n in range(self.shape[0]):
                nodo_enA = self.__getitem__((m, n))
                nodo_enB = other.__getitem__((m,n))
                resultado.__setitem__((m,n), nodo_enA + nodo_enB)

        #Iterar sobre las filas de la matriz other para agregar elementos que no están en la matriz self
        for m, fila in other.filas.items():
            if m not in self.filas:
                resultado.filas[m] = fila  # Copia la fila completa desde other a result 
    
        return resultado
    
    def __sub__( self, other ):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        #restar es sumar la inversa
        negative_other = other.__mul__(-1)
        resultado = self.__add__(negative_other)
        return resultado
    
    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]: # cant col A debe ser igual a cant fila B
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación matricial")

        # Crear una nueva instancia de la matriz resultante
        resultado = MatrizRala(self.shape[0], other.shape[1])       

        # Iterar sobre las filas de la matriz self
        for i in range(self.shape[0]):
            # Iterar sobre las columnas de la matriz other
            for j in range(other.shape[1]):
                # Calcular el valor del elemento (i, j) en la matriz resultante
                valor = 0
                for k in range(self.shape[1]): 
                    valor += self.__getitem__((i, k)) * other.__getitem__((k, j))
                    print(i, j, self.__getitem__((i, k)) , other.__getitem__((k, j)))

                # Asignar el valor calculado al elemento (i, j) en la matriz resultante
                resultado.__setitem__((i, j), valor)

        return resultado
        
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res

def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    pass


A = MatrizRala(2, 3)
B = MatrizRala(3, 2)

A[0, 0] = 1
A[0, 1] = 2
A[1, 2] = 3

B[0, 1] = 4
B[1, 0] = 5

C = A @ B
print(A)
print(B)
print(C)