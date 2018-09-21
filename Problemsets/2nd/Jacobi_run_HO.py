from Jacobi_class_K import Eigenvalues as J
import numpy as np
import time

#------------------------------------------------------------------------
# Hardcoded initial values for harmonic oscillator with one electron.
N = 10
h = 1.0/(N+1)
# rho = [make a list and loop?]
rho = 2.0
d1 = (2.0/h**2 + rho**2)
a = (1.0/h**2)*-1.0
#------------------------------------------------------------------------
# Harmonic oscillator with one electron

#------------------------------------------------------------------------
# Calling the Jacobi module with initial values for harmonic oscillator
# with one electron.
j = J(N, d1, a)
# Calculating solutions from Jacobi's method, Numpy's solver and analytic.

# Analytic calculation:
analytic = j.analytic_eigenval()

# Numpys solution:
t4 = time.time()
numpy_lmbda = j.nmpy_eigenval()
t5 = time.time()
time_numpy = t5 - t4

# Sorting eigenvalues by size to simplify comparison.
NA = np.sort(numpy_lmbda)

# Jacobi solution:
t6 = time.time()
Jacobi_A, Jacobi_R, Jacobi_iter = j.Jacobi()
t7 = time.time()
time_jacobi = t7 - t6

# Sorting eigenvalues by size to simplify comparison.
JA = np.sort(np.diag(Jacobi_A))

#---------------------------------------------------------------------------

print('SOLUTIONS OF PROBLEM WITH HARMONIC OSCILLATOR WITH ONE ELECTRON:')

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
