import numpy as np
import matplotlib.pyplot as plt
import solver as s

import numpy as np
import matplotlib.pyplot as plt
import solver as s
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')

def Plot(N, t_list):
    #===================Initializing input===============================
    dx      = 1.0/N
    dt      = 0.5*(dx**2)
    alpha   = dt/(dx**2)

    # The time-values we want to plot. Minimum time is 0, maximum is 1:

    t_max   = 1
    # Number of time steps from 0 to 1:
    T       = int(t_max/dt)

    # The x-range from 0 to 1 (scaled, original was from 0 to L):
    x   = np.linspace(0, 1, N+2)

    # The u(t,x) and w(t,x):
    u   = np.zeros((T, N+2)) #Gammel: u = np.zeros((T+1, N+2))
    w  = np.zeros((T, N+2)) #Gammel: w = np.zeros((T+1, N+2))

    # Setting the initial condition and the boundary condition for u(t,x):
    u[:, -1]   = 1.0
    u[0, :]    = 0.0

    # Setting the initial condition and the boundary condition for w(t,x):
    for t in range(T):
        w[t, :] = u[t, :] - x

    w[:,0] = w[:,N] = 0.0
    #===============Numerical solution================================================================
    plt.xlabel('x')
    plt.ylabel('u(t, x)')
    # Forward Euler:
    u_FE        = np.zeros_like(u)
    u_FE[:, -1] = 1.0
    w_FE        = s.ForwardEuler(alpha, w, N, T)
    for t in range(0, T): #Gammel: T+1
        u_FE[t, 1:-1] = w_FE[t, 1:-1] + x[1:-1]
    for t in t_list:
        idx_t = int(t*T)-1
        ax[0, 0].plot(x, u_FE[idx_t, :], label='t={}'.format(t))
    ax[0, 0].set_title('Forward Euler')
    ax[0, 0].legend()

    # Backward Euler:
    u_BE        = np.zeros_like(u)
    u_BE[:, -1] = 1.0
    w_BE        = s.BackwardEuler(alpha, w, N, T)
    for t in range(0, T): #Gammel: T+1
        u_BE[t, 1:-1] = w_BE[t, 1:-1] + x[1:-1]
    for t in t_list:
        idx_t = int(t*T)-1
        ax[0, 1].plot(x, u_BE[idx_t, :], label='t={}'.format(t))
        ax[0, 1].set_title('Backward Euler')
        ax[0, 1].legend()

    # Crank Nicolson:
    u_CN        = np.zeros_like(u)
    u_CN[:, -1] = 1.0
    w_CN        = s.CrankNicolson_LU(alpha, w, N, T)
    for t in range(0, T): #Gammel: T+1
        u_CN[t, 1:-1] = w_CN[t, 1:-1] + x[1:-1]
    for t in t_list:
        idx_t = int(t*T)-1
        ax[1, 0].plot(x, u_CN[idx_t, :], label='t={}'.format(t))
        ax[1, 0].set_title('Crank Nicolson')
        ax[1, 0].legend()

    #======================Analytic Solution========================================
    for i, t in enumerate(t_list):
        u = np.zeros_like(x)
        w = np.zeros_like(x)
        for k in range(1, N+1):
            w += (-1)**k*2.0*np.sin(np.pi*k*x)*np.exp(-np.pi**2*k**2*float(t))/(np.pi*k)
        u = w + x
        ax[1, 1].plot(x, u, 'C{}'.format(i), label='t={}'.format(t))
        ax[1, 1].legend()
        ax[1, 1].set_title('Analytical soluion of 1D diffusion equation')
    plt.figure()
    for t in [0.01, 0.03, 0.3]:
        u = np.zeros_like(x)
        w = np.zeros_like(x)
        for k in range(1, N+1):
            w += (-1)**k*2.0*np.sin(np.pi*k*x)*np.exp(-np.pi**2*k**2*float(t))/(np.pi*k)
        u = w + x
        idx_t = int(t*T)-1
        plt.plot(x, u_BE[idx_t, :], 'C0', label='BE t={}'.format(t))
        plt.plot(x, u_FE[idx_t, :], 'C1', label='FE t={}'.format(t))
        plt.plot(x, u_CN[idx_t, :], 'C2', label='CN t={}'.format(t))
        plt.plot(x, u, 'C3', linestyle='--', label='Analytic t={}'.format(t))
    plt.legend(loc='best', fontsize=12)
    plt.xlabel('x')
    plt.ylabel('u(x, t)')
    
fig, ax = plt.subplots(2, 2, figsize=(16, 16), sharey=True, sharex=True)
N=10
t_list  = [0.01, 0.03, 0.08, 0.3, 1]
Plot(N, t_list)
fig, ax = plt.subplots(2, 2, figsize=(16, 16), sharey=True, sharex=True)
N       = 100
t_list  = [0.001, 0.01, 0.03, 0.08, 0.3, 1]
Plot(N, t_list)
plt.show()
