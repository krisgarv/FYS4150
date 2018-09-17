import numpy as np
import sys
import scipy.linalg as sl
from math import *
#N = int(sys.argv[1])
# Initial values
N = 3
h = 1.0/N
d = (1.0/h**2)*2.0
a = (1.0/h**2)*-1.0

# Initial values for Jacobi's Jacobi's method:
eps = 1.0e-8    # epsilon
maxiter = N**3  # maximum number of iterations

# Creating input arrays for toeplitz matrix:
r = np.zeros(N-1)
r[0] = d
r[1] = a
A = sl.toeplitz(r, r)

# Solution found from library functions:
def nmpy_eigenval(A):
    lmbda, eigenvec = np.linalg.eig(A)
    return lmbda

# Function which calculates analytic solution:
def analytic_eigenval(N, d, a):
    lmbda = []
    for i in range(1, N):
        l = d + 2.0*a*np.cos((i*np.pi)/(N))
        lmbda.append(l)
    return lmbda

analytic = analytic_eigenval(N, d, a)
print(analytic)
library = nmpy_eigenval(A)
print(library)

#how to implement test?
"""def test_eigenval():
    assert [1.0, 3.0] == eigenval(3, 2.0, -1.0)
"""
