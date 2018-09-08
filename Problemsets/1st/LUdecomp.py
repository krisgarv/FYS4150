import numpy as np
import sys
import matplotlib.pyplot as plt
import time
import scipy
import scipy.linalg as sl

# LU-decomposition

#Getting the matrix-size from the terminal:
n = int(sys.argv[1])
#n=10

x = np.linspace(0, 1, n+2)
v = np.array(np.zeros_like(x))
d = np.zeros(n)
h = 1.0/(n+1)


def f(x):
	return 100*np.exp(-10*x)

def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

#Looping to find d-vector:
for i in range(0, n):
	d[i] = f(x[i+1])*h**2

# Defining the matrix A as a nested list as this does not need predefined size:
M = []
# Defining first row vector of size n:
r_0 = np.zeros(n)
r_0[0] = 2.0
r_0[1] = -1.0
# Appending first row in matrix
M.append(r_0)
# Looping over middle rows in matrix, appending initial values a=-1, b=2, c=-1,
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
# lu (matrix) - Calculate LU matrix containing U in its upper triangle, and L in its lower
# triangle. The unit diagonal elements of L are not stored.
# piv (array) - Pivot indices representing the permutation matrix P:
# row i of matrix was interchanged with row piv[i].
lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
#
t0 = time.time()
w = sl.lu_solve((lu, piv), d, trans=0, overwrite_b=True, check_finite=False)
t1 = time.time()

timer=t1-t0
with open('logfile.txt', 'a') as log:
	log.write('LU - n=%d, Timer: %.17f s\n' % (n, timer))

v[1:-1] = w
#print(v)
plt.plot(x, v, x, u(x))
plt.legend( ["Numerical", "Analytic"] )
plt.title("n=%d" % (n))
#plt.show()
print("Time used:" , timer, "s")
