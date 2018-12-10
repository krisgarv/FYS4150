import numpy as np
import matplotlib.pyplot as plt
import solver as s
#===========Initial variables for CrankNicolson===============================
N = 100
T = 50000
alpha = 0.5
# Initial conditions v(0, x) = u(0, x) - x = -x
x = np.linspace(0, 1, N+1)
# Initial matrix for storing v-values
# v[t, x]
u = np.zeros((T+1, N+1))
vi = np.zeros((T+1, N+1))
u[1:, -1] = 1.0
print(u[0, :])
for t in range(T+1):
    vi[t, :] = u[t, :]-x
vi[:,0] = vi[:,N] = 0.0

#===============================================================================
u_FE = np.zeros((T+1, N+1))
v_FE = s.ForwardEuler(alpha, vi, T, N)
for t in range(0, T+1):
    u_FE[t, :] = v_FE[t, :] + x
plt.figure(1)
for t in [0, 1, 10, 100, 200]:
    plt.plot(x, u_FE[t, :], label='t={}'.format(t))
    plt.title('Forward Euler')
    plt.legend()

u_BE = np.zeros((T+1, N+1))
v_BE = s.BackwardEuler(alpha, vi, T, N)
for t in range(0, T+1):
    u_BE[t, :] = v_BE[t, :] + x
plt.figure(2)
for t in [0, 1, 10, 100, 200]:
    plt.plot(x, u_BE[t, :], label='t={}'.format(t))
    plt.title('Backward Euler')
    plt.legend()

u_CN = np.zeros((T+1, N+1))
v_CN = s.CrankNicolson(alpha, vi, T, N)
for t in range(0, T+1):
    u_CN[t, :] = v_CN[t, :] + x
plt.figure(3)
for t in [0, 1, 10, 100, 200]:
    plt.plot(x, u_CN[t, :], label='t={}'.format(t))
    plt.title('Crank Nicolson')
    plt.legend()

plt.figure(4)
for t in [0, 1, 10, 100, 200]:
    plt.plot(x, u_CN[t, :], color='b', label='CrankNicolson')
for t in [0, 1, 10, 100, 200]:
    plt.plot(x, u_BE[t, :], color='r', label='BackwardEuler')
plt.plot()
plt.show()
#[0, 10, 100, 500, 2000, 10000, 50000]
