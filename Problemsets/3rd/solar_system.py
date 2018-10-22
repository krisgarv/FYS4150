from solver_K import solver
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import re


"""
Other programs?
    - Plot the position of the earth as function of integration steps for each Method
    - Plot the kinetic, potential, total energy and angular momentum
    - Calculate the diversion of angular momentum throughout one year run
"""
class solar_system(object):

    def __init__(self, objects, dimension=2, time_max=20, num_steps=500, CM=False, filename=None, method='verlet'):
        if 'Sun' not in objects:
            objects.append('Sun')
        self.objects = objects
        self.dim = dimension
        self.numbodies = len(objects)
        self.t = time_max
        self.N = num_steps
        self.CM = CM
        self.filename = filename
        self.method = method
        self.main()

    def main(self):
        input_matrix, legend = self.input_data()
        if self.CM is True:
            input_matrix = self.center_of_mass(input_matrix)
        I = solver(input_matrix, self.method, self.t, self.N)
        output_matrix, KE, PE, AM = I.main()
        if self.dim == 3:
            self.plot_3D(output_matrix, legend)
        else:
            self.plot_2D(output_matrix, legend)
        if self.filename != None:
            fig.savefig(filename + '.png')
        plt.show()
        return output_matrix, KE, PE, AM

    def input_data(self):
        """This function creates a 2D matrix containing information on the
        objects mass, position and velocity.

        The information is based on
        NASAs data from september 18th 2018, read from the data file
        planets_distancespeed.txt.

        The positions of the planets is realtive
        to the position of the Sun, placed in origo. The initial speed of the
        sun is zero."""
        #objects = self.objects
        # The sun is not optional, will be added as first element of the list from input arguments
        if 'Sun' not in self.objects:
            self.objects.append('Sun')
        # Creating a empty matrix to store the objects data
        input_matrix = np.empty((len(self.objects), 7))
        # Reading inital values from the data file, creating the input matrix
        data = open('planets_distancespeed.txt', 'r')
        # Using loops and regular expressions to achieve the data from file
        i = 0
        legend = []
        for lines in data.read().splitlines():
            name = re.findall(r"(^\D+):", lines)
            # Extracting data on the objects of interest
            if len(set(name) & set(self.objects)) >= 1:
                legend.append(name)
                index = lines.index(':')
                numbers = lines[index+1:]
                array = np.asarray([float(value) for value in numbers.split(',')])
                input_matrix[i, :] = array
                i += 1
        # Converting velocity unit from [AU/day] to [AU/year]
        input_matrix[:, 4:7] = input_matrix[:, 4:7]*365
        # The returned matrix are shaped to match the solver method input
        return input_matrix, legend

    def center_of_mass(self, matrix):
        # Changing the positions of all objects relative to center of mass, in origo.
        x, y, z = sum(input_matrix[:, 0]*input_matrix[:, 1:4])/sum(input_matrix[:, 0])
        # x-direction
        matrix[:, 1]-x
        # y-direction
        matrix[:, 2]-y
        # z-direction
        matrix[:, 3]-z
        # empty array for the initial velocity of the Sun
        numerator = np.empty(3)
        # The Suns initial velocity which makes the total momentum of the system zero
        # velcity_sun = (sum(mass_planet_i*veocity_planet_i*position_planets_i)/(mass_sun*position_sun))
        for i in range(1, len(objects)):
            # Calculating the numerator first to avoid repetative calculation
            numerator += matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7]
        # Divinding by the mass and position of the Sun
        matrix[0, 4:7] = numerator/(matrix[0, 0]*matrix[0, 1:4])
        # Returning the modified matrix
        return matrix

    def plot_2D(self, position, legend):
        plt.figure(figsize=(10, 10))
        for i in range(self.numbodies):
            plt.plot(position[i, 0, :], position[i, 1, :])
        plt.xlabel('x [AU]')
        plt.ylabel('y [AU]')
        plt.title('The solar system. \n %d years from Sep. 18 2018' %(self.t))
        plt.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')

    def plot_3D(self, position, legend):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')
        for i in range(self.numbodies):
            ax.plot(position[i, 0, :], position[i, 1, :], position[i, 2, :])
        ax.set_xlabel('x [AU]')
        ax.set_ylabel('y [AU]')
        ax.set_zlabel('z [AU]')
        ax.set_title('The solar system. \n %d years from Sep. 18 2018' %(self.t))
        ax.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')


if __name__=='__main__':
    main()
    """
    # Using argparse to make a nice help flag to describe the usage of this
    # program
    pa = argparse.ArgumentParser(description='This program calculates and \
    plots the position of objects of your choosing from \
    the solar system in two or three dimensions. ', epilog='This script \
    uses the method solver.py and the data file planets_distancespeed.txt, \
    make sure that you have all files in your directory.\n \
    The program uses the the solver method to calculate Newtons law of \
    gravitation by Eulers or the velocity Verlet method.\n \
    DEFAULT: \n \
    The program plots all planets as well as Pluto and the Sun,\
     in two dimensions. \n \
    The velocity Verlet method is given 1000 integration points and \
    calculates the position of the planets over 10 years.\n \
    The center of the Sun is placed in origo and have no initial velocity.\
    The velocity Verlet method is set as default as it need far less \
    integration points to stabilize.\n \
    WARNING:\n \
    In list of objects first letter must be capitalized.\n \
    To calculate the objects positions with Eulers method, remember to \
    increase number of integration points for the system to stabilize.')
    pa.add_argument('-objects', type=list, help='List of planet names.', \
    default=['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', \
    'Uranus', 'Neptune', 'Pluto'])
    pa.add_argument('-D', type=int, default=2, \
    help='Which dimension to plot, 2D or 3D (integer).')
    pa.add_argument('-t', type=int, default=1, \
    help='Number of years (integer) to be plotted.')
    pa.add_argument('-N', type=int, default=500, \
    help='Integration points (integer) per year.')
    pa.add_argument('-CM', type=bool, default=False, \
    help='Shift origo to center of mass (boolean variable). If true: Initial \
    position and velocity of the sun and relative positions are calculated. ')
    pa.add_argument('-filename', type=str, default=None, help='If filename is\
    provided, the plot is saved as a .png file with given filename.')
    pa.add_argument('-method', type=str, default='verlet', help='Integration \
    method, velocity Verlet ot Eulers method. Velocity Verlet is far more \
    efficient and are therefore set as default.')
    args = pa.parse_args()
    # Initializing the method with the arguments from the command line.
    ss = solar_system(args.objects, args.D, args.t, args.N, args.CM, \
    args.filename, args.method)
    #ss.main()
    """
