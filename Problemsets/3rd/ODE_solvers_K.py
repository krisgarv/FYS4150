import numpy as np


class ODE_solver:
    """Two finite difference methods for solving coupled ordinary differential
    equations."""

    def __init__(N, yrs, x0, y0, v_x0, v_y0, a_x, a_y):
        # Euler or Verlet method
        self.method = method
        # Number of integration points
        self.N = N
        # Initial position x-direction
        self.x0 = x0
        # Initial position y-direction
        self.y0 = y0
        # Initial velocity x-direction
        self.v_x0 = v_x0
        # Initial velocity y-direction
        self.v_y0 = v_y0
        # Acceleration in x-direction, function of x and y
        self.a_x = a_x
        # Acceleration in y-direction, function of x and y
        self.h = float(yrs)/N

    def euler_coupled(self):
        """ This function solves a coupled differential equation numerically,
        using the traditional Euler forward method."""
        x=np.empty(self.N+1)
        y=np.empty_like(x)
        vx=np.empty_like(x)
        vy=np.empty_like(x)
        ax=np.empty_like(x)
        ay=np.empty_like(x)

        x[0] = self.x0
        y[0] = self.y0
        vx[0] = self.v_x0
        vy[0] = self.v_y0
        ax[0] = self.a_x(x[0], y[0])
        ay[0] = self.a_y(x[0], y[0])

        for n in range(1,self.N+1):
            vx[n] = vx[n-1] + self.h*ax[n-1]
            x[n] = x[n-1] + self.h*vx[n-1]

            vy[n] = vy[n-1] + self.h*ay[n-1]
            y[n] = y[n-1] + self.h*vy[n-1]

            ax[n] = self.a_x(x[n], y[n])
            ay[n] = self.a_y(x[n], y[n])

            return x, y


    def verlet(self):
        """ This function solves a coupled differential equation numerically,
        using the popular velocity Verlet method."""
        x=np.empty(self.N+1)
        y=np.empty_like(x)
        vx=np.empty_like(x)
        vy=np.empty_like(x)
        ax=np.empty_like(x)
        ay=np.empty_like(x)

        x[0] = self.x0
        y[0] = self.y0
        vx[0] = self.v_x0
        vy[0] = self.v_y0
        ax[0] = self.a_x(x[0], y[0])
        ay[0] = self.a_y(x[0], y[0])

        for i in range (1,self.N+1):
            x[i] = x[i-1] + self.h*vx[i-1] + (self.h**2*0.5*ax[i-1])
            y[i] = y[i-1] + self.h*vy[i-1] + (self.h**2*0.5*ay[i-1])

            ax[i] = self.a_x(x[i], y[i])
            ay[i] = self.a_y(x[i], y[i])

            vx[i] = vx[i-1] + self.h*0.5*(ax[i]+ax[i-1])
            vy[i] = vy[i-1] + self.h*0.5*(ay[i]+ay[i-1])
            return x, y

    def main():
