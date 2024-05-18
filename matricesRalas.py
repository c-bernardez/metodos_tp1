# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 
import numpy as np
import pandas as pd
import time

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

    def __add__(self, other):
        # Esta función implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise ValueError("Las matrices deben tener la misma forma para poder sumarlas")

        resultado = MatrizRala(*self.shape)  # Crear una nueva matriz para almacenar el resultado

        # Agregar todos los elementos de la matriz self
        for m, fila in self.filas.items():
            nodo_actual = fila.raiz
            while nodo_actual is not None:
                n, valor = nodo_actual.valor
                resultado[m, n] = valor
                nodo_actual = nodo_actual.siguiente

        # Agregar todos los elementos de la matriz other
        for m, fila in other.filas.items():
            nodo_actual = fila.raiz
            while nodo_actual is not None:
                n, valor = nodo_actual.valor
                resultado[m, n] += valor  # Si el elemento ya existe en resultado, se suma
                nodo_actual = nodo_actual.siguiente

        return resultado

    
    def __sub__( self, other ):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        #restar es sumar la inversa
        negative_other = other.__mul__(-1)
        resultado = self.__add__(negative_other)
        return resultado
    
    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación matricial")

        resultado = MatrizRala(self.shape[0], other.shape[1])
        acumulados = {}

        for i, fila_a in self.filas.items():
            nodo_a = fila_a.raiz
            while nodo_a is not None:
                k, valor_a = nodo_a.valor
                if k in other.filas:
                    fila_b = other.filas[k]
                    nodo_b = fila_b.raiz
                    while nodo_b is not None:
                        j, valor_b = nodo_b.valor
                        if (i, j) not in acumulados:
                            acumulados[(i, j)] = 0
                        acumulados[(i, j)] += valor_a * valor_b
                        nodo_b = nodo_b.siguiente
                nodo_a = nodo_a.siguiente

        for (i, j), valor in acumulados.items():
            resultado[i, j] = valor

        return resultado

    def imprimir_fila(self, fila_idx):
        if fila_idx in self.filas:
            fila = self.filas[fila_idx]
            nodo_actual = fila.raiz
            while nodo_actual is not None:
                columna, valor = nodo_actual.valor
                print(f"WD[{fila_idx}, {columna}] = {valor}")
                nodo_actual = nodo_actual.siguiente
        else:
            print(f"Fila {fila_idx} no tiene elementos no nulos.")
            
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                #res += str(round(self[i,j],5)) + ' '
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res

def GaussJordan(A, b):
    m, n = A.shape
    if b.shape[0] != m or b.shape[1] != 1:
        raise ValueError("Las dimensiones de A y b no son compatibles")
    
    # Crear una matriz aumentada
    A_aug = MatrizRala(m, n + 1)
    for i in range(m):
        for j in range(n):
            A_aug[i, j] = A[i, j]
        A_aug[i, n] = b[i, 0]
    
    # print("Matriz aumentada inicial:")
    # print(A_aug)
    
    # Aplicar eliminación Gauss-Jordan
    for i in range(m):
        # Si el pivote es cero, buscar una fila para intercambiar
        if A_aug[i, i] == 0:
            swap_made = False
            for k in range(i + 1, m):
                if A_aug[k, i] != 0:
                    # Intercambiar filas
                    for j in range(n + 1):
                        A_aug[i, j], A_aug[k, j] = A_aug[k, j], A_aug[i, j]
                    swap_made = True
                    break
            if not swap_made:
                raise ValueError("La matriz A es singular y no tiene solución única")

        # Hacer el pivote igual a 1
        pivote = A_aug[i, i]
        for j in range(n + 1):
            A_aug[i, j] /= pivote

        # print(f"Después de hacer el pivote A[{i},{i}] igual a 1:")
        # print(A_aug)

        # Hacer ceros en la columna i
        for k in range(m):
            if k != i:
                factor = A_aug[k, i]
                for j in range(n + 1):
                    A_aug[k, j] -= factor * A_aug[i, j]
        
        # print(f"Después de hacer ceros en la columna {i}:")
        # print(A_aug)
    
    # Extraer la solución
    x = MatrizRala(m, 1)
    for i in range(m):
        x[i, 0] = A_aug[i, n]
    
    # print("Solución final x:")
    # print(x)
    
    return x


#-------------------NOTEBOOK---------------------------------------
start_outer = time.time()

print("carga dataframes")
df_citas = pd.read_csv('files/citas.csv')
df_papers = pd.read_csv('files/papers.csv')

print("creamos WD")
size = df_papers.iloc[-1,0] + 1 #el i empieza en 0
WD = MatrizRala(size, size)
z = np.zeros(size)
for index, row in df_citas.iterrows():
    from_index = int(row['from'])
    to_index = int(row['to'])
    z[from_index] += 1

for index, row in df_citas.iterrows():
    from_index = int(row['from'])
    to_index = int(row['to'])
    WD[to_index, from_index] = 1 / z[from_index]


print("inicializa parametros")
#buscamos p_t+1 con el método iterativo
d=0.85
p_t0 = np.ones((size, 1)) * (1 / size)
a = np.ones((size, 1)) * ((1 - d) / size)

# Crear matrices ralas
a_matriz_rala = MatrizRala(size, 1)
for i in range(size):
    a_matriz_rala[i, 0] = a[i, 0]

