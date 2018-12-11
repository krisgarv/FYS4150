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
        #diff = 0.0
        for t in range(1, T):
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[x, y] = (1.0/float(1.+4.*alpha))*(uPrev[x,y] + \
                    alpha*(u_temp[x+1,y] + u_temp[x-1,y] + u_temp[x,y+1] + \
                    u_temp[x,y-1]))
            iter += 1
            diff /= N*2
            uTmp = uPrev
            uPrev = u
    return u

Nx = 50
Ny = 50
dx = 1.0/Nx
dt = 0.001
T  = 1000
L=1.0
Tfinal=0.1
alpha=dt/float(dx**2)
x = np.linspace(0, 1, Nx+2)
y = np.linspace(0, 1, Ny+2)
time = np.linspace(0, Tfinal, T)
u = np.zeros(Nx+2, Ny+2)
u[:, -1] = u[i, 0] = 1.0
u[-1, :] = 1.0

v = JacobiImplicit(alpha, u, N, T)

X,Y =np.meshgrid(x,y)
plt.subplots()
ax = fig.add_subplot(111)


cont=ax.contour(X,Y,u)
plt.tight_layout()
#plt.axis([0.99, 1.0,0.0, 0.03])
plt.xlabel('$x$')
plt.ylabel('$y$')

plt.title('2D diffusion equation with dx= %1.2f, dt= %1.3f, alpha= %1.1f, t= %1.1f '%(dx,dt,alpha,Tfinal))
plt.legend(loc= 'best')
#plt.savefig('boundaryhallo1.pdf')

plt.show()
