import numpy as np


class solver():
    """
    This is a method for solving the differential equation, Newtons law of
    gravitation by numerical integration. Two numerical integration methods are
    included, the forward Euler method and the velocity Verlet method.
    The method returns a matrix containing positions of all objects over time as
    well as arrays containing the development of potential and kinetic energy
    and angular momentum as functions of time.
    """
    def __init__(self, input_matrix, method, time_max, numsteps, perihelion=False):
        """
        The method takes an input matrix where the initial mass, position and
        velocity of each object in a system is stored as the row vectors of the
        2 dimensional matrix. In addition, the number of integration steps,
        whether to solve Newtons law of gravitation by Eulers or the velocity
        Verlet method, and the number of periods to be returned, are also taken
        as input variables.
        """
        self.method = method
        # Total number of integration steps
        self.numsteps = numsteps*time_max
        # Extracting the number of objects from the dimension of the input matrix
        self.numbodies = len(input_matrix[:, 0])
        # Size of each integration step
        self.h = 1.0/numsteps
        # Mass extracted from the input matrix
        self.mass = input_matrix[:, 0]
        # Initial positions and velocities extracted from the input matrix
        self.prev_position = input_matrix[:, 1:4]
        self.prev_velocity = input_matrix[:, 4:7]
        self.perihelion = perihelion

    def main(self):
        """
        This functions combine all the functionalities of this method, loops
        over all the time steps and creates the output of the method.
        """
        # Creating an empty 3D matrix for the output positions
        out_position = np.empty((self.numbodies, 3, self.numsteps+1))
        # Initial position
        position = self.prev_position
        # Initial velocity
        velocity = self.prev_velocity
        # Appending initial position to output matrix
        out_position[:,:,0] = position
        # Calculating initial relative position
        relposition = self.relative_position(position)
        # If the program is user to evaluate the specific problem with
        # mercurys perihelion, the acceleration is altered
        if self.perihelion == True:
            # Calculating initial acceleration a_0
            prev_ac = self.ac_mercury(relposition, velocity)
        else:
            # Calculating initial acceleration a_0
            prev_ac = self.acceleration(relposition)
        # Empty array for kinetic and potential energy and angular momentum
        KE = np.empty(self.numsteps+1)
        PE = np.empty(self.numsteps+1)
        AM = np.empty(self.numsteps+1)
        # Initializing the first step
        KE[0] = self.kinetic_energy(velocity)
        PE[0] = self.potential_energy(relposition)
        AM[0] = self.angular_momentum(relposition, velocity)
        # Looping over all time steps, calculating position, energies and
        # momentum
        for i in range(1, self.numsteps+1):
            # Updating position
            position = self.calc_position(position, velocity, prev_ac)
            # Updating relative position
            relposition = self.relative_position(position)
            # If the program is user to evaluate the specific problem with
            # mercurys perihelion, the acceleration is altered
            if self.perihelion == True:
                # Calculating next acceleration step
                ac = self.ac_mercury(relposition, velocity)
            else:
                # Calculating next acceleration step
                ac = self.acceleration(relposition)
            # Updating velocity
            velocity = self.calc_velocities(velocity, ac, prev_ac)
            # Storing current acceleration step as previous for next velocity
            # calculation
            prev_ac = ac
            # Storing position to output matrix
            out_position[:, :, i] = position
            # Calculating kinetic energy, potential energy and angular momentum
            KE[i] = self.kinetic_energy(velocity)
            PE[i] = self.potential_energy(relposition)
            AM[i] = self.angular_momentum(relposition, velocity)
            # Repeating over all time steps
        # Retuning a 3D output matrix and three arrays
        return out_position, KE, PE, AM

    def relative_position(self, position):
        """
        This function calculate the distance between all the bodies.
        The input is a matrix consisting of the x, y, z position of all of the
        bodies.
        The output is a 3D matrix.
        """
        # Empty matrix for relative positions
        relposition = np.zeros((self.numbodies, self.numbodies, 4))
        # Looping over all objects, calculating the relative position
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                # Skipping the relative position between an object and itself
                if(i != j):
                    relposition[j,i,0] = position[i,0] - position[j,0] # x-direction
                    relposition[j,i,1] = position[i,1] - position[j,1] # y-direction
                    relposition[j,i,2] = position[i,2] - position[j,2] # z-direction
                    relposition[j,i,3] = np.sqrt(relposition[j,i,0]**2 + relposition[j,i,1]**2 + relposition[j,i,2]**2) #The absolute difference
        return relposition

    def acceleration(self, relposition):
        """
        This function calculate the acceleration between all the bodies.
        The input is a matrix consisting of the relative positions and the
        masses of the bodies.
        The output of this function is a 2D matrix.
        """
        # Initializing to avoid repetative FLOPS
        fourpi2 = 4*np.pi**2
        # Empty matrix for the acceleration
        ac = np.zeros((self.numbodies,3))
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    rrr = relposition[j,i,3]**3
                    ac[i,0] = ac[i,0] - (fourpi2*self.mass[j]*relposition[j,i,0])/rrr
                    ac[i,1] = ac[i,1] - (fourpi2*self.mass[j]*relposition[j,i,1])/rrr
                    ac[i,2] = ac[i,2] - (fourpi2*self.mass[j]*relposition[j,i,2])/rrr
                    # Modifying the acceleration to evaluate the escape velocity
                    # problem 3.d): made plots for beta= 2, 2.6 and 3
                    # Run through the solar_system method plotting the Sun and Earth
                    """
                    beta=3
                    rbeta = relposition[j, i, 3]**(beta+1)
                    ac[i,0] = ac[i,0] - (fourpi2*self.mass[j]*relposition[j,i,0])/rbeta
                    ac[i,1] = ac[i,1] - (fourpi2*self.mass[j]*relposition[j,i,1])/rbeta
                    ac[i,2] = ac[i,2] - (fourpi2*self.mass[j]*relposition[j,i,2])/rbeta
                    """
        return ac

    def ac_mercury(self, relposition, velocity):
        """
        Modifying the acceleration to evaluate the perihelion of Mercury
        problem 3.g):
        Run through the script perihelion.py
        """
        # Initializing to avoid repetative FLOPS
        fourpi2 = 4*np.pi**2
        # The magnitude of Mercury's orbital angular momentum
        l = abs(relposition[0,1,3])*(np.sqrt(velocity[1,0]**2 + velocity[1,1]**2 + velocity[1,2]**2))
        # The speed of light in vacuum
        #(299792458 × 60 × 60 × 24 / 149597870700) AU/day
        c = 299792458*60*60*24*365/149597870700 # [AU/yr]
        # Empty matrix for the acceleration
        ac = np.zeros((self.numbodies,3))
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    rr = relposition[j,i,3]**2
                    # Correction
                    corr_x = 1+3*l**2/(relposition[j, i, 3]**2*c**2)
                    corr_y = 1+3*l**2/(relposition[j, i, 3]**2*c**2)
                    corr_z = 1+3*l**2/(relposition[j, i, 3]**2*c**2)
                    ac[i,0] = ac[i,0] - (fourpi2*self.mass[j]*relposition[j,i,0]*corr_x)/rr
                    ac[i,1] = ac[i,1] - (fourpi2*self.mass[j]*relposition[j,i,1]*corr_y)/rr
                    ac[i,2] = ac[i,2] - (fourpi2*self.mass[j]*relposition[j,i,2])*corr_z/rr
        return ac


    def calc_position(self, prev_position, prev_velocity, prev_ac):
        """
        This function calculate the position for the next timestep.
        The input is a 2D position matrix, a 2D velocity matrix and
        2D acceleration matrix.
        The output is a 2D position matrix.
        """
        h = self.h
        h205 = self.h**2/2.0
        position = np.zeros((self.numbodies, 3))
        if self.method == 'euler':
            for i in range(self.numbodies):
                position[i,0] = prev_position[i,0] + h*prev_velocity[i,0]
                position[i,1] = prev_position[i,1] + h*prev_velocity[i,1]
                position[i,2] = prev_position[i,2] + h*prev_velocity[i,2]
            return position
        elif self.method == 'verlet':
            for i in range(self.numbodies):
                position[i,0] = prev_position[i,0] + h*prev_velocity[i,0] + h205*prev_ac[i,0]
                position[i,1] = prev_position[i,1] + h*prev_velocity[i,1] + h205*prev_ac[i,1]
                position[i,2] = prev_position[i,2] + h*prev_velocity[i,2] + h205*prev_ac[i,2]
            return position
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')

    def calc_velocities(self, prev_velocity, ac, prev_ac):
        """
        This function calculates the velocity for the next time step.
        The input is a 2D velocity matrix, a 2D acceleration matrix and a
        2D updated acceleration matrix.
        The output is a 2D velocity matrix.
        """
        h = self.h
        h05 = self.h/2.0
        velocity = np.zeros((self.numbodies, 3))
        if self.method == 'euler':
            for i in range(self.numbodies):
                velocity[i,0] = prev_velocity[i,0] + h*prev_ac[i,0]
                velocity[i,1] = prev_velocity[i,1] + h*prev_ac[i,1]
                velocity[i,2] = prev_velocity[i,2] + h*prev_ac[i,2]
            return velocity

        elif self.method == 'verlet':
            for i in range(self.numbodies):
                velocity[i,0] = prev_velocity[i,0] + h05*(prev_ac[i,0] + ac[i,0])
                velocity[i,1] = prev_velocity[i,1] + h05*(prev_ac[i,1] + ac[i,1])
                velocity[i,2] = prev_velocity[i,2] + h05*(prev_ac[i,2] + ac[i,2])
            return velocity
        else:
            print('Please state which method you want to use; Euler or Verlet(rocommended)')

    def kinetic_energy(self, velocity):
        """
        This function calculates the kinetic energy.
        The input is a vector containing the masses of the bodies,
        a vector of kinetic energy and a 2D velocity matrix.
        The output is a kinetic energy vector.
        """
        kinetic = np.empty(self.numbodies)
        total_ke = 0
        for i in range(self.numbodies):
            kinetic[i] = 0.5*self.mass[i]*(velocity[i,0]**2 + velocity[i,1]**2 + velocity[i,2]**2)
            total_ke += kinetic[i]
        return total_ke

    def potential_energy(self, relposition):
        """
        This function calculate the potential energy.
        The input is a 3D relative position matrix.
        The output is a potential enegy array
        """
        potential = np.empty(self.numbodies)
        total_pe = 0
        for i in range(self.numbodies):
            for j in range(self.numbodies):
                if (i != j):
                    potential[i] = potential[i] - ((4*np.pi**2*self.mass[i]*self.mass[j])/relposition[j,i,3])
            total_pe += potential[i]
        return total_pe

    def angular_momentum(self, relposition, velocity):
        """
        This function calculates the angular momentum.
        The input is a 3D relative position matrix and a 2D velocity matrix.
        The output is a angular momentum vector.
        """
        angular = np.empty(self.numbodies)
        total_ang = 0
        for i in range(self.numbodies):
            angular[i] = self.mass[i]*relposition[0,i,3]*(np.sqrt(velocity[i,0]**2 + velocity[i,1]**2 + velocity[i,2]**2))
            total_ang += angular[i]
        return total_ang
