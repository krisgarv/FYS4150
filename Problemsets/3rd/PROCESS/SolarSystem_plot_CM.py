from solver_K import solver
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

"""
------------------------------------------------
USE WHEN ORIGO IS IN THE CENTER OF MASS
------------------------------------------------

Using the inital velocity for the Earth and Jupiter found from
NASA HORIZON.
------------------------------------------------

To use, write into terminal:
python SolarSystem_plot.py arg1 arg2 arg3 arg4 arg 5 arg6 ...

arg1: Dimensions to be plotted. Enter 2 for 2D or 3 for 3D
arg2: Number of planets. Enter 3 for Earth-Jupiter-Sun
arg3: Method to be used. Type either euler or verlet
arg4: Maximum time (time_max)
arg5 arg6 ...: The values of N that you want to run the program for, minimum
one input.
"""

mass_sun = 1.0
mass_earth = 3E-6
mass_jupiter = 9.5E-4

#----------------------------------------------------------------------------
def input_matrix_2D(numbodies):
    input_matrix = np.zeros((numbodies, 7))
    if numbodies == 3:
        #Init.positions:
        position_sun = (2.64979664e-03, 4.35946834e-03, -7.74642213e-05)
        position_earth = (1.003538121253694+2.64979664e-03, 1.410236892872957E-03+4.35946834e-03, -7.890400039667053E-05-7.74642213e-05)
        position_jupiter = (-2.795086855829125+2.64979664e-03, -4.593269013324874+4.35946834e-03, 8.161900152196526E-02-7.74642213e-05)
        #Init.velocities:
        velocity_sun = (-2.20552097e-03, 1.21929711e-03, 4.42139127e-05)
        velocity_earth = (365*-1.833830875310781E-04, 365*1.713325008634928E-02, 365*-2.247700714731761E-07)
        velocity_jupiter = (365*6.361129851123679E-03, 365*-3.570462926243191E-03, 365*-1.275087715416329E-04)
        #Making initial matrix:
        input_matrix[0, 0] = mass_sun
        input_matrix[1, 0] = mass_earth
        input_matrix[2, 0] = mass_jupiter
        input_matrix[0, 1:4] = position_sun
        input_matrix[1, 1:4] = position_earth
        input_matrix[2, 1:4] = position_jupiter
        input_matrix[0, 4:7] = velocity_sun
        input_matrix[1, 4:7] = velocity_earth
        input_matrix[2, 4:7] = velocity_jupiter
    return(input_matrix)
#----------------------------------------------------------------------------
def input_matrix_3D(numbodies):
    input_matrix = np.zeros((numbodies, 7))
    if numbodies == 3:
        #Init.positions:
        position_sun = (2.64979664e-03, 4.35946834e-03, -7.74642213e-05)
        position_earth = (1.003538121253694+2.64979664e-03, 1.410236892872957E-03+4.35946834e-03, -7.890400039667053E-05-7.74642213e-05)
        position_jupiter = (-2.795086855829125+2.64979664e-03, -4.593269013324874+4.35946834e-03, 8.161900152196526E-02-7.74642213e-05)
        #Init.velocities:
        velocity_sun = (-2.20552097e-03, 1.21929711e-03, 4.42139127e-05)
        velocity_earth = (365*-1.833830875310781E-04, 365*1.713325008634928E-02, 365*-2.247700714731761E-07)
        velocity_jupiter = (365*6.361129851123679E-03, 365*-3.570462926243191E-03, 365*-1.275087715416329E-04)
        #Making initial matrix:
        input_matrix[0, 0] = mass_sun
        input_matrix[1, 0] = mass_earth
        input_matrix[2, 0] = mass_jupiter
        input_matrix[0, 1:4] = position_sun
        input_matrix[1, 1:4] = position_earth
        input_matrix[2, 1:4] = position_jupiter
        input_matrix[0, 4:7] = velocity_sun
        input_matrix[1, 4:7] = velocity_earth
        input_matrix[2, 4:7] = velocity_jupiter
    return(input_matrix)
#----------------------------------------------------------------------------

