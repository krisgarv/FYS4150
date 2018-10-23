from solver import solver
import numpy as np
import matplotlib.pyplot as plt

# Mass
mass_sun = 1.0
mass_mercury = 1.6602e-07
# Initial position
position_sun = (0.0, 0.0, 0.0)
position_mercury = (0.3075, 0.0, 0.0)
# Initial velocity
velocity_sun = (0.0, 0.0, 0.0)
velocity_mercury = (0.0, 12.44, 0.0)
# Creating the input matrix
input_matrix = np.zeros((2, 7))
input_matrix[0, 0] = mass_sun
input_matrix[1, 0] = mass_mercury
input_matrix[0, 1:4] = position_sun
input_matrix[1, 1:4] = position_mercury
input_matrix[0, 4:7] = velocity_sun
input_matrix[1, 4:7] = velocity_mercury

time_max = 100
num_steps = 1000
sol = solver(input_matrix, 'verlet', time_max, num_steps, perihelion=True)
out_position, KE, PE, AM = sol.main()

xM = out_position[1, 0, :]
yM = out_position[1, 1, :]
zM = out_position[1, 2, :]

sol2 = solver(input_matrix, 'verlet', time_max, num_steps)
out_position, KE, PE, AM = sol2.main()
xM2 = out_position[1, 0, :]
yM2 = out_position[1, 1, :]
plt.plot(xM, yM, xM2, yM2)
plt.show()
"""
# Initializing the figure
fig = plt.figure(figsize=(10, 10))
ax = fig.gca(projection='3d')
ax.plot(xM, yM, zM)
# Decorating the plot
ax.set_xlabel('x [AU]', fontsize=16)
ax.set_ylabel('y [AU]', fontsize=16)
ax.set_zlabel('z [AU]', fontsize=16)
ax.set_title('The solar system. \n %d years from Sep. 18 2018' \
%(self.t), fontsize=20)
ax.legend(legend, loc=2, fontsize='small')
"""
plt.axis('equal')
plt.show
