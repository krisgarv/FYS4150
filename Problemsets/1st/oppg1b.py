import numpy as np
import sys
import matplotlib.pyplot as plt
import time

#Getting the matrix-size from the terminal:
n = int(sys.argv[1])

#Matrix values:
a = -1.0
b = 2.0
c = -1.0

#Defining x, and the step size h:
x = np.linspace(0, 1, n+2)
h = 1.0/(n+1)

#Function for finding the d's:
def f(x):
	return 100*np.exp(-10*x)

#Creating the vectors:
v 		= np.zeros_like(x)

a_vec		= np.zeros(n-1)
a_vec[:]	= a

b_vec		= np.zeros(n)
b_vec[:]	= b
b_tilde		= np.zeros(n)

c_vec 		= np.zeros(n-1)
c_vec[:] 	= c

d_vec		= np.zeros(n)
d_tilde		= np.zeros(n)
d_hat		= np.zeros(n)

#Looping to find d-vector:
for i in range(0, n):
	d_vec[i] = f(x[i+1])*h**2

#Inserting known values for b_tilde and d_tilde:
b_tilde[0] = b_vec[0]

b_tilde[1] = b_vec[1] - c_vec[0]*a_vec[0]/b_tilde[0]

d_tilde[0] = d_vec[0]

d_tilde[1] = d_vec[1] - d_tilde[0]*a_vec[0]/b_tilde[0]

#Looping to find b_tilde, d_tilde and d_hat:
t0 = time.time()
for i in range(2, n):	#b3 -> bn
	b_tilde[i] = b_vec[i] - c_vec[i-1]*a_vec[i-1]/b_tilde[i-1]
	d_tilde[i] = d_vec[i] - d_tilde[i-1]*a_vec[i-1]/b_tilde[i-1]

d_hat[-1] = d_tilde[-1]

for i in range(n-2, -1, -1):
	d_hat[i] = d_tilde[i] - d_tilde[i+1]*c_vec[i]/b_tilde[i+1]
t1 = time.time()

#Numerical answer: 
for i in range(1, n+1):	#we want to find v_1 and up til v_n, and we have to use d_hat_1 and up til d_hat_n
	v[i] = d_hat[i-1]/float(b_tilde[i-1])

#Analytic answer: 
def u(x): 
	return 1 - (1 - np.exp(-10))*x - np.exp(-10*x)

#TEST!!
print(np.max(u(x) - v))


#Plot:
plt.plot(x, v, x, u(x))
plt.legend( ["data", "analytic"] )
plt.title("For n=%d" % (n))
plt.show()

print("Time used: ",(t1-t0)," s")




