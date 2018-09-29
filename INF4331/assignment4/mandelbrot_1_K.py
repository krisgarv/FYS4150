import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math

def fc(z, c, maxiter, horizon=2):
    for iterations in range(maxiter):
        if abs(z) >= horizon:
            return iterations
        z = z*z + c
    return maxiter

def mandelbrot(xmin, xmax, ymin, ymax, h, maxiter, horizon=2):
    x = np.linspace(xmin, xmax, h)
    y = np.linspace(ymin, ymax, h)
    Z = np.empty((h, h))
    image = np.empty((h, h, 3))
    for j in range(h):
        for i in range(h):
            c = complex(x[j], y[i])
            Z[i, j] = fc(complex(0), c, maxiter, horizon)
            v = float(Z[i, j]/maxiter)
            #RED
            image[i, j, 0] = 1.0/2 - 1.0/2*(np.cos(32.0*np.pi*v/2.0))
            #GREEN
            image[i, j, 1] = 1.0/4 - 1.0/4*(np.cos(104.0*np.pi*v/2.0))
            #BLUE
            image[i, j, 2] = 1.0/2*np.cos(np.pi*v/2.0)
    return image
