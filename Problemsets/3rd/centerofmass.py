import numpy as np

"""
Result: CM = [-2.64979664e-03, -4.35946834e-03, 7.74642213e-05] from the Sun at [0,0,0]
"""

mass_sun = 1.0
mass_earth = 3E-6
mass_jupiter = 9.5E-4
position_sun = [0.0, 0.0, 0.0]
position_earth = np.array([1.003538121253694, -5.782251806221399E-03, -2.257327676060083E-06]) #23.09.18
position_jupiter = np.array([-2.795086855829125, -4.593269013324874, 8.161900152196526E-02]) #23.09.18

# Center of mass: CM = sum(mass_i * pos_i)/M, where M = sum(mass_i)
CM = (mass_earth*position_earth + mass_jupiter*position_jupiter)/(mass_earth + mass_sun + mass_jupiter)
print(CM)

"""
#New positions after changing the coordinate origin to be in the center of mass:
position_CM_sun = np.array([2.64979664e-03, 4.35946834e-03, -7.74642213e-05])
position_CM_earth = np.array([1.003538121253694+2.64979664e-03, 1.410236892872957E-03+4.35946834e-03, -7.890400039667053E-05-7.74642213e-05]) #23.09.18
position_CM_jupiter = np.array([-2.795086855829125+2.64979664e-03, -4.593269013324874+4.35946834e-03, 8.161900152196526E-02-7.74642213e-05]) #23.09.18
"""
