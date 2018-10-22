import numpy as np
import matplotlib.pyplot as plt
from solver import solver

"""This program plots the engergy balance in a simple two-object system, namely
the Earth-Sun-system.
For simplicity the center of the Sun placed in origo which has no
initial velocity. The Earth is initially placed in the xy-plane at
x = 1 AU, y = 0. All calculations are done with the verlet method with 10000
integration steps in the class solver."""

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

def energies():
    """This function takes no positional arguments as it is made only to
    calculate the energies and angular momentum for a simlified Earth-Sun-system.
    It returns five plots: potential energy, kinetic energy, total energy,
    angular momentum and total energy together with kinetic and potential.

    To calculate these quantities for a more complex sysytem, use the method
    solar_system which also has buildt in methods for plotting the energies
    and angulat momentum against time."""
    # Hardcoded initial values
    numsteps = 10000
    time_max = 1
    # Running the calculation in the solver class using the velocity verlet method
    # for better accuracy.
    verlet  = solver(input_matrix, 'verlet', time_max, numsteps)
    output_matrix, KE, PE, AM = verlet.main()
    # Creating a simple time axis for plotting
    x = np.linspace(0, 1, numsteps+1)

    # Plotting kinetic energy over time
    plt.figure(1, figsize=(10, 10))
    plt.plot(x, KE)
    plt.suptitle('Total kinetic energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['KE'])

    # Plotting potential energy over time
    plt.figure(2, figsize=(10, 10))
    plt.plot(x, PE)
    plt.suptitle('Total potential energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['PE'])

    # Plotting total energy against time
    plt.figure(3, figsize=(10, 10))
    plt.plot(x, PE+KE)
    plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['KE+PE'])

    # Plotting angular momentum against time. print the amplitude to terminal
    amplitude = max(AM)-min(AM)
    print('Amplitude of angular momentum during 1 year: %g[AU²/yr²]' %(amplitude))
    plt.figure(4, figsize=(10, 10))
    plt.plot(x, AM)
    plt.suptitle('Total angular momentum in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²/yr²]', fontsize=16)
    plt.legend(['AM'])

    # Plotting the kinetic, potential and total energy against time to see
    # how great the variations are
    plt.figure(5, figsize=(10, 10))
    plt.plot(x, PE, x, KE, x, KE+PE)
    plt.suptitle('Total energy in the Earth-Sun system.', fontsize=24)
    plt.xlabel('time [yr]', fontsize=16)
    plt.ylabel('energy [AU²*kg/yr²]', fontsize=16)
    plt.legend(['PE', 'KE', 'KE+PE'])
    plt.show()

# Executed if called from command line
if __name__ == '__main__':
    energies()
