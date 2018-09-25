from Jacobi_class import Eigenvalues as J
import scipy.linalg as sl
import numpy as np
import time

#------------------------------------------------------------------------

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
    Nlmbda, Nvec = i.nmpy_eigenval()
    t1 = time.time()
    time_numpy = t1 - t0

    # Sorting eigenvalues by size to simplify comparison.
    NA = np.sort(Nlmbda)

    # Jacobi solution:
    t2 = time.time()
    Jacobi_A, Jacobi_R, Jacobi_iter = i.Jacobi()
    t3 = time.time()
    time_jacobi = t3 - t2

    # Sorting eigenvalues by size to simplify comparison.
    JA = np.sort(np.diag(Jacobi_A))

    return A, JA, NA, Jacobi_iter, time_jacobi, time_numpy



# Hardcoded initial values for harmonic oscillator with one electron.
N = 4
rho_max = 10
h = float(rho_max)/N
a = -1.0/h**2

# Constructing d's for for the situation with adding the harmonic oscillator
# with one electron:
di = np.zeros(N)
for i in range(N):
    # rho_i = rho_0 + i*h = i*h
    di[i] = 2.0/h**2 + (i*h)**2
A, JA, NA, Jacobi_iter, time_jacobi, time_numpy = run(N, a, di)

# ANALYTIC RESULTS FOR THE EIGENVALUES L = [3, 7, 11, 15, ...]
# HVORDAN FINNE EN RHO SOM MATCHER?


# Print to commandline:
#------------------------------------------------------------------------
print ('SOLUTIONS FOR BUCKLING BEAM PROBLEM:')

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
