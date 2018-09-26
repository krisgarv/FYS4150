import numpy as np
cimport numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colors

cpdef int find_numbers(double complex z, double complex c, int max_iterations):
	cdef int N
	for N in range(max_iterations+1):
		if abs(z) >= 2:
			return N
		z = z**2 + c
	return max_iterations


cpdef numpy.ndarray[numpy.double_t, ndim=2] find_total_grid(double x_min, double x_max, double y_min, double y_max, int nr_of_val, int max_iterations, double limit):
	# Creating the x- and y- values:
	cdef numpy.ndarray[numpy.double_t, ndim=1] x
	cdef numpy.ndarray[numpy.double_t, ndim=1] y
	cdef numpy.ndarray[numpy.double_t, ndim=2] grid
	x = np.linspace(x_min, x_max, nr_of_val)
	y = np.linspace(y_min, y_max, nr_of_val)
	# Creating the matrix which are going to be colored:
	grid = np.zeros((len(y), len(x)))
	# Run through the coordinate-system to find the c's, and call the function
	# "find_numbers" for each c to find the right iterationnumber to insert in the going-to-be-colored matrix.
	cdef int i
	cdef int j
	cdef double complex c_number
	for i in range(len(x)):
		for j in range(len(y)):
			c_number = complex(x[i], y[j])
			grid[j,i] = find_numbers(complex(0), c_number, max_iterations)
	#grid goes from 0 -> 100, we want values 0 -> 1
	#grid2 = grid/100.0
	return grid



#im = np.zeros((100,100,3))
#im[:,:,0] = 1

#interpolation='nearest' RdGy
