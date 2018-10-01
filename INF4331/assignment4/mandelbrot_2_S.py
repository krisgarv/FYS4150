import numpy as np
import matplotlib.pyplot as plt

def find_numbers(z, c, columns, rows, max_iterations):
	#Create a new matrix which is going to contain the number of iterations
	result = np.zeros((rows, columns), dtype=int)#np.zeros_like(c, np.int)
	#Create a new matrix which has the same size as c, but contains true
	truefalse = np.zeros(c.shape, dtype=bool)
	truefalse[:,:] = True
	#Looping through until max_iterations:
	for i in range(max_iterations):
		#This is the elements that is going to be handled:
		element = z[truefalse]
		#If the absolute value of the elements in element is greater than 2.0, the truefalse
		#array will change the index to False. If not it will stay True:
		truefalse[truefalse] = np.less(np.abs(element), 2.0)
		#Put in the number of iterations in the result-matrix. Only those with True is changed:
		#(i+1 since the first round with 0**2 + c is one iteration, and the i=1 won't be put to the
		#the result matrix if not)
		result[truefalse] = i+1
		#Changing the z for those numbers which we still need to check the iteration number of:
		z[truefalse] = z[truefalse]**2 + c[truefalse]
	return result

def find_total_grid(x_min, x_max, y_min, y_max, columns, rows, max_iterations):
	y_min = complex(0, y_min)
	y_max = complex(0, y_max)
	x = np.linspace(x_min, x_max, columns)
	y = np.linspace(y_max, y_min, rows)

	xx, yy = np.meshgrid(x,y)

	cnumbers = np.zeros((rows, columns))
	cnumbers = xx + yy

	#Create a new matrix which name is z, where everything is first 0+0j
	z = np.zeros_like(cnumbers)

	grid = find_numbers(z, cnumbers, columns, rows, max_iterations) #Sends in cnumbers and max_iterations
	#grid2 = grid/float(max_iterations)
	#grid3 = colouring(columns, rows, grid)
	return grid

def colouring(columns, rows, grid):
	grid2 = np.empty((rows, columns, 3))
	for i in range(columns):
		for j in range(rows):
			if grid[j,i] <= 1:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0
				grid2[j,i,2] = 0.2
			elif grid[j,i] == 2:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0
				grid2[j,i,2] = 0.3
			elif grid[j,i] > 2 and grid[j,i] < 4:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0
				grid2[j,i,2] = 0.4
			elif grid[j,i] >= 4 and grid[j,i] < 6:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.1
				grid2[j,i,2] = 0.5
			elif grid[j,i] >= 6 and grid[j,i] < 8:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.1
				grid2[j,i,2] = 0.6
			elif grid[j,i] >= 8 and grid[j,i] < 10:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.1
				grid2[j,i,2] = 0.7
			elif grid[j,i] >= 10 and grid[j,i] < 12:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.1
				grid2[j,i,2] = 0.8
			elif grid[j,i] >= 12 and grid[j,i] < 14:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.1
				grid2[j,i,2] = 0.9
			elif grid[j,i] >= 14 and grid[j,i] < 16:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.2
				grid2[j,i,2] = 0.9
			elif grid[j,i] >= 16 and grid[j,i] < 18:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.2
				grid2[j,i,2] = 0.8
			elif grid[j,i] >= 18 and grid[j,i] < 20:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.4
				grid2[j,i,2] = 0.8
			elif grid[j,i] >= 20 and grid[j,i] < 50:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.5
				grid2[j,i,2] = 0.6
			elif grid[j,i] >= 50 and grid[j,i] < 200:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.7
				grid2[j,i,2] = 0.3
			elif grid[j,i] >= 200 and grid[j,i] < 1000:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0.8
				grid2[j,i,2] = 0.1
			elif grid[j,i] == 1000:
				grid2[j,i,0] = 0
				grid2[j,i,1] = 0
				grid2[j,i,2] = 0
	return grid2

def colouring2():
	from matplotlib.colors import LinearSegmentedColormap
	cdict = {'red':   [(0.0,  0.4039, 0.4039),
						(0.04, 0.8392, 0.8392),
	                   (0.15,  1.0, 1.0),
	                   (1.0,  0.101, 1.101)],

	         'green': [(0.0,  0.0, 0.0),
			 			(0.04, 0.3764, 0.3764),
	                   (0.15, 1.0, 1.0),
	                   (1.0,  0.101, 0.101)],

	         'blue':  [(0.0,  0.1215, 0.1215),
			 			(0.04, 0.3019, 0.3019),
	                   (0.15,  1.0, 1.0),
	                   (1.0,  0.101, 0.101)]}

	blue_red1 = LinearSegmentedColormap('BlueRed1', cdict)
	return blue_red1

if __name__ == "__main__":
	#When running the program in the terminal, this is run
	#Choosing the size of the matrix which is going to be plotted:
	columns = 1000
	rows	= 1000

	import time
	t0 		= time.time()
	grid 	= find_total_grid(x_min = -2.0, x_max = 1.0, y_min = -1.3, y_max = 1.3, columns=1000, rows=1000, max_iterations=1000)
	t1 		= time.time()
	t_tot	= t1 - t0
	print("Runtime: %f s for a nxm matrix with n=%d and m=%d" %(t_tot, columns, rows))
	#rg = colouring2()
	plt.imshow(grid, cmap='RdGy', extent=[-2.0, 1.0, 1.3, -1.3])
	plt.colorbar()
	plt.gca().invert_yaxis()
	plt.xlabel("Real")
	plt.ylabel("Imaginary")
	plt.title("Mandelbrot, nxm with n=%d and m=%d" %(columns, rows))
	plt.savefig("mandelbrot_2.png")
	plt.show()
