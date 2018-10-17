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

numsteps = [1000000, 100000, 10000, 1000, 100, 50]
time_max = 1
legend=[]

for num in numsteps:
    euler = solver(input_matrix, 'euler', time_max, num)
    verlet = solver(input_matrix, 'verlet', time_max, num)

    output_euler = euler.main()
    xEe = output_euler[1, 0, :]
    yEe = output_euler[1, 1, :]

    output_verlet = verlet.main()
    xVe = output_verlet[1, 0, :]
    yVe = output_verlet[1, 1, :]

    if num == numsteps[0]:
        plt.figure(1, figsize=(10, 10))
        plt.plot(xEe, yEe, 'y')
        plt.figure(2, figsize=(10, 10))
        plt.plot(xVe, yVe, 'y')
    else:
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
    plt.axis('equal')
plt.show()




#------------------------------------------------------------------------------
x = np.linspace(0, np.pi*2, numsteps+1)
#plt.plot(x, KE)
#plt.plot(x, PE+KE)
#plt.plot(x, AM)
#plt.show()
