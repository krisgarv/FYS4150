import numpy as np
import sys
import matplotlib.pyplot as plt
import time

# Getting the matrix-size from the terminal:
n = int(sys.argv[1])

# Matrix values:
a = -1.0
b = 2.0
c = -1.0

# Defining x, and the step size h:
x = np.linspace(0, 1, n+2)
h = 1.0/(n+1)

# Defining a function which calculates f(x):
def f(x):
	return 100*np.exp(-10*x)

# Creating the vectors:
v 			= np.zeros_like(x)

a_vec		= np.zeros(n-1)
a_vec[:]	= a

b_vec		= np.zeros(n)
b_vec[:]	= b
b_tilde		= np.zeros(n)

c_vec 		= np.zeros(n-1)
c_vec[:] 	= c

d_vec		= np.zeros(n)
d_tilde		= np.zeros(n)

# Looping to find d-vector:
for i in range(0, n):
	d_vec[i] = f(x[i+1])*h**2

# FORWARD SUBSTITUTION
# Defining the initial values of b_tilde and d_tilde:
d_tilde[0] = d_vec[0]
b_tilde[0] = b_vec[0]

# Taking  the time of the forward and backward substitution:
t0 = time.time()
for i in range(1, n):
	b_tilde[i] = b_vec[i] - c_vec[i-1]*a_vec[i-1]/b_tilde[i-1]
	d_tilde[i] = d_vec[i] - d_tilde[i-1]*a_vec[i-1]/b_tilde[i-1]

# BACKWARD SUBSTITUTION
# To avoid index error for c_vec, must define v[n] outside loop:
# Calculating v:
v[n] = d_tilde[i-1]/b_tilde[i-1]
for i in range(n-1, 0, -1):
	v[i] = (d_tilde[i-1] - c_vec[i-1]*v[i+1])/b_tilde[i-1]
t1 = time.time()
timer=t1-t0

# Analytic solution:
def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

# Plot:
plt.plot(x, v, x, u(x))
plt.xlabel('x')
plt.ylabel('$v(x)$ and $u(x)$')
plt.legend( ["Numerical", "Analytic"] )
plt.title("%d Grid points" % (n))
plt.show()

# Return CPU time:
print("Time used: ", timer, "s")
