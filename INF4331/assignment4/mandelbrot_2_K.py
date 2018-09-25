import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import time


def fc(z, c, maxiter, horizon=2):
    out = np.empty(c.shape)
    for iterations in range(maxiter):
        cont = np.less(abs(z), horizon)
        out[cont] = iterations
        z[cont] = z[cont]*z[cont] + c[cont]
    return out

def mandelbrot(xmin, xmax, ymin, ymax, h, maxiter, horizon=2):
    x = np.linspace(xmin, xmax, h)
    y = np.linspace(ymin, ymax, h)
    Z = np.empty((h, h))
    c = x + y[:, None]*1j
    z = np.zeros(c.shape, np.complex64)
    Z = fc(z, c, maxiter, horizon)
    return Z


#-----------------------------------------------------------------------
maxiter = 1000
xmin = -2.0
xmax = 0.5
ymin = -1.25
ymax = 1.25
h = 1000

t0=time.time()
image = mandelbrot(xmin, xmax, ymin, ymax, h, maxiter)
t1=time.time()
print ('Time used for maximum %d number of iterations: %fs' %(maxiter, t1-t0))
#fig, ax = plt.subplots(figsize=(height, width),dpi=dpi)
fig, ax = plt.subplots(figsize=(10, 10), dpi=72)
ax.imshow(image, cmap='RdGy' , origin='lower', interpolation='bicubic')
plt.show()
