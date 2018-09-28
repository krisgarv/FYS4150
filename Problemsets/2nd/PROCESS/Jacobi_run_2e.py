from Jacobi_class import Eigenvalues as J
import scipy.linalg as sl
import numpy as np
import time

def run(N, a, di):
    # Creating the input matrix
    r = np.zeros(N)
    r[0] = 0
    r[1] = a

    A = sl.toeplitz(r, r)
    np.fill_diagonal(A, di)


    # Calling the Jacobi module with initial values for buckling beam.
    i = J(A)

    # Numpys solution:
    t0 = time.time()
    numpy_lmbda = i.nmpy_eigenval()
    t1 = time.time()
    time_numpy = t1 - t0

    # Sorting eigenvalues by size to simplify comparison.
    NA = np.sort(numpy_lmbda)

    # Jacobi solution:
    t2 = time.time()
    Jacobi_A, Jacobi_R, Jacobi_iter = i.Jacobi()
    t3 = time.time()
    time_jacobi = t3 - t2

    # Sorting eigenvalues by size to simplify comparison.
    JA = np.sort(np.diag(Jacobi_A))

    return A, JA,NA, Jacobi_iter, time_jacobi, time_numpy

N = 4
rho_max = 1.85
h = float(rho_max)/N
a = (1.0/h**2)*-1.0


di = np.zeros(N+1)
di[0] = 1/h**2
omega = [0.01, 0.05, 1., 5.]

for j in omega:
    for i in range(1,N+1):
        di[i] = (2 + j**2*i**2*h**4 + h*(1./i))/h**2

    A, JA, NA, Jacobi_iter, time_jacobi, time_numpy = run(N, a, di)
    
