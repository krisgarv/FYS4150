import numpy as np
import matplotlib.pyplot as plt

"""
In this script we study the orbit of Mercury in two dimensions. The aim is to
find the perihelion precission
"""



# Initial conditions
time_max = 100
num_steps = 1000000*time_max
h = time_max/num_steps
# Pre-calculations to avoid repeating FLOPS
fourpi2 = 4*np.pi**2
h05 = h/2
h205 = h**2/2

# The speed of light in vacuum
#(299792458 × 60 × 60 × 24 / 149597870700) AU/day
c = 299792458*60*60*24*365/149597870700 # [AU/yr]

# Arrays for storing position, velocity and acceleration data
x, y, u, v, ax, ay, r = [np.zeros(num_steps) for i in range(7)]

# Mercurys initial position
x[0] = 0.3075
y[0] = 0.0
# Mercurys initial velocity
u[0] = 0.0
v[0] = 12.44

# Relative distance from origo
r[0] = np.sqrt(x[0]**2 + y[0]**2)
# Magnitude of Mercurys orbital angular momentum per unit mass
l = abs(v[0]*x[0] - u[0]*y[0])
# Correction
corr = (1+3*l**2/(r[0]**2*c**2))
# Corrected Newtonian gravitational force per unit mass
ax[0] = -fourpi2*x[0]/r[0]**2*corr
ay[0] = -fourpi2*y[0]/r[0]**2*corr

# Looping over all steps in the time series
# Storing the relative position, the position, velocity and acceleration for
# further conputation and evaluation.
for i in range(1, num_steps):
    x[i] = x[i-1] + h*u[i-1] + h205*ax[i-1]
    y[i] = y[i-1] + h*v[i-1] + h205*ay[i-1]
    r[i] = np.sqrt(x[i]**2 + y[i]**2)
    l = abs(v[i-1]*x[i] - u[i-1]*y[i])
    corr = (1+3*l**2/(r[i]**2*c**2))
    ax[i] = -fourpi2*x[i]/(r[i]**3)*corr
    ay[i] = -fourpi2*y[i]/(r[i]**3)*corr
    u[i] = u[i-1] + h05*(ax[i-1] + ax[i])
    v[i] = v[i-1] + h05*(ay[i-1] + ay[i])

for i in range(num_steps):
    if r[i] < r[i-1] and r[i] < r[i+1]:
        print(x[i], y[i])

"""
plt.figure(figsize=(10, 10))
plt.plot(x, y)
plt.xlabel('x [AU]\n %i year(s)' %(time_max), fontsize=14)
plt.ylabel('y [AU]', fontsize=14)
plt.title("Mercurys position around the Sun fixed in origo \n %i years."\
%(time_max), fontsize=20)
plt.legend(['with correction'], loc=2, fontsize='small')
plt.axis('equal')
plt.show()
"""
