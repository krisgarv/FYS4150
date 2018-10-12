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

    def calc_position(self, numbodies, position, velocity, relforce, h):

        for i in range(numbodies):
            position[i,1] = position[i,1] + h*velocity[i,1] - (h**2/2.0)*relforce[i,1]
            position[i,2] = position[i,2] + h*velocity[i,2] - (h**2/2.0)*relforce[i,2]
            position[i,3] = position[i,3] + h*velocity[i,3] - (h**2/2.0)*relforce[i,3]
        return position

    def calc_velocities(self, velocity, relforce, updatedforce, h, numbodies):

        for i in range(numbodies):
            velocity[i,1] = velocity[i,1] - h*0.5*updatedforce[i,1] - h*0.5*relforce[i,1]
            velocity[i,2] = velocity[i,2] - h*0.5*updatedforce[i,2] - h*0.5*relforce[i,2]
            velocity[i,3] = velocity[i,3] - h*0.5*updatedforce[i,3] - h*0.5*relforce[i,3]
        return velocity

    def kinetic_energy(self, numbodies, mass):

        totalke = 0
        for i in range(numbodies):
            kinetic[i] = 0.5*mass[i]*(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2)
            totalke += kinetic[i]
        kinetic.append(totalke)
        return kinetic

        
