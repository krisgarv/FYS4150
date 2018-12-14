import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_style('white')
#sns.set_style('ticks')
sns.set_context('talk')

#==========================INITAL VALUES=======================================
N       = 50
dx      = 1.0/N
dt      = 0.5*(dx**2)
alpha   = dt/(dx**2)
# The time-values we want to plot. Minimum time is 0, maximum is 1:
t_list  = [0.01, 0.03, 0.3, 1]
t_max   = 1
# Number of time steps from 0 to 1:
T       = int(t_max/dt)
# The x- and y-range from 0 to 1 (scaled, original was from 0 to L):
x = np.linspace(0, 1, N+2)
y = np.linspace(0, 1, N+2)
X,Y = np.meshgrid(x,y)

u = np.zeros((N+2, N+2))
x_p = 0
y_p = 0
for x_ in x:
    for y_ in y:
        u[y_p, x_p] = np.sin(np.pi*x_)*np.sin(np.pi*y_)
        y_p += 1
    y_p = 0
    x_p += 1
u[:, 0] = u[:,-1] = u[0,:] = u[-1,:] = 0.0

#Initializing subplots
fig, ax = plt.subplots(1, 2, figsize=(16, 8))
#======================NUMERICAL SOLUTION======================================
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
    #for t in range(1, T+1):
    for x in range(1, N+1):
        for y in range(1, N+1):
            u[y, x] = (1.0/(1.0+4.0*alpha))*(uPrev[y, x] + \
            alpha*(uTmp[y, x+1] + uTmp[y, x-1] + uTmp[y+1, x] + \
            uTmp[y-1, x]))
    iter += 1
    diff = np.max(np.abs(u - uTmp))
    uTmp = uPrev
    uPrev = u

ax[0].contour(X, Y, u, cmap='viridis')
ax[0].set_title('Numerical')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
plt.figure()
plt.contour(X, Y, u, cmap='viridis')
#======================ANALYTIC SOLUTION=======================================
u = np.sin(np.pi*X)*np.sin(np.pi*Y)*np.exp(-2*np.pi**2)
ax[1].contour(X, Y, u, cmap='viridis_r')
ax[1].set_title('Analytic')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
plt.contour(X, Y, u, cmap='viridis_r')
plt.xlabel('x')
plt.ylabel('y')
#==============================================================================
plt.show()
