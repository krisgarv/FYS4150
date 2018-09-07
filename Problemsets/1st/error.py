import numpy as np
import sys
import matplotlib.pyplot as plt


#OBS! Super slow since n_val = 1e7
n_val = np.array([int(1e1), int(1e2), int(1e3), int(1e4), int(1e5), int(1e6), int(1e7)])
error = []
h_list = []

for n in n_val:
	#Defining x, and the step size h:
	x = np.linspace(0, 1, n+2)
	h = 1.0/(n+1)

	#Function for finding the d's:
	def f(x):
		return 100*np.exp(-10*x)

	#Creating the vectors:
	v 		= np.zeros_like(x)

	b_tilde		= np.zeros(n)

	d_vec		= np.zeros(n)
	d_tilde		= np.zeros(n)

	#Looping to find d-vector:
	for i in range(0, n):
		d_vec[i] = f(x[i+1])*h**2

	#Finding b_tilde and d_tilde:
	d_tilde[0] = d_vec[0]
	b_tilde[0] = 2.0

	for i in range(1, n):
		b_tilde[i] = 2.0 - 1.0/b_tilde[i-1]
		d_tilde[i] = d_vec[i] + d_tilde[i-1]/b_tilde[i-1]

	#Calculating v_n, which is the first in the backward elimination:
	v[n] = d_tilde[n-1]/b_tilde[n-1]

	#Calculating v_(n-1) until v_1
	for i in range(n-1, 0, -1):
		v[i] = (d_tilde[i-2] + v[i+1])/b_tilde[i-2]

	#Analytic answer:
	def u(x):
		u = np.zeros_like(x)
		u[:] = 1 - (1 - np.exp(-10))*x - np.exp(-10*x)
		return u

	#Compute the relative error:
	v_sliced = v[1:-1]
	u = u(x)
	u_sliced = u[1:-1]

	error_max = np.max(np.log10(np.abs((v_sliced - u_sliced)/u_sliced)))
	#??????WHAAAAT are we taking max of????
	
	error.append(error_max)
	h_list.append(h)
	print(n)
	

#Plotting:	
error_arr = np.array(error)
h_arr = np.array(h_list)
plt.plot(np.log10(n_val), error_arr) #Supposed to be h_arr
plt.xlabel("$log_{10}(n)$") 
plt.ylabel("Maxval. of $log_{10}(\epsilon)$")
plt.show()
