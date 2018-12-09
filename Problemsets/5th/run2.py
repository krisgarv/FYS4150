
import numpy as np
import matplotlib.pyplot as plt
import solver as s
#===========Initial variables for CrankNicolson===============================

# Endret slik at det passer med deltax osv:
N = 99
T = 60000

# Kun dersom den skulle bli noe annet enn 0.5 senere i oppg.:
deltax = 1.0/(N+1)
deltat = 0.5*(deltax)**2
alpha = deltat/((deltax)**2)
print("Alpha:", alpha, "\n")

x = np.linspace(0, 1, N+1)
print("x:\n", x[1:-1], "\n\n")

u = np.zeros((T+1, N+1))
vi = np.zeros((T+1, N+1))

# Boundary conditions:
# w(t, 0) = w(t, 1) = 0  for t>=0
# u(t, 0) = 0, u(t, 1) = 1   for t>=0
# Initial conditions:
# u(0, x) = 0  for 0<x<1
# Since w(t, x) = u(t, x) - x: w(0, x) = -x   for 0<x<1

u[:, -1] = 1.0
for t in range(0, T+1):
    vi[t, :] = u[t, :] - x

print("To check the initial-/boundary conditions:\n")
print("u(t=0):\n", u[0, :], "\n")
print("w(t=0):\n", vi[0, :], "\n")
print("u(x=0):\n", u[:, 0], "\n")
print("w(x=0):\n", vi[:, 0], "\n")
print("u(x=1):\n", u[:, -1], "\n")
print("w(x=1):\n", vi[:, -1], "\n\n")

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
