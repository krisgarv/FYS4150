import cython
import numpy as np



cdef int fc(z, c, int maxiter):
    cdef:
    complex z
    complex c
    int iterations

    for iterations in range(maxiter):
        if abs(z) >= horizon:
            return iterations
        z = z*z + c
    return 0

cpdef mandelbrot(double xmin, double xmax, double ymin double ymax, \
                int h, int maxiter)
    cdef:
        double[:] x = np.linspace(xmin, xmax, h)
        double[:] y = np.linspace(ymin, ymax, h)
        int[:, :] Z = np.empty((h, h), np.int)
        int i, j

    for i in range(h):
        for j in range(h):
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
ax.imshow(image, cmap='gist_stern' , origin='lower', interpolation='bicubic')
plt.show()
