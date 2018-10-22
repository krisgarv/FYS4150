from solver import solver
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

    def __init__(self, objects, dimension, time_max, num_steps, \
    CM, filename, method, plot_energies):
    #dimension=2, time_max=20, num_steps=500, \
    #CM=False, filename=None, method='verlet', plot_energies=None):
        if 'all' in objects:
            objects = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', \
            'Saturn', 'Uranus', 'Neptune', 'Pluto']
        # The sun is not optional, will be added as first element of the list from input arguments
        if 'Sun' not in objects:
            objects.append('Sun')
        print(objects)
        self.objects = objects
        self.dim = dimension
        self.numbodies = len(objects)
        self.t = time_max
        self.N = num_steps
        self.CM = CM
        self.filename = filename
        self.method = method
        self.plot_energies = plot_energies
        self.main()

    def main(self):
        input_matrix, legend = self.input_data()
        if self.CM is True:
            input_matrix = self.center_of_mass(input_matrix)
        I = solver(input_matrix, self.method, self.t, self.N)
        output_matrix, KE, PE, AM = I.main()
        if self.plot_energies != None:
            print(self.plot_energies)
            if self.plot_energies == 'PE':
                self.potential_energy(PE)
                plt.show()
            elif self.plot_energies == 'KE':
                print('hello')
                self.kinetic_energy(KE)
                plt.show()
            elif self.plot_energies == 'TOT':
                self.total_energy(KE, PE)
                plt.show()
            elif self.plot_energies == 'AM':
                self.angular_momentum(AM)
                plt.show()
        else:
            if self.dim == 3:
                self.plot_3D(output_matrix, legend)
            else:
                self.plot_2D(output_matrix, legend)
            if self.filename != None:
                fig.savefig(filename + '.png')
            plt.show()


    def input_data(self):
        """This function creates a 2D matrix containing information on the
        objects mass, position and velocity.

        The information is based on
        NASAs data from september 18th 2018, read from the data file
        planets_distancespeed.txt.

        The positions of the planets is realtive
        to the position of the Sun, placed in origo. The initial speed of the
        sun is zero."""
        # Creating a empty matrix to store the objects data
        input_matrix = np.empty((len(self.objects), 7))
        # Reading inital values from the data file, creating the input matrix
        data = open('planets_data.txt', 'r')
        # Using loops and regular expressions to achieve the data from file
        i = 0
        legend = []
        for lines in data.read().splitlines():
            name = re.findall(r"(^\D+):", lines)
            # Extracting data on the objects of interest
            # Appending the objects name to the list of legends to get the
            # correct order.
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

    """
    def center_of_mass(self, matrix):
        # Changing the positions of all objects relative to center of mass, in origo.
        x = sum(matrix[:, 0]*matrix[:, 1])/sum(matrix[:, 0])
        y = sum(matrix[:, 0]*matrix[:, 2])/sum(matrix[:, 0])
        z = sum(matrix[:, 0]*matrix[:, 3])/sum(matrix[:, 0])
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
        for i in range(1, len(self.objects)):
            # Calculating the numerator first to avoid repetative calculation
            numerator += matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7]
        # Divinding by the mass and position of the Sun
        matrix[0, 4:7] = numerator/(matrix[0, 0]*matrix[0, 1:4])
        # Returning the modified matrix
        return matrix
    """
    def center_of_mass(self, matrix):
        x, y, z = (sum(matrix[:, 0].reshape(len(self.objects), 1)*matrix[:, 1:4])/sum(matrix[:, 0].reshape(len(self.objects), 1)))
        print(x, y, z)
        matrix[:, 1] = matrix[:, 1]-x
        matrix[:, 2] = matrix[:, 2]-y
        matrix[:, 3] = matrix[:, 3]-z
        numerator = np.empty(3)
        for i in range(1, len(self.objects)):
            numerator += matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7]
            #(matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7])/(matrix[0, 0]*matrix[0, 1:4])
        matrix[0, 4:7] = numerator/(matrix[0, 0]*matrix[0, 1:4])
        print(matrix[0, 4:7])
        #sum(matrix[1:, 0]*matrix[1:, 1:4]*matrix[1:, 4:7])/(matrix[0, 0]*matrix[0, 1:4])
        return matrix



    def plot_2D(self, position, legend):
        plt.figure(figsize=(10, 10))
        for i in range(self.numbodies):
            plt.plot(position[i, 0, :], position[i, 1, :])
        plt.xlabel('x [AU]', fontsize=16)
        plt.ylabel('y [AU]', fontsize=16)
        plt.title('The solar system. \n %d years from Sep. 18 2018' %(self.t),\
        fontsize=24)
        plt.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')

    def plot_3D(self, position, legend):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')
        for i in range(self.numbodies):
            ax.plot(position[i, 0, :], position[i, 1, :], position[i, 2, :])
        ax.set_xlabel('x [AU]', fontsize=16)
        ax.set_ylabel('y [AU]', fontsize=16)
        ax.set_zlabel('z [AU]', fontsize=16)
        ax.set_title('The solar system. \n %d years from Sep. 18 2018' \
        %(self.t), fontsize=24)
        ax.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')


    def potential_energy(self, PE):
        x = np.linspace(0, self.t, self.N*self.t+1)
        plt.figure(figsize=(10, 10))
        plt.plot(x, PE)
        plt.suptitle('Total potential energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yrs]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['PE'])

    def kinetic_energy(self, KE):
        x = np.linspace(0, self.t, self.N*self.t+1)
        plt.figure(figsize=(10, 10))
        plt.plot(x, KE)
        plt.suptitle('Total kinetic energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['KE'])

    def total_energy(self, KE, PE):
        x = np.linspace(0, self.t, self.N*self.t+1)
        plt.figure(figsize=(10, 10))
        plt.plot(x, PE+KE)
        plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['KE+PE'])

    def angular_momentum(self, AM):
        amplitude = max(AM)-min(AM)
        print('Amplitude of angular momentum during %i year(s): %g[AU²/yr²]' %(self.t, amplitude))
        x = np.linspace(0, self.t, self.N*self.t+1)
        plt.figure(figsize=(10, 10))
        plt.plot(x, AM)
        plt.suptitle('Total angular momentum in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²/yr²]', fontsize=16)
        plt.legend(['AM'])

    def analyze_AM(self, KE):
        diff = max(KE) - min(KE)
        return diff



if __name__=='__main__':
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
    pa.add_argument('objects', type=str, nargs='+', \
    help='List of planet names to plot. Plot all planets by giving "all" as input \
    argument. Usage: $ filename.py "planet1" "planet2" ...')
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
    pa.add_argument('-plot_energies', type=str, default=None, \
    help = "Plot the kinetic ('KE'), potential('PE') or total ('TOT') enegy, or \
    the angular momentum('AM'), of the system.")
    args = pa.parse_args()
    # Initializing the method with the arguments from the command line.
    ss = solar_system(args.objects[:], args.D, args.t, args.N, args.CM, \
    args.filename, args.method, args.plot_energies)