p_t0_matriz_rala = MatrizRala(size, 1)
for i in range(size):
    p_t0_matriz_rala[i, 0] = p_t0[i, 0]

diff = np.inf
iteracion = 0
diferencias = []
matrix = (d * (WD)) #W@D

print("loop")

start_inner = time.time()

while iteracion < 10 and diff > 1e-4:
    print(iteracion)
    p_t1 = a_matriz_rala + matrix @ p_t0_matriz_rala
    diff = 0  
    
    # Calcular la diferencia en norma ||pt+1 - pt||
    sum_diff = 0

    for i in range(size):
        diff_temp = p_t1[i, 0] - p_t0_matriz_rala[i, 0]
        sum_diff += diff_temp ** 2
    
    diff = sum_diff ** 0.5
       
    diferencias.append(diff)
    p_t0_matriz_rala = p_t1  
    iteracion += 1

end_outer = time.time()

# print(p_t1)

# print(f"La ejecución completa tardó {end_outer-start_outer} segundos, y la iteración {end_outer-start_inner}")

# suma_pt1 = 0
# for i in range(size):
#     suma_pt1 += p_t1[i, 0]

# print("La suma de todos los elementos de p_t1 es:", suma_pt1)

#-----scores----
print("calculamos top 10")
impact_scores = [(i, p_t1[i, 0]) for i in range(size)]
top_10_impact = sorted(impact_scores, key=lambda x: x[1], reverse=True)[:10]

print("Top 10 papers con mayor impacto (por p_t1):")
for paper, score in top_10_impact:
    print(f"Paper ID: {paper}, Score: {score}")

# Encontrar los 10 papers más citados
citation_counts = df_citas['to'].value_counts()
top_10_cited = citation_counts.head(10)

print("Top 10 papers más citados:")
for paper, count in top_10_cited.items():
    impact_score = p_t1[paper, 0]
    print(f"Paper ID: {paper}, Citas: {count}, Impacto: {impact_score}")













#----------------------------------------------
# #cargamos los dataframes
# print("cargamos los dataframes")
# df_citas = pd.read_csv('files/citas.csv')
# df_papers = pd.read_csv('files/papers.csv')

# #inicializamos W y D a partir de la cantidad de filas - header de papers.csv
# size = df_papers.iloc[-1,0] + 1 #el i empieza en 0
# W = MatrizRala(size, size)
# D = MatrizRala(size, size)

# # print("creamos W y D")
# # #creamos W a partir de citas csv
# # for index, row in df_citas.iterrows():
# #     from_index = int(row['from'])
# #     to_index = int(row['to'])
# #     W[to_index, from_index] = 1

# # #creamos D a partir de citas csv
# # z = np.zeros(size)
# # for index, row in df_citas.iterrows():
# #     from_index = int(row['from'])
# #     z[from_index] += 1
# #     D[from_index, from_index] = 1/z[from_index]

# # print(W.shape, D.shape)
# # print(W[251778,24])
# # print(D[24,24])
# WD = MatrizRala(size, size)
# print("Creando WD directamente...")
# z = np.zeros(size)
# for index, row in df_citas.iterrows():
#     from_index = int(row['from'])
#     to_index = int(row['to'])
#     z[from_index] += 1

# for index, row in df_citas.iterrows():
#     from_index = int(row['from'])
#     to_index = int(row['to'])
#     WD[to_index, from_index] = 1 / z[from_index]

# # #chequeos 1/4 1/4 0
# # print(WD[251778,24])
# # print(WD[436906,24])
# # print(WD[3,24])

# print("inicializamos")
# #buscamos p_t+1 con el método iterativo
# d=0.85
# p_t0 = np.ones((size, 1)) * (1 / size)
# a = np.ones((size, 1)) * ((1 - d) / size)


# # Crear matrices ralas
# a_matriz_rala = MatrizRala(size, 1)
# for i in range(size):
#     a_matriz_rala[i, 0] = a[i, 0]

# p_t0_matriz_rala = MatrizRala(size, 1)
# for i in range(size):
#     p_t0_matriz_rala[i, 0] = p_t0[i, 0]

# diff = np.inf
# iteracion = 0
# diferencias = []
# #diferencias_pstar = []

# # print("multiplicacion")
# # print((WD@p_t0_matriz_rala)+a_matriz_rala)

# while iteracion < 3 and diff > 1e-4:
#     print(iteracion)
#     p_t1 = a_matriz_rala + (d * (W @ D)) @ p_t0_matriz_rala
#     diff = 0  
#     #diff_pstar = 0
    
#     # Calcular la diferencia en norma ||pt+1 - pt||
#     sum_diff = 0
#     #sum_diff_pstar = 0
    
#     for i in range(size):
#         diff_temp = p_t1[i, 0] - p_t0_matriz_rala[i, 0]
#         sum_diff += diff_temp ** 2
        
#         #diff_temp_pstar = p_t1[i, 0] - p_star[i, 0]
#        # sum_diff_pstar += diff_temp_pstar ** 2
    
#     diff = sum_diff ** 0.5
#     #diff_pstar = sum_diff_pstar ** 0.5
       
#     diferencias.append(diff)
#    # diferencias_pstar.append(diff_pstar)
#     p_t0_matriz_rala = p_t1  
#     iteracion += 1

# print(p_t1)

