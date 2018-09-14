import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

xmin = -2.0
xmax = 1.0
ymin = -1.5
ymax = 1.5
horizon = 2.0
maxiter = 50
h = 1000

x = np.linspace(xmin, xmax, h)
y = np.linspace(ymin, ymax, h)
Z = np.zeros((len(x), len(y)))

def fc(z, c, temp_iter = 0):
    if abs(z) >= horizon:
        return temp_iter
    else:
        if temp_iter < maxiter:
            z = complex(z.real**2 - z.imag**2 + c.real, 2*z.real*z.imag + c.imag)
            return fc(z, c, temp_iter + 1)
        else:
            return temp_iter

for j in range(len(x)):
    for i in range(len(y)):
        c = complex(x[j], y[i])
        Z[i][j] = fc(complex(0), c)

plt.imshow(Z)
plt.show()
