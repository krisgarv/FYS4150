# Input arguments: u(x), n

from math import *
import matplotlib.pyplot as plt

x0 = 0.0
xn = 1.0
n = 100
h = (xn - x0)/(n)

def func(z):
    return 100.0*exp(-10.0*z)

x = []
f = []
d_tilde = []

for i in range (0, n+1):
    xi = x0 + h*i
    x.append(xi)
    fi = func(xi)
    f.append(fi)
    d = fi*h**2
    d_tilde.append(d)

print (x[n])
print(h)
print (d_tilde)
#print (f)
plt.plot(x, f)
plt.show()
