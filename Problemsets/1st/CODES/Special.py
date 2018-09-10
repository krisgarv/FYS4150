import numpy as np
import sys
import matplotlib.pyplot as plt
import time

# Getting the matrix-size from the terminal:
n = int(sys.argv[1])

# Defining x, and the step size h:
x = np.linspace(0, 1, n+2)
h = 1.0/(n+1)

# Function for finding the d's:
def f(x):
	return 100*np.exp(-10*x)

# Creating the vectors:
v 		= np.zeros_like(x)

b_tilde		= np.zeros(n)

d_vec		= np.zeros(n)
d_tilde		= np.zeros(n)

# Looping to find the initial d-vector:
for i in range(0, n):
	d_vec[i] = f(x[i+1])*h**2

# FORWARD SUBSTITUTION
# Defining initial b_tilde and d_tilde:
d_tilde[0] = d_vec[0]
b_tilde[0] = 2.0
# Taking  the time of the forward and backward substitution:
t0 = time.time()
for i in range(1, n):
	b_tilde[i] = 2.0 - 1.0/b_tilde[i-1]
	d_tilde[i] = d_vec[i] + d_tilde[i-1]/b_tilde[i-1]

# BACKWARD SUBSTITUTION
# Calculating v:
for i in range(n, 0, -1):
	v[i] = (d_tilde[i-1] + v[i+1])/b_tilde[i-1]
t1 = time.time()
timer=t1-t0

# Analytic solution:
def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

# Plot:
plt.plot(x, v, x, u(x))
plt.xlabel('x')
plt.ylabel('u(x) and v(x)')
plt.legend( ["Numerical", "Analytic"] )
plt.title("%d Grid points" % (n))
plt.show()

# Return CPU time:
print("Time used:" , timer, "s")
