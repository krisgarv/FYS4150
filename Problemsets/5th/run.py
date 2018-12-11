import numpy as np
import matplotlib.pyplot as plt
import solver as s
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
#sns.set_context('talk')

#===================Initializing input===============================
N = 100
T = 20000
dx=1.0/N
dt=1.0/T
alpha = dt/(dx*dx)
#t_list=[0, 1, 10, 100, 200]
t_list=[0, 10, 1000]
# Initial conditions v(0, x) = u(0, x) - x = -x
x = np.linspace(0, 1, N+2)
# Initial matrix for storing v-values
# v[t, x]
u = np.zeros((T+1, N+2))
vi = np.zeros((T+1, N+2))
u[:, -1] = 1.0
u[0, :] = 0.0
for t in range(T+1):
    vi[t, :] = u[t, :]-x
vi[:,0] = vi[:,N] = 0.0

#===============Analytic solution================================================================
"""
u_FE = np.zeros_like(u)
u_FE[:, -1] = 1.0
v_FE = s.ForwardEuler(alpha, vi, N, T)
for t in range(0, T+1):
    u_FE[t, 1:-1] = v_FE[t, 1:-1] + x[1:-1]
plt.figure(1)
for t in t_list:
    plt.plot(x, u_FE[t, :], label='t={}'.format(t))
    plt.title('Forward Euler')
    plt.legend()

u_BE = np.zeros_like(u)
u_BE[:, -1] = 1.0
v_BE = s.BackwardEuler(alpha, vi, N, T)
for t in range(0, T+1):
    u_BE[t, 1:-1] = v_BE[t, 1:-1] + x[1:-1]
plt.figure(2)
for t in t_list:
    plt.plot(x, u_BE[t, :], label='t={}'.format(t))
    plt.title('Backward Euler')
    plt.legend()

u_CN = np.zeros_like(u)
u_CN[:, -1] = 1.0
v_CN = s.CrankNicolson_LU(alpha, vi, N, T)
for t in range(0, T+1):
    u_CN[t, 1:-1] = v_CN[t, 1:-1] + x[1:-1]
plt.figure(3)
for t in t_list:
    plt.plot(x, u_CN[t, :], label='t={}'.format(t))
    plt.title('Crank Nicolson, LU')
    plt.legend()

for i, t in enumerate(t_list):
    plt.figure(5+i)
    plt.plot(x, u_BE[t, :], 'C0', label='BE, t={}'.format(t))
    plt.plot(x, u_FE[t, :], 'C1', label='FE, t={}'.format(t))
    plt.plot(x, u_CN[t, :], 'C2', label='CN, t={}'.format(t))
    plt.legend(loc='best')
"""
plt.figure()
for i, t in enumerate(t_list):
    u=np.zeros_like(x)
    v=np.zeros_like(x)
    for n in range(N+1):
        v += np.sin(np.pi*n*x)*np.exp(-np.pi*n**2*float(t))/float(np.pi*n)
    u=x+2*v
    plt.plot(u, x, 'C{}'.format(i), label='t={}'.format(t))
    plt.xlabel('x')
    plt.ylabel('u(t, x)')
    plt.legend()
    plt.title('Analytical soluion of 1D diffusion equation')
plt.show()
