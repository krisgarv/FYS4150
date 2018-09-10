# LU-decomposition
import numpy as np
import sys
import matplotlib.pyplot as plt
import time
import scipy
import scipy.linalg as sl

# Fetching matrix-size from the command line:
n = int(sys.argv[1])

# Arrays of length [0, n+1]:
x = np.linspace(0, 1, n+2)
v = np.array(np.zeros_like(x))
# Array of length [1, n]:
d = np.zeros(n)
# Defining the step size:
h = 1.0/(n+1)

# Defining a function which calculates f(x):
def f(x):
	return 100*np.exp(-10*x)

# Defining a function which calculates our analytical solution:
def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

# Defining the vector d (RHS):
for i in range(0, n):
	d[i] = f(x[i+1])*h**2

# Defining the matrix A as an empty nested list:
M = []
# Defining first row in matrix:
r_0 = np.zeros(n)
r_0[0] = 2.0
r_0[1] = -1.0
# Appending first row in matrix
M.append(r_0)
# Looping over row [2, n-1] in matrix, appending initial values a=-1, b=2, c=-1,
# along the diagonal and non-diagonal:
for i in range(0, n-2):
    r = np.zeros(n)
    r[i] = -1.0
    r[i+1] = 2
    r[i+2] = -1.0
    M.append(r)
# Defining n'th row in matrix
r_n = np.zeros(n)
r_n[-1] = 2.0
r_n[-2] = -1.0
# Appending n'th row in matrix
M.append(r_n)

# Converting from nested list to matrix of arrays:
A = np.array(M)

# The LU-decomposition is done in two steps
# with functions from the scipy.linalg library
# First we use lu_factor which gives a factorization of our matrix A.
# lu (matrix) - Calculate LU matrix containing U in its upper triangle,
# and L in its lower triangle. The unit diagonal elements of L are not stored.
# piv (array) - Pivot indices representing the permutation matrix P:
# row i of matrix was interchanged with row piv[i].
# To increase performance:
# overwrite_a = True, lets the function reuse the input matrix
# check_finite = False, the function will not check that the input matrix
# contains only finite numbers.
lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
# The lu_solve function solves the equation system Av = d,
# given the LU factorization from lu_factor.
# w (array) - is the solution of the system, does not include the
# boundary conditions.
# To increase performance:
# overwrite_b=True, allows the function to reuse the input vector.
# check_finite=False, the function will not check that the input matrix
# contains only finite numbers.
# The time of this operation is logged:
t0 = time.time()
w = sl.lu_solve((lu, piv), d, trans=0, overwrite_b=True, check_finite=False)
t1 = time.time()
# Appending the results to final solution where v[0] = v[n+1] = 0
v[1:-1] = w

# Calculating time spendt by the LU solver:
timer=t1-t0

# Plotting Numerical solution compared to analytical
plt.plot(x, v, x, u(x))
plt.xlabel('x')
plt.ylabel('u(x) and v(x)')
plt.legend( ["Numerical", "Analytic"] )
plt.title("%d Grid points" % (n))
plt.show()
print("Time used:" , timer, "s")
