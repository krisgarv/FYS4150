from solver import solver
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import re

class solar_system(object):

    """
    This method uses information on planets mass, position and velocity, extracted
    from NASA data at september 18th 2018. It calculates the position of selected
    objects in the solar system as a function of time using the velocity Verlet
    method to integate Newtons law of gravitation. This operation is done by the
    solver method found in solver.py. \n
    Finally the method plot the positions of the selected objects in 2 or 3
    dimensions.\n
    The method has additional functions to plot the kinetic, potential or total
    energy or angular momentum of the system. 
    """
    def __init__(self, objects, dimension, time_max, num_steps, \
    CM, method, plot_energies):
        """
        To make use of the method you must provide a list of object names
        i.e. $ python solar_system "Eeath" "Merkury" "..." \n
        If no other input is givern, the method will produce a 2D plot of the objects
        position over one year with the center of the Sun placed in origo, given
        zero initial velocity, By default 500 integration point are used for the
        velocity Verlet method.\n
        There are several optional functionalities that can be applied through the
        command line or input. See help flag for more information:\n
        $ python solar_system --help
        """
        # Let the user plot all planets without listing all elements as input
        if 'all' in objects:
            objects = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', \
            'Saturn', 'Uranus', 'Neptune', 'Pluto']
        # The sun is not optional, will be added to list of objects
        if 'Sun' not in objects:
            objects.append('Sun')
        # Initializing input variables
        self.objects = objects
        self.dim = dimension
        self.numbodies = len(self.objects)
        self.t = time_max
        self.N = num_steps
        self.CM = CM
        self.method = method
        self.plot_energies = plot_energies

    def main(self):
        """
        The main program coordinates all the functionalities of the method and
        executes the plotting that has been demanded.
        """
        # Creating the inpust matrix for the solver method using the input_data
        # function
        input_matrix, legend = self.input_data()
        # Adjusting the input matrix if origo is to be set at the center of mass
        # instead of center of initial origo
        if self.CM is True:
            input_matrix = self.center_of_mass(input_matrix)
        # Inintialiszing the solver method with the selected input
        I = solver(input_matrix, self.method, self.t, self.N)
        # Running the solver, extracting a position matrix and arrays conatining
        # information on the energies and angular momentum of the system
        output_matrix, KE, PE, AM = I.main()
        # If the optional variable plot_energies is given a input string that
        # matches the code names, the selected energies or momentum will be plotted
        # and the positional plots will be supressed
        if self.plot_energies != None:
            if self.plot_energies == 'PE':
                self.potential_energy(PE)
            elif self.plot_energies == 'KE':
                self.kinetic_energy(KE)
            elif self.plot_energies == 'TOT':
                self.total_energy(KE, PE)
            elif self.plot_energies == 'AM':
                self.angular_momentum(AM)
            plt.show()
        # If the optional variable -D is called and given 3 as argument, the
        # positions will be plotted in three dimensions.
        else:
            if self.dim == 3:
                self.plot_3D(output_matrix, legend)
            # The positions are plotted in three dimensions as default
            else:
                self.plot_2D(output_matrix, legend)
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


    def center_of_mass(self, matrix):
        """
        This function calculates the center of mass for the selected objects
        of the system. It then shifts all positions realtive to origo, to their
        updated positions relative to the calculated center of mass (in origo).
        The function then gives the Sun an initial velocity which makes the
        momentum of the system zero.
        """
        # Changing the positions of all objects relative to center of mass, in origo.
        x, y, z = np.sum(matrix[:, 0].reshape(self.numbodies, 1)*matrix[:, 1:4], axis=0)/(np.sum(matrix[:, 0], axis=0))
        print('Center of mass located at (%.4g, %.4g, %.4g)' %(x, y, z))
        # x-direction
        matrix[:, 1] = matrix[:, 1]-x
        # y-direction
        matrix[:, 2] = matrix[:, 2]-y
        # z-direction
        matrix[:, 3] = matrix[:, 3]-z
        # The Suns initial velocity which makes the total momentum of the system zero
        # velcity_sun = sum(mass_planet_i*veocity_planet_i)/(mass_sun)
        u, v, w = np.sum(matrix[:, 0].reshape(self.numbodies, 1)*matrix[:, 4:7], axis=0)/(matrix[0, 0])
        print('The initial velocity of the Sun (%.4g, %.4g, %.4g)' %(u, v, w))
        matrix[0, 4:7] = u, v, w
        # Returning the modified matrix
        return matrix


    def plot_2D(self, position, legend):
        """
        This function plots the position of the selected objects in two dimensions.
        Labeling the objects with the label made by the input_data function.
        """
        # Initializing figure
        plt.figure(figsize=(10, 10))
        # Looping over all object arrays in the position matrix,
        # adding it to the plot
        for i in range(self.numbodies):
            plt.plot(position[i, 0, :], position[i, 1, :])
        # Decorating the plot
        plt.xlabel('x [AU]', fontsize=16)
        plt.ylabel('y [AU]', fontsize=16)
        plt.title('The solar system. \n %d years from Sep. 18 2018' %(self.t),\
        fontsize=24)
        plt.legend(legend, loc=2, fontsize='small')
        plt.grid(True)
        plt.axis('equal')

    def plot_3D(self, position, legend):
        """
        This function plots the position of the selected objects in three dimensions.
        Labeling the objects with the label made by the input_data function.
        """
        # Initializing the figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')
        # Looping over all object arrays in the position matrix,
        # adding it to the plot
        for i in range(self.numbodies):
            ax.plot(position[i, 0, :], position[i, 1, :], position[i, 2, :])
        # Decorating the plot
        ax.set_xlabel('x [AU]', fontsize=16)
        ax.set_ylabel('y [AU]', fontsize=16)
        ax.set_zlabel('z [AU]', fontsize=16)
        ax.set_title('The solar system. \n %d years from Sep. 18 2018' \
        %(self.t), fontsize=24)
        ax.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')

    def potential_energy(self, PE):
        """
        This function plots the Potential energy of the system against time.
        """
        # Creating an axis for the time steps
        x = np.linspace(0, self.t, self.N*self.t+1)
        # Initializing the figure
        plt.figure(figsize=(10, 10))
        # Creating the plot
        plt.plot(x, PE)
        # Decorating the plot
        plt.suptitle('Total potential energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yrs]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['PE'])

    def kinetic_energy(self, KE):
        """
        This function plots the Kinetic energy of the system against time.
        """
        # Creating an axis for the time steps
        x = np.linspace(0, self.t, self.N*self.t+1)
        # Initializing the figure
        plt.figure(figsize=(10, 10))
        # Creating the plot
        plt.plot(x, KE)
        # Decorating the plot
        plt.suptitle('Total kinetic energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['KE'])

    def total_energy(self, KE, PE):
        """
        This function creates a plot showing the total energy of the system
        together with the kinetic energy and the potential energy. It also
        prints the difference between the maximum and minimum total energy during
        the selected time period.
        """
        TOT = KE+PE
        # Printing the amplitude to command line
        amplitude = max(TOT)-min(TOT)
        print('Amplitude of total energy during %i year(s): %g[AU²*kg/yr²]' \
        %(self.t, amplitude))
        # Creating an axis for the time steps
        x = np.linspace(0, self.t, self.N*self.t+1)
        # Initializing the second figure
        plt.figure(figsize=(10, 10))
        # Creating the plot
        plt.plot(x, KE, x, PE, x, KE+PE)
        # Decorating the plot
        plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
        plt.legend(['KE', 'PE', 'KE+PE'], loc=2)

    def angular_momentum(self, AM):
        """
        This function plots the angular momentum of the system against time.
        It also prints the difference between the maximum and minimum angular
        momentum during the selected time period.
        """
        # Printing the amplitude to command line
        amplitude = max(AM)-min(AM)
        print('Amplitude of angular momentum during %i year(s): %g[AU²/yr²]' \
        %(self.t, amplitude))
        # Creating an axis for the time steps
        x = np.linspace(0, self.t, self.N*self.t+1)
        # Initializing the figure
        plt.figure(figsize=(10, 10))
        # Creating the plot
        plt.plot(x, AM)
        # Decorating the plot
        plt.suptitle('Total angular momentum in the Earth-Sun system.', fontsize=24)
        plt.xlabel('time [yr]', fontsize=16)
        plt.ylabel('energy [AU²/yr²]', fontsize=16)
        plt.legend(['AM'])

if __name__=='__main__':
    # Using argparse to make a nice help flag to describe the usage of this
    # program
    pa = argparse.ArgumentParser(description='This program calculates and \
    plots the position, potential or kinetic energy or angular momentum of \
    objects of your choosing.\
    The position of the objects can be plotted in two or three dimensions.', \
    epilog='This script \
    uses the method solver.py and the data file planets_distancespeed.txt, \
    make sure that you have all files in your directory.\n \
    The program uses the the solver method to calculate Newtons law of \
    gravitation and thereby the objects position by the Euler or velocity \
    Verlet method. If provided the program can plot the potential, kinetic or\
    total energy of the system, or the angular momentum as functions of time.\n \
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
    increase number of integration points for the system to stabilize. \n \
    USAGE: \n \
    $ python solar_system.py "Planetname1" "Planetname2" -optional_variable=... \
    -optional_variable=...')
    pa.add_argument('objects', type=str, nargs='+', \
    help='List of planet names to plot. Plot all planets by giving "all" as input \
    argument.')
    pa.add_argument('-D', type=int, default=2, \
    help='Which dimension to plot, 2D or 3D (integer).')
    pa.add_argument('-t', type=int, default=10, \
    help='Number of years (integer) to be plotted.')
    pa.add_argument('-N', type=int, default=1000, \
    help='Integration points (integer) per year.')
    pa.add_argument('-CM', type=bool, default=False, \
    help='Shift origo to center of mass (boolean variable). If true: Initial \
    position and velocity of the sun and relative positions are calculated. ')
    pa.add_argument('-method', type=str, default='verlet', help='Integration \
    method, velocity Verlet ot Eulers method. Velocity Verlet is far more \
    efficient and are therefore set as default.')
    pa.add_argument('-plot_energies', type=str, default=None, \
    help = "Plot the kinetic ('KE'), potential('PE') or total ('TOT') enegy, or \
    the angular momentum('AM'), of the system.")
    args = pa.parse_args()
    # Initializing the method with the arguments from the command line.
    ss = solar_system(args.objects[:], args.D, args.t, args.N, args.CM, \
    args.method, args.plot_energies)
    ss.main()
