# Para correr los tests:
#   1- Instalar pytest: ("pip install pytest")
#   2- Correr en la terminal "pytest tests.py"

import pytest
from matricesRalas import MatrizRala
import numpy as np

class TestIndexacionMatrices:
    def test_indexarCeros( self ):
        A = MatrizRala(3,3)

        assert np.allclose( np.zeros(9), [A[i,j] for i in range(3) for j in range(3)] )

    def test_asignarValor( self ):
        A = MatrizRala(3,3)
        A[0,0] = 1

        assert A[0,0] == 1

    def test_asignarDejaCeros(self):
        A = MatrizRala(3,3)

        assert np.allclose( np.zeros(9), [A[i,j] if (i != j and i != 0) else 0 for i in range(3) for j in range(3)] )

    def test_asignarEnMismaFila( self ):
        A = MatrizRala(3,3)
        A[0,1] = 2
        A[0,0] = 1

        assert A[0,1] == 2 and A[0,0] == 1

    def test_reasignar( self ):
        A = MatrizRala(3,3)
        A[1,0] = 1
        A[1,0] = 3

        assert A[1,0] == 3

class TestSumaMatrices:
    def test_distintasDimensiones( self ):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)
        with pytest.raises(Exception) as e_info:
            C = A + B
        
    def test_sumaCorrectamente( self ):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        B[0,2]=3
        B[1,1]=2

        C = A+B
        assert C[0,0] == 1 and C[0,2] == 6 and C[2,2] == 4 and C[1,1] == 2

    def test_sumarMismaMatriz(self):
        A = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        C = A + A
        assert C[0,0] == 2 and C[0,2] == 6 and C[2,2] == 8 

    def test_sumarMatrizCeros(self):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0] = 10
        A[0,1] = 20
        A[0,2] = 30

        B[0,0] = 0
        B[0,1] = 0
        B[0,2] = 0

        C = A + B
        assert C[0,0] == 10 and C[0,1] == 20 and C[0,2] == 30

    def test_sumarMatrizNegativos(self):
        A = MatrizRala(3,3)
        B = MatrizRala(3,3)

        A[0,0] = 10
        A[0,1] = 20
        A[0,2] = 30

        B[0,0] = -10
        B[0,1] = -20
        B[0,2] = -30

        C = A + B
        assert C[0,0] == 0 and C[0,1] == 0 and C[0,2] == 0

class TestResta:

    def test_restarDistintasDimensiones( self ):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)
        with pytest.raises(Exception) as e_info:
            C = A - B

    def test_restaCorrectamente(self):
        A = MatrizRala(2,2)
        B = MatrizRala(2,2)
        A[0,0] = 5
        A[0,1] = 10
        A[1,0] = 15
        A[1,1] = 20

        B[0,0] = 5
        B[0,1] = 1
        B[1,0] = 0
        B[1,1] = 28

        C = A - B
        assert C[0,0] == 0 and C[0,1] == 9 and C[1,0] == 15 and C[1,1] == -8

    def test_restaCeros(self):
        A = MatrizRala(2,2)
        B = MatrizRala(2,2)
        A[0,0] = 5
        A[0,1] = 10
        A[1,0] = 15
        A[1,1] = 20

        C = A - B
        assert C[0,0] == 5 and C[0,1] == 10 and C[1,0] == 15 and C[1,1] == 20

    def test_restaMismaMatriz(self):
        A = MatrizRala(2,2)
    
        A[0,0] = 5
        A[0,1] = 10
        A[1,0] = 15
        A[1,1] = 20

        C = A - A
        assert C[0,0] == 0 and C[0,1] == 0 and C[1,0] == 0 and C[1,1] == 0


class TestProductoPorEscalar:
    def test_escalaCorrectamente( self ):
        A = MatrizRala(3,3)
        A[0,0]=1
        A[0,2]=3
        A[2,2]=4

        C = A * 13
        assert C[0,0] == (1*13) and C[0,2] == (3*13) and C[2,2] == (4*13)

    def test_multiplicar_por_cero(self):
        A = MatrizRala(3,3)
        A[0,0]=1
        A[0,2]=5
        A[2,2]=9

        C = A * 0
        assert C[0,0] == 0 and C[0,2] == 0 and C[2,2] == 0

    def test_multiplicar_por_fraccion(self):
        A = MatrizRala(3,3)
        A[0,0]=4
        A[0,2]=8
        A[2,2]=10

        C = A * (1/2)
        assert C[0,0] == 2 and C[0,2] == 4 and C[2,2] == 5

    def test_r_mul(self):
        A = MatrizRala(3,3)
        A[0,0]=4
        A[0,2]=8
        A[2,2]=10
        
        D = (1/2) * A
        assert D[0,0] == 2 and D[0,2] == 4 and D[2,2] == 5

class TestProductoMatricial:
    def test_dimensionesEquivocadas(self):
        A = MatrizRala(2,3)
        B = MatrizRala(4,3)
        with pytest.raises(Exception) as e_info:
            C = A @ B

    def test_productoAndaBien(self):
        A = MatrizRala(2,3)
        B = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        B[2,0]=3
        B[1,1]=2

        C = A @ B

        assert C.shape[0] == 2 and C.shape[1]==3 and C[0,0] == 9 and all( [C[i,i] == 0 for i in range(3) for j in range(4) if (i!=j and i!=0)] )

    def test_productoPorIdentidad( self ):
        A = MatrizRala(3,3)
        Id = MatrizRala(3,3)

        A[0,0]=1
        A[0,2]=3
        A[1,2]=4

        Id[0,0] = 1
        Id[1,1] = 1
        Id[2,2] = 1

        C1 = A @ Id
        C2 = Id @ A
        assert C1[0,0] == 1 and C1[0,2] == 3 and C1[1,2] == 4 and C2[0,0] == 1 and C2[0,2] == 3 and C2[1,2] == 4 and C1.shape == C2.shape and C1.shape == A.shape

    def test_productoPorNegativos(self):
        A = MatrizRala(2, 3)
        B = MatrizRala(3, 2)

        A[0, 0] = 1
        A[0, 1] = -2
        A[1, 1] = 3

        B[0, 0] = -1
        B[1, 1] = 2
        B[2, 1] = -3

        C = A @ B

        assert C.shape == (2, 2)
        assert C[0, 0] == -1 and C[0, 1] == -4 and C[1, 0] == 0 and C[1, 1] == 6

    def test_productoPorCeros(self):
        A = MatrizRala(2, 3)
        B = MatrizRala(3, 2)

        A[0, 0] = 1
        A[0, 1] = 2
        A[1, 2] = 3

        B[0, 1] = 4
        B[1, 0] = 5

        C = A @ B

        assert C.shape == (2, 2)

        assert C[0, 0] == 10 and C[0, 1] == 4 and C[1, 0] == 0 and C[1, 1] == 0

# class testGaussJordan:
#     def test_GaussJordan( self ):
#         A = MatrizRala(3,3)
#         b = MatrizRala(3,1)

#         A[0,0]=1
#         A[0,2]=3
#         A[1,2]=4
#         A[2,1]=5

#         b[0,0]=1
#         b[2,0]=3

#         x = GaussJordan(A,b)
        
#         assert x[0,0] == (-5/4) and x[2,0] == (3/4)


        

