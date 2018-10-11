import numpy as np
import matplotlib.pyplot as plt
from ODE_solver import ODE_solver
import time

N = 100000
x0 = 1.0
y0 = 0.0
v_x0 = 0.0
v_y0 = 2*np.pi
def a_x(x, y):
    return -4*x*np.pi**2/((np.sqrt(x*x + y*y))**3)

def a_y(x, y):
    return -4*y*np.pi**2/((np.sqrt(x*x + y*y))**3)


"""
OS = ODE_solver(50, x0, y0, v_x0, v_y0, a_x, a_y)
xE50, yE50 = OS.euler_coupled()
xV50, yV50 = OS.verlet()
OS = ODE_solver(100, x0, y0, v_x0, v_y0, a_x, a_y)
xE100, yE100 = OS.euler_coupled()
xV100, yV100 = OS.verlet()
OS = ODE_solver(1000, x0, y0, v_x0, v_y0, a_x, a_y)
xE1000, yE1000 = OS.euler_coupled()
xV1000, yV1000 = OS.verlet()
"""
OS = ODE_solver(1000, x0, y0, v_x0, v_y0, a_x, a_y)
t0E = time.time()
xE1000, yE1000 = OS.euler_coupled()
t1E = time.time()
timeE = t1E - t0E
t0V = time.time()
xV1000, yV1000 = OS.verlet()
t1V = time.time()
timeV = t1V - t0V

logfile = open('log.txt', 'a')
logfile.write('\nCPU-time Euler: %.05fs\n \
CPU-time Verlet: %.05fs\n ' %(timeE, timeV))
logfile.close()

"""
OS = ODE_solver(1000, x0, y0, v_x0, v_y0, a_x, a_y)
xE100000, yE100000 = OS.euler_coupled()
OS = ODE_solver(1000000, x0, y0, v_x0, v_y0, a_x, a_y)
xE1000000, yE1000000 = OS.euler_coupled()


plt.figure(figsize=(10, 10))
plt.plot(xE1000000, yE1000000,'y', xE100000, yE100000,xE10000, yE10000, xE1000,\
 yE1000,xE100, yE100, xE50, yE50)
plt.axis('equal')
plt.title("Earth's orbit around the Sun (in origo)")
plt.xlabel('x [AU] \n %i integration points' %(N))
plt.ylabel('y [AU]')
plt.legend(['1000000', '100000', '10000', '1000', '100', '50'], loc=2, \
fontsize='small')
plt.show()

plt.figure(figsize=(10, 10))
plt.plot( xV1000, yV1000,'y', xV100, yV100, xV50, yV50)
plt.axis('equal')
plt.title("Earth's orbit around the Sun (in origo)")
plt.xlabel('x [AU] \n %i integration points' %(N))
plt.ylabel('y [AU]')
plt.legend(['1000','100','50'], loc=2, \
fontsize='small')
plt.show()
"""
