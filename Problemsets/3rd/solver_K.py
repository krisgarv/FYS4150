import numpy as np

class solver():
    def __init__(self, input_matrix, method, time_max, num_steps):
        self.numbodies = len(input_matrix[:, 0])
        self.h = time_max/num_steps
        self.mass = input_matrix[:, 0]
        self.in_postition = input_matrix[:, 1:4]
        self.in_velocity = input_matrix[:, 4:7]
        #initialize
        # ta fra hverandre input matrise

    def main():
        position = self.in_position
        velocity = self.in_velocity
        out_position = np.empty((self.numbodies, 3, self.num_steps))
        for i in range(num_steps):
            relposition = relative_position(self.numbodies, position)
            relforce = forces(self.numbodies, relposition, self.mass)
            velocity = calc_velocities(self.method, self.numbodies, velocity, relforce, relforce[i-1], self.h)
            position = calc_position(self.method, self.numbodies, position, velocity, relforce)
            updatedforce = relforce
            out_position(:, :, i) = position
        return out_position

    def relative_position(self, numbodies, position):
        """
        This function calculate the distance between all the bodies.
        The input is the number of bodies included and a matrix consisting of the x, y, z position
        of all of the bodies.
        The output is a 3D matrix.
        """
        relposition = np.zeros((self.numbodies, self.numbodies, 4))
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if(i != j):
                    relposition[j,i,0] = position[j,0] - position[i,0] #position x-direction
                    relposition[j,i,1] = position[j,1] - position[i,1] #position y-direction
                    relposition[j,i,2] = position[j,2] - position[i,2] #position z-direction
                    relposition[j,i,3] = np.sqrt(relposition[j,i,0]**2 + relposition[j,i,1]**2 + relposition[j,i,2]**2) #The absolute difference
        return relposition

    def forces(self, numbodies, relposition, mass):
        """
        This function calculate the force between all the bodies.
        The input is the number of bodies included, a matrix consisting of the relative positions and the masses of the bodies.
        The output of this function is a 2D matrix.
        """

        fourpi2 = 4*np.pi**2
        relforce = np.zeros(self.numbodies,3)
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    rrr = relposition[j,i,4]**3
                    relforce[i,1] = relforce[i,1] - (fourpi2*self.mass[j]*relposition[j,i,1])/rrr
                    relforce[i,2] = relforce[i,2] - (fourpi2*self.mass[j]*relposition[j,i,2])/rrr
                    relforce[i,3] = relforce[i,3] - (fourpi2*self.mass[j]*relposition[j,i,3])/rrr
        return relforce

    def calc_position(self, method, numbodies, position, velocity, relforce):
        """
        This function calculate the position for the next timestep.
        The input is the number of included bodies, a 2D position matrix, a 2D velocity matrix,
        2D relative force matrix, the value of tmax and the number of steps.
        The output is a 2D position matrix.
        """
        h = self.h
        h205 = self.h**2/2.0

        if self.method == 'Euler':
            for i in range(self.numbodies):
                position[i,1] = position[i,1] + h*velocity[i,1]
                position[i,2] = position[i,2] + h*velocity[i,2]
                position[i,3] = position[i,3] + h*velocity[i,3]
        elif self.method == 'Verlet':
            for i in range(self.numbodies):
                position[i,1] = position[i,1] + h*velocity[i,1] + h205*relforce[i,1]
                position[i,2] = position[i,2] + h*velocity[i,2] + h205*relforce[i,2]
                position[i,3] = position[i,3] + h*velocity[i,3] + h205*relforce[i,3]
            return position
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')


    def calc_velocities(self, method, numbodies, velocity, relforce, updatedforce, tmax, num_steps):
        """
        This function calculates the velocity.
        The input is the number of included bodies, a 2D velocity matrix, a 2D relative force matrix,
        2D updated force matrix, the value of tmax and the number of steps.
        The output is a 2D velocity matrix.
        """
        velocity[0, :] = self.velocity
        h = self.h
        h05 = self.h/2.0
        if self.method == 'Euler':
            for i in range(self.numbodies):
                velocity[i,1] = velocity[i,1] + h*relforce[i,1]
                velocity[i,2] = velocity[i,2] + h*relforce[i,2]
                velocity[i,3] = velocity[i,3] + h*relforce[i,3]
            return velocity

        elif self.method == 'Verlet':
            for i in range(self.numbodies):
                velocity[i,1] = velocity[i,1] + h05*(updatedforce[i,1] + relforce[i,1])
                velocity[i,2] = velocity[i,2] + h05*(updatedforce[i,2] + relforce[i,2])
                velocity[i,3] = velocity[i,3] + h05*(updatedforce[i,3] + relforce[i,3])
            return velocity
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')
"""
    def kinetic_energy(self, numbodies, mass, velocity):
        """
#        This function calculates the kinetic energy.
#        The input is the number of included bodies, a vector containing the masses of the bodies,
#        a vector of kinetic energy and a 2D velocity matrix.
#        The output is a kinetic energy vector.
        """
        kinetic=[]
        totalke = 0
        for i in range(self.numbodies):
            kinetic[i] = 0.5*self.mass[i]*(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2)
            total_ke += kinetic[i]
        kinetic.append(total_ke)
        return kinetic

    def potential_energy(self, numbodies, mass, relposition):
        """
#        This function calculate the potential energy.
#        The input is the number of included bodies, a positional vector, a mass vector,
#        and a 3D relative positional matrix.
        """
        potentital=[]
        total_pe = 0  #np.zeros(numbodies+1)
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    potential[i] = potential[i] + ((4*np.pi**2*self.mass[i]*self.mass[j])/relposition[j,i,4])
            total_pe += potential[i]
        potential.append(total_pe)
        return potential

    def angular_momentum(self, numbodies, mass, relposition, velocity):
        """
#        This function calculates the angular momentum.
#        The input is the number of included bodies, a mass vector, a 3D relative position matrix,
#        and a 2D velocity matrix.
#        The output is a angular momentum vector.
        """
        angular=[]
        total_ang = 0
        for i in range(self.numbodies):
            angular[i] = self.mass[i]*relposition[1,i,4]*(np.squrt(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2))
            total_ang += angular[i]
        angular.append(total_ang)
        return angular
"""