def plot_2D(input_matrix, numbodies, method, time_max, numsteps):
    i = 0
    for num in numsteps:
        legend = []
        i += 1
        if method == "euler":
            euler = solver(input_matrix, 'euler', time_max, num)
            out_euler, KE_euler, PE_euler, AM_euler = euler.main()
            if numbodies == 3:
                xEs = out_euler[0, 0, :]
                yEs = out_euler[0, 1, :]
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                xEj = out_euler[2, 0, :]
                yEj = out_euler[2, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xEs, yEs, 'y')
                plt.plot(xEe, yEe, 'g')
                plt.plot(xEj, yEj, 'r')
                legend.append("Sun")
                legend.append("Earth")
                legend.append("Jupiter")

        elif method == "verlet":
            verlet = solver(input_matrix, 'verlet', time_max, num)
            out_verlet, KE_verlet, PE_verlet, AM_verlet = verlet.main()
            if numbodies == 3:
                xVs = out_verlet[0, 0, :]
                yVs = out_verlet[0, 1, :]
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                xVj = out_verlet[2, 0, :]
                yVj = out_verlet[2, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xVs, yVs, 'y')
                plt.plot(xVe, yVe, 'g')
                plt.plot(xVj, yVj, 'r')
                legend.append("Sun")
                legend.append("Earth")
                legend.append("Jupiter")
        plt.figure(i)
        plt.xlabel('x [AU]')
        plt.ylabel('y [AU]')
        plt.title('Orbits (Sun in origo) by using %s, N=%i' %(method,num))
        plt.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')
        plt.show()
#----------------------------------------------------------------------------

def plot_3D(input_matrix, numbodies, method, time_max, numsteps):
    i = 0
    for num in numsteps:
        legend = []
        i +=1
        if method == "euler":
            euler = solver(input_matrix, 'euler', time_max, num)
            out_euler, KE_euler, PE_euler, AM_euler = euler.main()
            if numbodies == 3:
                xEs = out_euler[0, 0, :]
                yEs = out_euler[0, 1, :]
                zEs = out_euler[0, 2, :]
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                zEe = out_euler[1, 2, :]
                xEj = out_euler[2, 0, :]
                yEj = out_euler[2, 1, :]
                zEj = out_euler[2, 2, :]
                fig = plt.figure(i, figsize=(10, 10))
                ax = fig.gca(projection='3d')
                ax.plot(xEs, yEs, zEs, 'y')
                ax.plot(xEe, yEe, zEe, 'g')
                ax.plot(xEj, yEj, zEj, 'r')
                legend.append("Sun")
                legend.append("Earth")
                legend.append("Jupiter")

        elif method == "verlet":
            verlet = solver(input_matrix, 'verlet', time_max, num)
            out_verlet, KE_verlet, PE_verlet, AM_verlet = verlet.main()
            if numbodies == 3:
                xVs = out_verlet[0, 0, :]
                yVs = out_verlet[0, 1, :]
                zVs = out_verlet[0, 2, :]
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                zVe = out_verlet[1, 2, :]
                xVj = out_verlet[2, 0, :]
                yVj = out_verlet[2, 1, :]
                zVj = out_verlet[2, 2, :]
                fig = plt.figure(i, figsize=(10,10))
                ax = fig.gca(projection='3d')
                ax.plot(xVs, yVs, zVs, 'y')
                ax.plot(xVe, yVe, zVe, 'g')
                ax.plot(xVj, yVj, zVj, 'r')
                legend.append("Sun")
                legend.append("Earth")
                legend.append("Jupiter")
        ax.set_xlabel('x [AU]')
        ax.set_ylabel('y [AU]')
        ax.set_zlabel('z [AU]')
        ax.set_title('Orbits (Sun in origo) by using %s, N=%i' %(method,num))
        ax.legend(legend, loc=2, fontsize='small')
        plt.axis('equal')
        plt.show()

#----------------------------------------------------------------------------

def start():
    plot_dimension = int(sys.argv[1])
    numbodies = int(sys.argv[2])
    method = sys.argv[3]
    time_max = int(sys.argv[4])
    numsteps = [int(number) for number in sys.argv[5::]]

    if plot_dimension == 2:
        input_matrix = input_matrix_2D(numbodies)
        plot_2D(input_matrix, numbodies, method, time_max, numsteps)
    else:
        input_matrix = input_matrix_3D(numbodies)
        plot_3D(input_matrix, numbodies, method, time_max, numsteps)

#------------------------------------------------------------------------------

if __name__=="__main__":
    start()
