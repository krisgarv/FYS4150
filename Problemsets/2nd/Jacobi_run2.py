from Jacobi_class_K import Eigenvalues as J
import numpy as np
import time

N = 10
h = 1.0/(N+1)
a = (1.0/h**2)*-1.0
# Constructing d's for for the situation with adding the harmonic oscillator:
di = np.zeros(N+1)
for i in range(0,N):
    di[i] = (2.0 + (i*h)**2)/h**2

i = J(N, di, a)

# Analytic calculation:
#analytic = i.analytic_eigenval()

# Numpys solution:
t0 = time.time()
numpy_lmbda = i.nmpy_eigenval()
t1 = time.time()
time_numpy = t1 - t0

# Jacobi solution:
t2 = time.time()
Jacobi_A, Jacobi_R, Jacobi_iter = i.Jacobi()
t3 = time.time()
time_jacobi = t3 - t2

#print("Eigenvalues obtained analytically: %a" %(np.sort(analytic)))
#print (' ')
print("Eigenvalues obtained by library function from numpy: %a" \
      %(np.sort(numpy_lmbda)))
print("Time spendt by numpys method, for a %dx%d matrix: %g" \
      %(N, N, time_numpy))
print (' ')
print ("Eigenvalues obtained by Jacobi's method: %a" % (np.sort(np.diag(Jacobi_A))))
print ("Time spendt by Jacobi's method, for a %dx%d matrix: %g"\
      %(N, N, time_jacobi))
print ("Number of similarity transformations, for %dx%d matrix:\
   %d" % (N, N, Jacobi_iter))

print(Jacobi_A)
