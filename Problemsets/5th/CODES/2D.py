import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')
import numba

@numba.njit(cache = True)
def JacobiImplicit(alpha, u, N, T):
    """
    This function calculates the evolution of u(x, y) over time using the
    iterative Jacobi method.
    Input:
        -alpha = dt/dx^2
        -u = u(x, y) at t=0
        -N = Number of spatial steps
    	-T = Number of time steps
    The function is compiled by numbas 'just-in-time' compiler to gain CPU-time.
    """
    uTmp = np.zeros_like(u)
    uPrev = np.zeros_like(u)
    # Setting u at previous time step as uPrev
    uPrev = np.copy(u)
    # Creating a guess for the inner matrix of the present timestep
    uTmp = np.copy(uPrev)
    # Limit for the difference between time steps, when the difference reaches
    # this limit the iterations are stopped. diff = max(abs(u-uTmp))
    epsilon = 10e-13
    # Max number of iterations before iterations are stopped
    max_iter = N**3
    # Looping over all time steps solveing linear system by Jacobi iteration at time level t+1
    for t in range(0, T+1):
        # Counter
        r = 0
        # Initializing difference to be > epsilon
        diff=1.0
        while(diff > epsilon and r < max_iter):
            # Looping over all x, y points calculating next step u
            for x in range(1, N+1):
                for y in range(1, N+1):
                    u[y, x] = (1.0/(1.0+4.0*alpha))*(uPrev[y, x] + \
                    alpha*(uTmp[y, x+1] + uTmp[y, x-1] + uTmp[y+1, x] + \
                    uTmp[y-1, x]))
            # Resetting variables for while loop
            r += 1
            diff = np.abs(u-uTmp).max()
            uTmp = np.copy(uPrev)
            uPrev = np.copy(u)
            # Print statement to have a look at number of iterarions and difference
            print('T=', T, 't=', t, 'r=', r, 'diff=', diff)
    return u

def analytic2D(x, y, N, t_list):
    """
    This function calculates the analytic solution of the 2D diffusion equation
    and plots a contour plot for each t-max in the t_list
    """
    for t in t_list:
        plt.figure()
        X,Y = np.meshgrid(x,y)
        u_a = np.sin(np.pi*X)*np.sin(np.pi*Y)*np.exp(-2*np.pi**2*t)
        plt.contour(X, Y, u_a, cmap='viridis')
        plt.gca().invert_yaxis()
        plt.xlabel('x')
        plt.ylabel('u(x, y, t)')
        plt.title('Analytical soluion of 2D diffusion equation, t_max=%f'%t)

#======================= Initial values =====================================
N       = 100
dx      = 1.0/N
dt      = 0.5*(dx**2)
alpha   = dt/(dx**2)
# The time-values we want to plot. Minimum time is 0, maximum is 1:
t_list  = [0.01, 0.5, 1.0]
# The x- and y-range from 0 to 1 (scaled, original was from 0 to L):
x = np.linspace(0, 1, N+2)
y = np.linspace(0, 1, N+2)

u = np.zeros((N+2, N+2))
x_p = 0
y_p = 0
# Creating the input matrix with boundary and initial conditions
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

# Looping over all elements in t_list, calling the JacobiImplicit function
# and creating a contour plot for each element.
for t_max in t_list:
    T = int(round(t_max/dt))
    v = JacobiImplicit(alpha, u, N, T)
    plt.figure()
    X,Y =np.meshgrid(x,y)
    plt.contour(X, Y, v, cmap='viridis')
    plt.gca().invert_yaxis()
    plt.title('Numerical soluion of 2D diffusion equation, t_max = %f'%t_max)
    plt.xlabel('x')
    plt.ylabel('y')
    
# Calling the analytic function with the same t_list and spacing
analytic2D(x, y, N, t_list)

plt.show()
