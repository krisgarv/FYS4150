import numpy as np
import sys
import matplotlib.pyplot as plt

# This program calculates the relative error of our spcialized algorithm,
# compared to the analytic solution of the linear 2nd order eq.,
# with Dirichlet boundary condition, where u"(x)= 100*e^(-10*x)

# OBS! Super slow since n_val contains 1e7
n_val = np.array([int(1e1), int(1e2), int(1e3), int(1e4), int(1e5), \
int(1e6), int(1e7)])
# Empty lists
error = []
h_list = []

# Looping over all n values
for n in n_val:
	#vDefining x, and the step size h:
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

	# Looping to find d-vector:
	for i in range(0, n):
		d_vec[i] = f(x[i+1])*h**2

	# Finding b_tilde and d_tilde:
	d_tilde[0] = d_vec[0]
	b_tilde[0] = 2.0

	# Forward substitution:
	for i in range(1, n):
		b_tilde[i] = 2.0 - 1.0/b_tilde[i-1]
		d_tilde[i] = d_vec[i] + d_tilde[i-1]/b_tilde[i-1]

	# Backward substitution:
	for i in range(n, 0, -1):
		v[i] = (d_tilde[i-1] + v[i+1])/b_tilde[i-1]

	# Analytic solution:
	def u(x):
		u = np.zeros_like(x)
		u[:] = 1 - (1 - np.exp(-10))*x - np.exp(-10*x)
		return u

	# Inserting boundary conditions to our solutions
	v_sliced = v[1:-1]
	u = u(x)
	u_sliced = u[1:-1]

	# Compute the relative error:
	error_max = np.max(np.abs((v_sliced - u_sliced)/u_sliced))

	# Appending maximal error value of n to list of errors
	error.append(error_max)
	h_list.append(h)
	print('n=%d error=%.20f' % (n, error_max))

# Converting lists to arrays for plotting
error_arr = np.array(error)
h_arr = np.array(h_list)

#Plotting:
plt.plot(np.log10(h_arr), np.log10(error_arr)) #Supposed to be h_arr
plt.title('Relative error, a function of step size', size=17)
plt.xlabel("$log_{10}(h)$", size=15)
plt.ylabel("$log_{10}(\epsilon)$", size=15)
plt.show()
