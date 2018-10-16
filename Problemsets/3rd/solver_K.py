import numpy as np

class solver():
    def __init__(self, input_matrix, method, time_max, numsteps):
        self.method = method
        self.numsteps = numsteps
        self.numbodies = len(input_matrix[:, 0])
        self.h = time_max/numsteps
        self.mass = input_matrix[:, 0]
        self.in_position = input_matrix[:, 1:4]
        self.in_velocity = input_matrix[:, 4:7]

    def main(self):
        # Creating an empty 3D matrix for the output positions
        out_position = np.empty((self.numbodies, 3, self.numsteps))
        # Initial position
        position = self.in_position
        # Initial velocity
        velocity = self.in_velocity
        # Appending initial position to output matrix
        out_position[:,:,0] = position
            #out_velocity = np.empty_like((out_position))
            #out_velocity[:,:,0] = self.in_velocity
        # Calculating initial relative position
        relposition = self.relative_position(position)
            #prev_force = np.empty((numbodies, 3, self.numsteps))
        # Calculating initial acceleration a_0
        prev_force = self.forces(relposition)
        # Looping over all time steps, calculating position
        for i in range(1, self.numsteps):
            # Updating position
            position = self.calc_position(position, velocity, prev_force)
            # Updating relative position
            relposition = self.relative_position(position)
            # Calculating next acceleration step
            force = self.forces(relposition)
            # Updating velocity
            velocity = self.calc_velocities(velocity, force, prev_force)
            # Storing current acceleration step as previous for next velocity
            # calculation
            prev_force = force
            # Storing position to output matrix
            out_position[:, :, i] = position
                #out_velocity(:, :, i) = velocity
            # Repeating over all time steps
        # Retuning 3D output matrix
        return out_position

    def relative_position(self, position):
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

    def forces(self, relposition):
        """
        This function calculate the force between all the bodies.
        The input is the number of bodies included, a matrix consisting of the relative positions and the masses of the bodies.
        The output of this function is a 2D matrix.
        """

        fourpi2 = 4*np.pi**2
        relforce = np.zeros((self.numbodies,3))
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    rrr = relposition[j,i,3]**3
                    relforce[i,0] = relforce[i,0] - (fourpi2*self.mass[j]*relposition[j,i,0])/rrr
                    relforce[i,1] = relforce[i,1] - (fourpi2*self.mass[j]*relposition[j,i,1])/rrr
                    relforce[i,2] = relforce[i,2] - (fourpi2*self.mass[j]*relposition[j,i,2])/rrr
        return relforce

    def calc_position(self, position, velocity, relforce):
        """
        This function calculate the position for the next timestep.
        The input is the number of included bodies, a 2D position matrix, a 2D velocity matrix,
        2D relative force matrix, the value of tmax and the number of steps.
        The output is a 2D position matrix.
        """
        h = self.h
        h205 = self.h**2/2.0

        if self.method == 'euler':
            for i in range(self.numbodies):
                position[i,0] = position[i,0] + h*velocity[i,0]
                position[i,1] = position[i,1] + h*velocity[i,1]
                position[i,2] = position[i,2] + h*velocity[i,2]

        elif self.method == 'verlet':
            for i in range(self.numbodies):
                position[i,0] = position[i,0] + h*velocity[i,0] - h205*relforce[i,0]
                position[i,1] = position[i,1] + h*velocity[i,1] - h205*relforce[i,1]
                position[i,2] = position[i,2] + h*velocity[i,2] - h205*relforce[i,2]
            return position
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')


    def calc_velocities(self, velocity, relforce, prev_force):
        """
        This function calculates the velocity.
        The input is the number of included bodies, a 2D velocity matrix, a 2D relative force matrix,
        2D updated force matrix, the value of tmax and the number of steps.
        The output is a 2D velocity matrix.
        """
        h = self.h
        h05 = self.h/2.0

        if self.method == 'euler':
            for i in range(self.numbodies):
                velocity[i,0] = velocity[i,0] + h*relforce[i,0]
                velocity[i,1] = velocity[i,1] + h*relforce[i,1]
                velocity[i,2] = velocity[i,2] + h*relforce[i,2]
            return velocity

        elif self.method == 'verlet':
            for i in range(self.numbodies):
                velocity[i,0] = velocity[i,0] - h05*(prev_force[i,0] - relforce[i,0])
                velocity[i,1] = velocity[i,1] - h05*(prev_force[i,1] - relforce[i,1])
                velocity[i,2] = velocity[i,2] - h05*(prev_force[i,2] - relforce[i,2])
            return velocity
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')
"""
    def kinetic_energy(self, numbodies, mass, velocity):

#        This function calculates the kinetic energy.
#        The input is the number of included bodies, a vector containing the masses of the bodies,
#        a vector of kinetic energy and a 2D velocity matrix.
#        The output is a kinetic energy vector.

        kinetic=[]
        totalke = 0
        for i in range(self.numbodies):
            kinetic[i] = 0.5*self.mass[i]*(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2)
            total_ke += kinetic[i]
        kinetic.append(total_ke)
        return kinetic

    def potential_energy(self, numbodies, mass, relposition):

#        This function calculate the potential energy.
#        The input is the number of included bodies, a positional vector, a mass vector,
#        and a 3D relative positional matrix.

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

#        This function calculates the angular momentum.
#        The input is the number of included bodies, a mass vector, a 3D relative position matrix,
#        and a 2D velocity matrix.
#        The output is a angular momentum vector.

        angular=[]
        total_ang = 0
        for i in range(self.numbodies):
            angular[i] = self.mass[i]*relposition[1,i,4]*(np.squrt(velocity[i,1]**2 + velocity[i,2]**2 + velocity[i,3]**2))
            total_ang += angular[i]
        angular.append(total_ang)
        return angular
"""
