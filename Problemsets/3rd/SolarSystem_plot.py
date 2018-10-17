from solver_K import solver
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

"""
To use: Write into terminal:

python SolarSystem_plot.py arg1 arg2 arg3 arg4 arg 5 arg6 ...

arg1: Dimensions to be plotted. Enter 2 for 2D or 3 for 3D
arg2: Number of planets. Enter 2 for Earth-Sun. Enter 3 for Earth-Jupiter-Sun
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
    if numbodies == 2:
        #Init.positions:
        position_sun = (0.0, 0.0, 0.0)
        position_earth = (1.0, 0.0, 0.0)
        #Init.velocities:
        velocity_sun = (0.0, 0.0, 0.0)
        velocity_earth = (0.0, 2*np.pi, 0.0)
        #Making initial matrix:
        input_matrix[0, 0] = mass_sun
        input_matrix[1, 0] = mass_earth
        input_matrix[0, 1:4] = position_sun
        input_matrix[1, 1:4] = position_earth
        input_matrix[0, 4:7] = velocity_sun
        input_matrix[1, 4:7] = velocity_earth
    else:
        #Init.positions:
        position_sun = (0.0, 0.0, 0.0)
        position_earth = (1.003549362691021, 1.410236892872957E-03, -7.890400039667053E-05)
        position_jupiter = (-2.795075614391798, -4.586076524625780, 8.154235484924463E-02)
        #Init.velocities:
        velocity_sun = (0.0, 0.0, 0.0)
        velocity_earth = (365*-1.909119143085214E-04, 365*1.713603683351200E-02, 365*-3.683319869509187E-08)
        velocity_jupiter = (365*6.353601024346235E-03, 365*-3.567676179080474E-03, 365*-1.273208346688556E-04)
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
    if numbodies == 2:
        #Init.positions:
        position_sun = (0.0, 0.0, 0.0)
        position_earth = (1.003549362691021, 1.410236892872957E-03, -7.890400039667053E-05)
        #Init.velocities:
        velocity_sun = (0.0, 0.0, 0.0)
        velocity_earth = (365*-1.909119143085214E-04, 365*1.713603683351200E-02, 365*-3.683319869509187E-08)
        #Making initial matrix:
        input_matrix[0, 0] = mass_sun
        input_matrix[1, 0] = mass_earth
        input_matrix[0, 1:4] = position_sun
        input_matrix[1, 1:4] = position_earth
        input_matrix[0, 4:7] = velocity_sun
        input_matrix[1, 4:7] = velocity_earth
    else:
        #Init.positions:
        position_sun = (0.0, 0.0, 0.0)
        position_earth = (1.003549362691021, 1.410236892872957E-03, -7.890400039667053E-05)
        position_jupiter = (-2.795075614391798, -4.586076524625780, 8.154235484924463E-02)
        #Init.velocities:
        velocity_sun = (0.0, 0.0, 0.0)
        velocity_earth = (365*-1.909119143085214E-04, 365*1.713603683351200E-02, 365*-3.683319869509187E-08)
        velocity_jupiter = (365*6.353601024346235E-03, 365*-3.567676179080474E-03, 365*-1.273208346688556E-04)
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
            if numbodies == 2:
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xEe, yEe, 'y')
                legend.append("Earth")
            else:
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                xEj = out_euler[2, 0, :]
                yEj = out_euler[2, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xEe, yEe, 'y')
                plt.plot(xEj, yEj, 'r')
                legend.append("Earth")
                legend.append("Jupiter")

        elif method == "verlet":
            verlet = solver(input_matrix, 'verlet', time_max, num)
            out_verlet, KE_verlet, PE_verlet, AM_verlet = verlet.main()
            if numbodies == 2:
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xVe, yVe, 'y')
                legend.append("Earth")
            else:
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                xVj = out_verlet[2, 0, :]
                yVj = out_verlet[2, 1, :]
                plt.figure(i, figsize=(10, 10))
                plt.plot(xVe, yVe, 'y')
                plt.plot(xVj, yVj, 'r')
                legend.append("Earth")
                legend.append("Jupiter")
        plt.figure(i)
        plt.xlabel('x [AU]')
        plt.ylabel('y [AU]')
        plt.title('Orbit around the Sun (in origo) by using %s, N=%i' %(method,num))
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
            if numbodies == 2:
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                zEe = out_euler[1, 2, :]
                fig = plt.figure(i, figsize=(10,10))
                ax = fig.gca(projection='3d')
                ax.plot(xEe, yEe, zEe, 'y')
                legend.append("Earth")
            else:
                xEe = out_euler[1, 0, :]
                yEe = out_euler[1, 1, :]
                zEe = out_euler[1, 2, :]
                xEj = out_euler[2, 0, :]
                yEj = out_euler[2, 1, :]
                zEj = out_euler[2, 2, :]
                fig = plt.figure(i, figsize=(10, 10))
                ax = fig.gca(projection='3d')
                ax.plot(xEe, yEe, zEe, 'y')
                ax.plot(xEj, yEj, zEj, 'r')
                legend.append("Earth")
                legend.append("Jupiter")

        elif method == "verlet":
            verlet = solver(input_matrix, 'verlet', time_max, num)
            out_verlet, KE_verlet, PE_verlet, AM_verlet = verlet.main()
            if numbodies == 2:
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                zVe = out_verlet[1, 2, :]
                fig = plt.figure(i, figsize=(10,10))
                ax = fig.gca(projection='3d')
                ax.plot(xVe, yVe, zVe, 'y')
                legend.append("Earth")
            else:
                xVe = out_verlet[1, 0, :]
                yVe = out_verlet[1, 1, :]
                zVe = out_verlet[1, 2, :]
                xVj = out_verlet[2, 0, :]
                yVj = out_verlet[2, 1, :]
                zVj = out_verlet[2, 2, :]
                fig = plt.figure(i, figsize=(10,10))
                ax = fig.gca(projection='3d')
                ax.plot(xVe, yVe, zVe, 'y')
                ax.plot(xVj, yVj, zVj, 'r')
                legend.append("Earth")
                legend.append("Jupiter")
        ax.set_xlabel('x [AU]')
        ax.set_ylabel('y [AU]')
        ax.set_zlabel('z [AU]')
        ax.set_title('Orbit around the Sun (in origo) by using %s, N=%i' %(method,num))
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

"""
def energies():
    numsteps = 10000
    time_max = 1
    verlet  = solver(input_matrixelse:
            plt.figure(1)
            plt.plot(xEe, yEe)
            plt.figure(2)
            plt.plot(xVe, yVe)

            legend.append(str(num))
        for i in range(1, 3):
            plt.figure(i)
            plt.xlabel('x [AU]\n %i year(s)' %(time_max))
            plt.ylabel('y [AU]')
            plt.title("Earth's orbit around the Sun (in origo)")
            plt.legend(legend, loc=2, fontsize='small')
            plt.axis('equal'), 'verlet', time_max, numsteps)
    output_matrix, KE, PE, AM = verlet.main()
    x = np.linspace(0, 1, numsteps+1)

    plt.figure(1, figsize=(10, 10))
    plt.plot(x, KE)
    plt.suptitle('Total kinetic energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['KE'])

    plt.figure(2, figsize=(10, 10))
    plt.plot(x, PE)
    plt.suptitle('Total potential energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['PE'])

    plt.figure(3, figsize=(10, 10))
    plt.plot(x, PE+KE)
    plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['KE+PE'])

    plt.figure(4, figsize=(10, 10))
    plt.plot(x, AM)
    plt.suptitle('Total angular momentum in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²/yr²]', fontsize=16)
    plt.legend(['AM'])

    plt.figure(5, figsize=(10, 10))
    plt.plot(x, PE, x, KE, x, KE+PE)
    plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['PE', 'KE', 'KE+PE'])
    plt.show()
"""
if __name__=="__main__":
    start()
