import numpy as np
import matplotlib.pyplot as plt
import solver as s

def JacobiImplicit(alpha, u, N, T):
    eps = 10e-8
    diff = eps + 1
    iter = 0
    maxiter = N**3
    uPrev = np.zeros((N+2, N+2))
    uTmp = np.zeros_like(uPrev)
    uPrev = u
    uTmp = uPrev
    while (diff > eps and iter < maxiter):
        diff = 0.0
        for t in range(1, T):
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[x, y] = (1.0/(1.0+4.0*alpha))*(uPrev[x,y] + \
                    alpha*(uTmp[x+1,y] + uTmp[x-1,y] + uTmp[x,y+1] + \
                    uTmp[x,y-1]))
            iter += 1
            diff /= N*2
            uTmp = uPrev
            uPrev = u
    return u

def analytic2D(x, N):
    plt.figure()
    t = x
    X,Y =np.meshgrid(x,t)
    u=np.zeros_like(X)
    for k in range(1, N):
        u += 2*np.sin(k*np.pi*x)*np.exp(np.pi*np.sqrt(2.0*k)*t)
    u = 4.0*u/float(np.pi)
    #plt.plot(u, x, 'C{}'.format(i), label='t={}'.format(t))
    plt.contour(X, Y, u)
    plt.xlabel('x')
    plt.ylabel('u(t, x)')
    #plt.legend()
    plt.title('Analytical soluion of 2D diffusion equation')

N = 50
N = 50
dx = 1.0/N
dt = 0.001
T  = 1000
L=1.0
Tfinal=0.1 # Brukes ikke til noe...
alpha=dt/float(dx**2)
x = np.linspace(0, 1, N+2)
y = np.linspace(0, 1, N+2)
time = np.linspace(0, Tfinal, T) # Brukes ikke til noe...
u = np.zeros((N+2, N+2))
u[:, -1] = u[:, 0] = 1.0
u[-1, :] = 1.0

v = JacobiImplicit(alpha, u, N, T)

X,Y =np.meshgrid(x,y)
plt.contour(X, Y, v)
plt.title('Numerical soluion of 2D diffusion equation')
plt.xlabel('x')
plt.ylabel('y')
analytic2D(x, N)
plt.show()
