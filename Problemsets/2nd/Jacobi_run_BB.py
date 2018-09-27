from Jacobi_class import Eigenvalues as J
import scipy.linalg as sl
import numpy as np
import time

#---------------------------------------------------------------------------
# The buckling beam:
#------------------------------------------------------------------------
# Hardcoded initial values for the buckling beam problem.
N = 4
h = 1.0/(N+1)
d = 2.0/h**2
a = -1.0/h**2
# Creating the toeplitz matrix
A = (np.zeros((N, N)) + np.diag(d*np.ones(N)) + np.diag(a*np.ones(N-1), k=1) +\
    np.diag(a*np.ones(N-1), k=-1))

#--------------------------------------------------------------------------

# Function which calculates analytic solution:
def analytic_eigenval(N, d, a):
    lmbda = []
    for i in range(1, N+1):
        l = d + 2.0*a*np.cos((i*np.pi)/(N+1))
        lmbda.append(l)
    return lmbda

#------------------------------------------------------------------------
# Calculating solutions from Jacobi's method, Numpy's solver and analytic.

# Analytic calculation:
analytic = analytic_eigenval(N, d, a)

# Calling the Jacobi module with initial values for buckling beam.
i = J(A)

# Numpys solution:
t0 = time.time()
numpy_lmbda, numpy_eigvec = i.nmpy_eigenval()
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




print ('SOLUTIONS FOR BUCKLING BEAM PROBLEM:')

print("Eigenvalues obtained analytically: %a" %(analytic))
print (' ')
print("Eigenvalues obtained by library function from numpy: %a" \
      %(NA))
print("Time spendt by numpys method, for a %dx%d matrix: %g" \
      %(N, N, time_numpy))
print (' ')
print ("Eigenvalues obtained by Jacobi's method: %a" % (JA) )
print ("Time spendt by Jacobi's method, for a %dx%d matrix: %g"\
      %(N, N, time_jacobi))
print ("Number of similarity transformations, for %dx%d matrix:\
   %d" % (N, N, Jacobi_iter))
