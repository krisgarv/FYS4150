import numpy as np

class solver():
    def __init__(self):
        #initialize

    def relative_position(self, numbodies, position):
        """
        This function calculate the distance between all the bodies.
        The input is the number of bodies included and a matrix consisting of the x, y, z position
        of all of the bodies.
        The output is a 3D matrix.
        """
        relposition = np.zeros(numbodies, numbodies, 4)
        for i in range(numbodies):
            for j in range(numbodies):
                if(i != j):
                    relposition[j,i,1] = position[j,1] - position[i,1] #position x-direction
                    relposition[j,i,2] = position[j,2] - position[i,2] #position y-direction
                    relposition[j,i,3] = position[j,3] - position[i,3] #position z-direction
                    relposition[j,i,4] = np.sqrt(relposition[j,i,1]**2 + relposition[j,i,2]**2 + relposition[j,i,3]**2) #The absolute difference
        return relposition

    def forces(self, numbodies, realposition, mass):
        """
        This function calculate the force between all the bodies.
        The input is the number of bodies included, a matrix consisting of the relative positions and the masses of the bodies.
        The output of this function is a 2D matrix.
        """

        fourpi2 = 4*np.pi**2
        relforce = np.zeros(numbodies,3)
        for i in range(numbodies):
            for j in range(numbodies):
                if (i != j):
                    rrr = realposition[j,i,4]**3
                    relforce[i,1] = relforce[i,1] - (fourpi2*mass[j]*realposition[j,i,1])/rrr
                    relforce[i,2] = relforce[i,2] - (fourpi2*mass[j]*realposition[j,i,2])/rrr
                    relforce[i,3] = relforce[i,3] - (fourpi2*mass[j]*realposition[j,i,3])/rrr
        return relforce

    def calc_position(self, numbodies, position, velocity, relforce, tmax, num_steps):
        """
        This function calculate the position for the next timestep.
        The input is the number of included bodies, a 2D position matrix, a 2D velocity matrix,
        2D relative force matrix, the value of tmax and the number of steps.
        The output is a 2D position matrix.
        """
        h = tmax/num_steps
        for i in range(numbodies):
            position[i,1] = position[i,1] + h*velocity[i,1] - (h**2/2.0)*relforce[i,1]
            position[i,2] = position[i,2] + h*velocity[i,2] - (h**2/2.0)*relforce[i,2]
            position[i,3] = position[i,3] + h*velocity[i,3] - (h**2/2.0)*relforce[i,3]
        return position

    def calc_velocities(self, numbodies, velocity, relforce, updatedforce, tmax, num_steps):
        """
        This function calculates the velocity.
        The input is the number of included bodies, a 2D velocity matrix, a 2D relative force matrix,
        2D updated force matrix, the value of tmax and the number of steps.
        The output is a 2D velocity matrix.
        """
        h = tmax/num_steps
        for i in range(numbodies):
            velocity[i,1] = velocity[i,1] - h*0.5*updatedforce[i,1] - h*0.5*relforce[i,1]
            velocity[i,2] = velocity[i,2] - h*0.5*updatedforce[i,2] - h*0.5*relforce[i,2]
            velocity[i,3] = velocity[i,3] - h*0.5*updatedforce[i,3] - h*0.5*relforce[i,3]
        return velocity

    def kinetic_energy(self, numbodies, mass, kinetic, velocity):
        """
        This function calculates the kinetic energy.
        The input is the number of included bodies, a vector containing the masses of the bodies,
        a vector of kinetic energy and a 2D velocity matrix.
        The output is a kinetic energy vector.
        """

        totalke = 0
        for i in range(numbodies):
            kinetic[i] = 0.5*mass[i]*(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2)
            totalke += kinetic[i]
        kinetic.append(totalke)
        return kinetic

    def potential_energy(self, numbodies, potential, mass, relposition):
        """
        This function calculate the potential energy.
        The input is the number of included bodies, a positional vector, a mass vector,
        and a 3D relative positional matrix.
        """

        totalpe = np.zeros(numbodies+1)
        for i in range(numbodies):
            for j in range(numbodies):
                if (i != j):
                    potential[i] = potential[i] + ((4*np.pi**2*mass[i]*mass[j])/relposition[j,i,4])
            totalpe += potential[i]
        potential.append(totalpe)
        return potential

    def angular_momentum(self, numbodies, mass, relposition, velocity):
        """
        This function calculates the angular momentum.
        The input is the number of included bodies, a mass vector, a 3D relative position matrix,
        and a 2D velocity matrix.
        The output is a angular momentum vector.
        """

        totalang = 0
        for i in range(numbodies):
            angular[i] = mass[i]*relposition[1,i,4]*(np.squrt(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2))
            totalang += angular[i]
        angular.append(totalang)
        return angular
