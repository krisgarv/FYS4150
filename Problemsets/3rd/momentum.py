import numpy as np

"""
Finding the initial velocity of the sun when using the center of mass as the origin
Result: v_sun = [-2.20552097e-03  1.21929711e-03  4.42139127e-05]
"""

mass_sun = 1.0
mass_earth = 3E-6
mass_jupiter = 9.5E-4


velocity_earth = np.array([365*-1.833830875310781E-04, 365*1.713325008634928E-02, 365*-2.247700714731761E-07]) #23.09.18
velocity_jupiter = np.array([365*6.361129851123679E-03, 365*-3.570462926243191E-03, 365*-1.275087715416329E-04]) #23.09.18

#Finding the initial velocity of the sun by mv(sun) + mv(earth) + mv(jupiter) = 0:
vel_sun = - (mass_earth*velocity_earth + mass_jupiter*velocity_jupiter)/mass_sun
print(vel_sun)
