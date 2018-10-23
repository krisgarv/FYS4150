import time
import numpy as np
from solver import solver
import matplotlib.pyplot as plt
from solar_system import solar_system as solar
"""
To compare the skills of the two methods we check how many integration steps
each of the methods need to stabilize. We also test the CPU-time for a selection
integration steps to see which method is more efficient.

To do these comparisons and simple calculations we have chosen to look at a
simple Sun-Earth-system with the center of the Sun placed in origo and with no
initial velocity for the Sun. The Earth is initially placed in the xy-plane at
x = 1 AU, y = 0. All plots are in two dimensions for simplicity, but the
calculations, done by the class solver, are in three dimensions.
"""
# Mass
mass_sun = 1.0
mass_earth = 3E-6
# Initial position
position_sun = (0.0, 0.0, 0.0)
position_earth = (1.0, 0.0, 0.0)
# Initial velocity
velocity_sun = (0.0, 0.0, 0.0)
velocity_earth = (0.0, 2*np.pi, 0.0)
# Creating the input matrix
input_matrix = np.zeros((2, 7))
input_matrix[0, 0] = mass_sun
input_matrix[1, 0] = mass_earth
input_matrix[0, 1:4] = position_sun
input_matrix[1, 1:4] = position_earth
input_matrix[0, 4:7] = velocity_sun
input_matrix[1, 4:7] = velocity_earth


def euler_or_verlet(method, numsteps, plot=False):
    """ This function is to compares the accuracy and CPU-time of the
    two integration methods Euler and velocity Verlet. Writing the results of
    the CPU-time to a logfile and plotting the positions calculated by the
    methods in individual plots, to see how many integration point the method
    needs to stabilize. The plots show the position of Earth throuhout one year.
    """
    # Open log file to write CPU-time to
    log = open('log.txt', 'a')
    # Running the script for one year
    time_max = 1
    # Empty list for legend names
    legend=[]
    # Initializing figure for plotting
    plt.figure(figsize=(10, 10))
    # Solving the system with either Euler's method or the velocity Verlet method
    if method == 'euler':
        # Repeating the calculation with different amounts of integration points
        for num in numsteps:
            # Initializing the solver method with the input variables
            euler = solver(input_matrix, 'euler', time_max, num)
            # Tracking the time of the calculation
            t0 = time.time()
            output_euler, KE, PE, AM = euler.main()
            t1 = time.time()
            t = t1-t0
            if plot == False:
                # Writing CPU-time to logfile
                log.write('Eulers method: CPU-time for %d integration points = %fs \n' %(num, t))
            else:
                # Extracting the arrays to plot
                xEe = output_euler[1, 0, :]
                yEe = output_euler[1, 1, :]
                # Plotting all solutions for the same solver in one plot
                plt.plot(xEe, yEe)
                # Appending the integration points to the legend
                legend.append(str(num))

    elif method == 'verlet':
        # Repeating the calculation with different amounts of integration points
        for num in numsteps:
            # Initializing the solver method with the input variables
            verlet = solver(input_matrix, 'verlet', time_max, num)
            # Running the calculation, logging the CPU-time
            t0 = time.time()
            output_verlet, KE, PE, AM = verlet.main()
            t1 = time.time()
            t = t1-t0
            if plot == False:
                # Writing CPU-time to logfile
                log.write('Velocity Verlet method: CPU-time for %d integration points: %fs \n' %(num, t))
            else:
                # Extracting the arrays to plot
                xVe = output_verlet[1, 0, :]
                yVe = output_verlet[1, 1, :]
                # Plotting all solutions for the same solver in one plot
                plt.plot(xVe, yVe)
                # Appending the integration points to the legend
                legend.append(str(num))
    log.close()
    # Showing the plot if the optional variable is set to True
    if plot == True:
        plt.xlabel('x [AU]\n %i year(s)' %(time_max), fontsize=16)
        plt.ylabel('y [AU]', fontsize=16)
        plt.title("Earth's orbit around the Sun (in origo)", fontsize=24)
        plt.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')
        plt.show()

"""-----------------------------------------------------------------------------
Running the script:
-----------------------------------------------------------------------------"""
"""Running euler_or_verlet three times to better evaluate the CPU-time, choosing
the shortest runs from the log file for comparison."""

for i in range(3):
    euler_or_verlet('euler', [1000000, 100000, 10000, 1000, 100])
for i in range(3):
    euler_or_verlet('verlet', [1000000, 100000, 10000, 1000, 100])

"""Plotting the two methods for different number of integration point to show
the accuracy of the calculations."""

euler_or_verlet('euler', [1000000, 100000, 10000, 1000, 100, 50], plot=True)
euler_or_verlet('verlet', [1000, 500, 100, 50], plot=True)
