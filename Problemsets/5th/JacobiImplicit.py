import numpy as np
import matplotlib.pyplot as plt
import solver as s
import numba

@numba.njit(cache = True)
def JacobiImplicit(alpha, u, N, T):
    uTmp = np.zeros_like(u) #u_n
    uPrev = np.zeros_like(u)
    uPrev = np.copy(u)
    uTmp = np.copy(uPrev)
    tol = 10e-7
    max_iter = N**3
    for n in range(0, T+1):
        # Solve linear system by Jacobi iteration at time level n+1
        converged = False
        r = 0
        while not converged:
            # Interior:
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[y, x] = (1.0/(1.0+4.0*alpha))*(uPrev[y, x] + \
                    alpha*(uTmp[y, x+1] + uTmp[y, x-1] + uTmp[y+1, x] + \
                    uTmp[y-1, x]))
            r += 1
            converged = np.abs(u-uTmp).max() < tol or r >= max_iter
            uTmp = np.copy(uPrev)
            uPrev = np.copy(u)
    return u

"""
@numba.njit(cache = True)
def JacobiImplicit(alpha, u, N, T):
    tol = 10e-7
    diff = tol + 1
    iter = 0
    maxiter = N**3
    uPrev = np.zeros((N+2, N+2))
    uTmp = np.zeros_like(uPrev)
    uPrev = np.copy(u)
    uTmp = np.copy(uPrev)
    for t in range(1, T+1):
        while (diff >= tol and iter < maxiter):
            diff = 0.0
            #for t in range(1, T+1):
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[y, x] = (1.0/(1.0+4.0*alpha))*(uPrev[y, x] + \
                    alpha*(uTmp[y, x+1] + uTmp[y, x-1] + uTmp[y+1, x] + \
                    uTmp[y-1, x]))

            iter += 1
            diff = np.max(np.abs(u - uTmp))
            uTmp = np.copy(uPrev)
            uPrev = np.copy(u)
    return u
"""

def analytic2D(x, y, N):
    for t in t_list:
        plt.figure()
        X,Y = np.meshgrid(x,y)
        u_a = np.sin(np.pi*X)*np.sin(np.pi*Y)*np.exp(-2*np.pi**2*t)
        #print("ANALYTIC:", u_a)
        #for k in range(1, N):
            #for l in range(1, N):
                #u += np.sin(k*np.pi*X)*np.sin(l*np.pi*Y)*np.exp(np.pi**2*(l**2+k**2)*t)
        #plt.plot(u, x, 'C{}'.format(i), label='t={}'.format(t))
        plt.contour(X, Y, u_a)
        plt.gca().invert_yaxis()
        plt.xlabel('x')
        plt.ylabel('u(x, y, t)')
        #plt.legend()
        plt.title('Analytical soluion of 2D diffusion equation, t_max=%f'%t)


N       = 100
dx      = 1.0/N
dt      = 0.5*(dx**2)
alpha   = dt/(dx**2)

# The time-values we want to plot. Minimum time is 0, maximum is 1:
t_list  = [0.01, 0.5, 1.0]

# Number of time steps from 0 to 1:


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

u[:, 0] = 0.0
u[:, -1] = 0.0
u[0, :] = 0.0
u[-1, :] = 0.0
#print("u-start", u)


for t_max in t_list:
    T = int(round(t_max/dt))
    print(T)
    v = JacobiImplicit(alpha, u, N, T)
    plt.figure()
    X,Y =np.meshgrid(x,y)
    plt.contour(X, Y, v)
    plt.gca().invert_yaxis()
    plt.title('Numerical soluion of 2D diffusion equation, t_max = %f'%t_max)
    plt.xlabel('x')
    plt.ylabel('y')

analytic2D(x, y, N)
plt.show()
