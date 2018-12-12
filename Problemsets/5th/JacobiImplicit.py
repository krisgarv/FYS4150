import numpy as np
import matplotlib.pyplot as plt
import solver as s

def JacobiImplicit(alpha, u, N, T):
    tol = 10e-7
    diff = tol + 1
    iter = 0
    maxiter = N**3
    uPrev = np.zeros((N+2, N+2))
    uTmp = np.zeros_like(uPrev)
    uPrev = u
    uTmp = uPrev
    while (diff >= tol and iter < maxiter):
        diff = 0.0
        for t in range(1, T+1):
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[y, x] = (1.0/(1.0+4.0*alpha))*(uPrev[y, x] + \
                    alpha*(uTmp[y, x+1] + uTmp[y, x-1] + uTmp[y+1, x] + \
                    uTmp[y-1, x]))
            iter += 1
            diff = np.max(np.abs(u - uTmp))
            uTmp = uPrev
            uPrev = u
    return u

def analytic2D(x, y, N):
    for t in t_list:
        plt.figure()
        X,Y = np.meshgrid(x,y)
        print(X)
        print(Y)

        u = np.sin(np.pi*X)*np.sin(np.pi*Y)*np.exp(-2*np.pi**2*t)
        #for k in range(1, N):
            #for l in range(1, N):
                #u += np.sin(k*np.pi*X)*np.sin(l*np.pi*Y)*np.exp(np.pi**2*(l**2+k**2)*t)
        #plt.plot(u, x, 'C{}'.format(i), label='t={}'.format(t))
        plt.contour(X, Y, u)
        plt.xlabel('x')
        plt.ylabel('u(x, y, t)')
        #plt.legend()
        plt.title('Analytical soluion of 2D diffusion equation')


N       = 50
dx      = 1.0/N
dt      = 0.5*(dx**2)
alpha   = dt/(dx**2)

# The time-values we want to plot. Minimum time is 0, maximum is 1:
t_list  = [0.001, 0.01, 0.03, 0.08, 0.3, 1]
t_max   = 1
# Number of time steps from 0 to 1:
T       = int(t_max/dt)

# The x- and y-range from 0 to 1 (scaled, original was from 0 to L):
x = np.linspace(0, 1, N+2)
y = np.linspace(0, 1, N+2)

u = np.zeros((N+2, N+2))
x_p = 0
y_p = 0
for x_ in x:
    for y_ in y:
        u[y_p, x_p] = np.sin(np.pi*x_)*np.sin(np.pi*y_) #t = 0
        y_p += 1
    y_p = 0
    x_p += 1
print(u[:,-1])
u[:, 0] = 0.0
u[:,-1] = 0.0
u[0,:] = 0.0
u[-1,:] = 0.0
#u[:, -1] = u[:, 0] = 1.0
#u[-1, :] = 1.0
#implementere t = 0

v = JacobiImplicit(alpha, u, N, T)

X,Y =np.meshgrid(x,y)
plt.contour(Y, X, v)
plt.title('Numerical soluion of 2D diffusion equation')
plt.xlabel('x')
plt.ylabel('y')

analytic2D(x, y, N)
plt.show()
