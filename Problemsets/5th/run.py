import numpy as np
import matplotlib.pyplot as plt
import solver as s
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
#sns.set_context('talk')

#===================Initializing input===============================
N       = 100
dx      = 1.0/N
dt      = 0.5*(dx**2)
alpha   = dt/(dx**2)

# The time-values we want to plot. Minimum time is 0, maximum is 1:
t_list  = [0.001, 0.01, 0.03, 0.08, 0.3, 1]
t_max   = 1
# Number of time steps from 0 to 1:
T       = int(t_max/dt)

# The x-range from 0 to 1 (scaled, original was from 0 to L):
x   = np.linspace(0, 1, N+2)

# The u(t,x) and w(t,x):
u   = np.zeros((T, N+2)) #Gammel: u = np.zeros((T+1, N+2))
vi  = np.zeros((T, N+2)) #Gammel: vi = np.zeros((T+1, N+2))

# Setting the initial condition and the boundary condition for u(t,x):
u[:, -1]   = 1.0
u[0, :]    = 0.0

# Setting the initial condition and the boundary condition for w(t,x):
for t in range(T): #Gammel: range(T+1)
    vi[t, :] = u[t, :] - x

vi[:,0] = vi[:,N] = 0.0


#===============Numerical solution================================================================

# Forward Euler:
u_FE        = np.zeros_like(u)
u_FE[:, -1] = 1.0
v_FE        = s.ForwardEuler(alpha, vi, N, T)
for t in range(0, T): #Gammel: T+1
    u_FE[t, 1:-1] = v_FE[t, 1:-1] + x[1:-1]
plt.figure(1)
for t in t_list:
    ind_t = int(t*T)-1
    print(ind_t)
    plt.plot(x, u_FE[ind_t, :], label='t={}'.format(t))
    plt.title('Forward Euler')
    plt.legend()

# Backward Euler:
u_BE        = np.zeros_like(u)
u_BE[:, -1] = 1.0
v_BE        = s.BackwardEuler(alpha, vi, N, T)
for t in range(0, T): #Gammel: T+1
    u_BE[t, 1:-1] = v_BE[t, 1:-1] + x[1:-1]
plt.figure(2)
for t in t_list:
    ind_t = int(t*T)-1
    plt.plot(x, u_BE[ind_t, :], label='t={}'.format(t))
    plt.title('Backward Euler')
    plt.legend()

# Crank Nicolson:
u_CN        = np.zeros_like(u)
u_CN[:, -1] = 1.0
v_CN        = s.CrankNicolson_LU(alpha, vi, N, T)
for t in range(0, T): #Gammel: T+1
    u_CN[t, 1:-1] = v_CN[t, 1:-1] + x[1:-1]
plt.figure(3)
for t in t_list:
    ind_t = int(t*T)-1
    plt.plot(x, u_CN[ind_t, :], label='t={}'.format(t))
    plt.title('Crank Nicolson, LU')
    plt.legend()

"""
for i, t in enumerate(t_list):
    ind_t = int(t*T)-1
    plt.figure(4+i)
    plt.plot(x, u_BE[ind_t, :], 'C0', label='BE, t={}'.format(t))
    plt.plot(x, u_FE[ind_t, :], 'C1', label='FE, t={}'.format(t))
    plt.plot(x, u_CN[ind_t, :], 'C2', label='CN, t={}'.format(t))
    plt.legend(loc='best')
"""

def analytic_1D():
    plt.figure()
    for i, t in enumerate(t_list):
        u = np.zeros_like(x)
        v = np.zeros_like(x)
        for n in range(1, N+1):
            v += (-1)**n*2.0*np.sin(np.pi*n*x)*np.exp(-np.pi**2*n**2*float(t))/(np.pi*n)

        u = v + x
        plt.plot(x, u, 'C{}'.format(i), label='t={}'.format(t))
        plt.xlabel('x')
        plt.ylabel('u(t, x)')
        plt.legend()
        plt.title('Analytical soluion of 1D diffusion equation')
    plt.show()

analytic_1D()
