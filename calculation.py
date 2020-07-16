import numpy as np
import math
import matplotlib.pyplot as plt
import material
K_i = [[1.0, -1.0], 
      [-1.0, 1.0]]

F_i = [[0.5], 
       [0.5]]

def createNodes(N):
    nodes = np.arange(1,(N+1))
    nodes = nodes / N
    return nodes
    
def createF(N, material):
    tmp = material.density / (N*N*material.youngModulus)
    F = np.full(N-1, tmp)
    F = np.append(F, 0.5 * tmp)
    return F

def createU(N):
    U = np.full(N, 0.0)
    return U

def createKdiagonal(N):
    Kdiagonal = np.full(N-1, 2.0)
    Kdiagonal = np.append(Kdiagonal, 1.0)
    return Kdiagonal

def createK_UP_DOWN_diagonal(N):
    K_UP_DOWN_diagonal = np.full(N, -1.0)
    return K_UP_DOWN_diagonal

def solveMatrix(N, F, U, Kdiagonal, K_UP_DOWN_diagonal):
    for i in range(1,N):
        tmp = K_UP_DOWN_diagonal[i]/Kdiagonal[i-1]
        Kdiagonal[i] -= tmp*K_UP_DOWN_diagonal[i-1]
        F[i] -= tmp*F[i-1]
    U[N-1] = F[N-1]/Kdiagonal[N-1]
    for i in range(N-2, 0, -1):
        U[i] = (F[i]-K_UP_DOWN_diagonal[i]*U[i+1])/Kdiagonal[i]

def calc(N = 5):
    mater = material.steel
    nodes = createNodes(N)
    F = createF(N, mater)
    U = createU(N)
    Kdiagonal = createKdiagonal(N)
    K_UP_DOWN_diagonal = createK_UP_DOWN_diagonal(N)
    solveMatrix(N, F, U, Kdiagonal, K_UP_DOWN_diagonal)
    return nodes, U