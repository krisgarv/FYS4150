from numba import jit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import time

@jit
def fc(z, c, maxiter, horizon=2):
    for iterations in range(maxiter):
        if abs(z) >= horizon:
            return iterations
        z = z*z + c
    return maxiter

def mandelbrot(xmin, xmax, ymin, ymax, h, maxiter, horizon=2):
    x = np.linspace(xmin, xmax, h)
    y = np.linspace(ymin, ymax, h)
    Z = np.empty((len(x), len(y)))
    for j in range(len(x)):
        for i in range(len(y)):
            c = complex(x[j], y[i])
            Z[i][j] = fc(complex(0), c, maxiter, horizon)
    return Z

#-----------------------------------------------------------------------
maxiter = 1000
xmin = -2.0
xmax = 0.5
ymin = -1.25
ymax = 1.25
h = 500

t0=time.time()
image = mandelbrot(xmin, xmax, ymin, ymax, h, maxiter)
t1=time.time()
print ('Time used for maximum %d number of iterations: %fs' %(maxiter, t1-t0))
#fig, ax = plt.subplots(figsize=(height, width),dpi=dpi)
fig, ax = plt.subplots(figsize=(10, 10), dpi=72)
ax.imshow(image, cmap='nipy_spectral_r' , origin='lower', interpolation='bicubic')
plt.show()
