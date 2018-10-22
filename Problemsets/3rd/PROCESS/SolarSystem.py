from solver_K import solver
import numpy as np
import matplotlib.pyplot as plt



mass_sun = 1.0
mass_earth = 3E-6

position_sun = (0.0, 0.0, 0.0)
position_earth = (1.0, 0.0, 0.0)

velocity_sun = (0.0, 0.0, 0.0)
velocity_earth = (0.0, 2*np.pi, 0.0)


input_matrix = np.zeros((2, 7))
input_matrix[0, 0] = mass_sun
input_matrix[1, 0] = mass_earth
input_matrix[0, 1:4] = position_sun
input_matrix[1, 1:4] = position_earth
input_matrix[0, 4:7] = velocity_sun
input_matrix[1, 4:7] = velocity_earth

#----------------------------------------------------------------------------
def euler_or_verlet(method):

    time_max = 4
    legend=[]
    if method == 'euler':
        numsteps = [1000000, 100000, 10000, 1000, 100, 50]
        for num in numsteps:
            euler = solver(input_matrix, 'euler', time_max, num)
            output_euler, KE, PE, AM = euler.main()
            xEe = output_euler[1, 0, :]
            yEe = output_euler[1, 1, :]
            plt.figure(figsize=(10, 10))
            plt.plot(xEe, yEe)
            legend.append(str(num))

    elif method == 'verlet':
        numsteps = [1000]
        for num in numsteps:
            verlet = solver(input_matrix, 'verlet', time_max, num)
            output_verlet, KE, PE, AM = verlet.main()
            xVe = output_verlet[1, 0, :]
            yVe = output_verlet[1, 1, :]
            plt.figure(figsize=(10, 10))
            plt.plot(xVe, yVe)
            legend.append(str(num))
    plt.xlabel('x [AU]\n %i year(s)' %(time_max))
    plt.ylabel('y [AU]')
    plt.title("Earth's orbit around the Sun (in origo)")
    plt.legend(legend, loc=2, fontsize='small')
    plt.axis('equal')
    plt.show()

#euler_or_verlet('verlet')





#------------------------------------------------------------------------------


def energies():
    numsteps = 10000
    time_max = 1
    verlet  = solver(input_matrix, 'verlet', time_max, numsteps)
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


def analyze_AM():
    time_max = 1
    numsteps = 10000
    verlet  = solver(input_matrix, 'verlet', time_max, numsteps)
    output_matrix, KE, PE, AM = verlet.main()
    diff = max(KE) - min(KE)
    return diff

print(analyze_AM())
