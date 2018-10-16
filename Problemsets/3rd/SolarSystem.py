from solver_K import solver
import numpy as np
import matplotlib.pyplot as plt
# __init__(self, input_matrix, method, time_max, num_steps):

mass_sun = 1.0
mass_earth = 3E-6

position_sun = (0.0, 0.0, 0.0)
position_earth = (1.0, 0.0, 0.0)

velocity_sun = (0.0, 0.0, 0.0)
velocity_earth = (0.0, 2*np.pi, 0.0)

numbodies = 2
numsteps = 100

input_matrix = np.zeros((2, 7))
input_matrix[0, 0] = mass_sun
input_matrix[1, 0] = mass_earth
input_matrix[0, 1:4] = position_sun
input_matrix[1, 1:4] = position_earth
input_matrix[0, 4:7] = velocity_sun
input_matrix[1, 4:7] = velocity_earth
sol = solver(input_matrix, 'verlet', 1, numsteps)
output_matrix, KE, PE, AM = sol.main()
x_earth = output_matrix[1, 0, :]
y_earth = output_matrix[1, 1, :]

#plt.plot(x_earth, y_earth)
#plt.axis('equal')
#plt.show()

x = np.linspace(0, np.pi*2, numsteps+1)
#plt.plot(x, KE)
plt.plot(x, PE+KE)
#plt.plot(x, AM)
plt.show()

"""
mass = np.zeros(num_objects)
position = np.zeros(3, num_objects)
velocity = np.zeros(3, num_objects)


solver.relative_position(self, numbodies, position)
solver.forces(self, numbodies, realposition, mass)
solver.calc_position(self, numbodies, position, velocity, relforce, tmax, num_steps)
solver.calc_velocities(self, numbodies, velocity, relforce, updatedforce, tmax, num_steps)
solver.kinetic_energy(self, numbodies, mass, kinetic, velocity)
solver.potential_energy(self, numbodies, potential, mass, relposition)
solver.angular_momentum(self, numbodies, mass, relposition, velocity)
"""
