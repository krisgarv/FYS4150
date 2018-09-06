import numpy as np
import sys
import matplotlib.pyplot as plt

#Getting the matrix-size from the terminal:
n = int(sys.argv[1])

#Matrix values:
b = 2.0

#Defining x, and the step size h:
x = np.linspace(0, 1, n+2)
h = 1.0/(n+1)

#Function for finding the d's:
def f(x):
	return 100*np.exp(-10*x)

#Creating the vectors:
v 		= np.zeros_like(x)

b_vec		= np.zeros(n)
b_vec[:]	= b
b_tilde		= np.zeros(n)


d_vec		= np.zeros(n)
d_tilde		= np.zeros(n)

#Looping to find d-vector:
for i in range(0, n):
	d_vec[i] = f(x[i+1])*h**2

#Finding b_tilde and d_tilde:
d_tilde[0] = d_vec[0]
b_tilde[0] = b_vec[0]

for i in range(1, n):
	b_tilde[i] = b_vec[i] - 1/b_tilde[i-1]
	d_tilde[i] = d_vec[i] + d_tilde[i-1]/b_tilde[i-1]

#Calculating v_n, which is the first in the backward elimination:
v[n] = d_tilde[n-1]/b_tilde[n-1]

#Calculating v_(n-1) until v_1
for i in range(n-1, 0, -1):
	v[i] = (d_tilde[i-2] + v[i+1])/b_tilde[i-2]

#Analytic answer:
def u(x):
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

#Plot:
plt.plot(x, v, x, u(x))
plt.legend( ["data", "analytic"] )
plt.title("For n=%d" % (n))
plt.show()
