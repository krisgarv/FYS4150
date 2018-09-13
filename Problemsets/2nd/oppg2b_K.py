import numpy as np
import sys
import scipy.linalg as sl
from math import *
#N = int(sys.argv[1])
N = 4


#rho = np.linspace(0, 1, N+1)
#u = np.zeros_like(rho)
#lmbda = np.zeros(N-1)
#a = np.zeros(N-2)
#d = np.zeros(N-1)

h = 1.0/N

r = np.zeros(N-1)
r[0] = 2
r[1] = -1

A = sl.toeplitz(r, r)
M = A*N**2
v, B = np.linalg.eig(M)

print (v)
eig = []
for i in range(1, N):
    print (i)
    l = (1.0/h**2)*(2.0 - 2.0*np.cos((i*np.pi)/(N)))
    eig.append(l)
print(eig)
