import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


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
    for j in range(h):
        for i in range(h):
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

image = mandelbrot(xmin, xmax, ymin, ymax, h, maxiter)

#fig, ax = plt.subplots(figsize=(height, width),dpi=dpi)
fig, ax = plt.subplots(figsize=(10, 10), dpi=72)
ax.imshow(image, cmap='gist_stern' , origin='lower', interpolation='bicubic')
plt.show()
