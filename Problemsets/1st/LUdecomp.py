import numpy as np
import sys
import matplotlib.pyplot as plt
import time
import scipy
import scipy.linalg

# LU-decomposition

#Getting the matrix-size from the terminal:
n = int(sys.argv[1])
#n=10

x = np.linspace(0, 1, n+2)
d = np.zeros(n)
h = 1.0/(n+1)


def f(x):
	return 100*np.exp(-10*x)

def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

#Looping to find d-vector:
for i in range(0, n):
	d[i] = f(x[i+1])*h**2

# Defining the matrix A as a nested list
M = []
r_0 = np.zeros(n)
r_0[0] = 2.0
r_0[1] = -1.0
M.append(r_0)
for i in range(0, n-2):
    r = np.zeros(n)#np.array(np.zeros(n))
    r[i] = -1.0
    r[i+1] = 2
    r[i+2] = -1.0
    M.append(r)
r_n = np.zeros(n)
r_n[-1] = 2.0
r_n[-2] = -1.0
M.append(r_n)

A = np.array(M)
#P, L, U = scipy.linalg.lu(A)
lu, piv = scipy.linalg.lu_factor(A)
v = np.array(np.zeros_like(x))
w = scipy.linalg.lu_solve((lu, piv), d)
v[1:-1] = w
#print(v)
plt.plot(x, v, x, u(x))
plt.show()
