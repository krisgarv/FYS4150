import numpy as np
import numba

"""
The functions in this script are being compiled by numba for optimization.
"""

@numba.njit(cache = True)
def initial_energy(spin_matrix, num_spins, temp):
    """
    This function calculates the initial energy and magnetization of the input
    configuration.
    """
    E = 0
    M = spin_matrix.sum()
    # Loop over all spins in the lattice
    for i in range(num_spins):
        for j in range(num_spins):
            # periodic boundary conditions
            left = spin_matrix[i-1, j] if i>0 else spin_matrix[num_spins - 1, j]
            above = spin_matrix[i, j-1] if j>0 else spin_matrix[i, num_spins - 1]

            E -= spin_matrix[i,j]*(left+above)

    return E, M


@numba.njit(cache=True)
def MC(spin_matrix, num_cycles, temperature):
    """
    This function calculates the energy, magnetization and their
    suared of a ising model lattice, the number of accepted configurations
    according to the metropolis algorithm is also tracked.
    Periodic boudary conditions are applied.
    The calculations are repeated according to choice of Monte Carlo cycles.
    The results are stored in a matrix for output.
    """
    num_spins = len(spin_matrix)
    # Matrix for storing calculated expectation and variance values, five variables
    exp_values = np.zeros((int(num_cycles), 6))
    accepted = 0
    # Initial energy and magnetization
    E, M = initial_energy(spin_matrix, num_spins, temperature)
    # Looping over number of Monte Carlo cycles storing values for each step
    for i in range(1, num_cycles+1):
        # Repeat according to size of lattice for each cycle
        for j in range(num_spins*num_spins):
            # Picking a random lattice position
            ix = np.random.randint(num_spins)
            iy = np.random.randint(num_spins)
            # Finding the surrounding spins accordng to periodic boundary conditions
            left = spin_matrix[ix - 1, iy] if ix > 0 else spin_matrix[num_spins - 1, iy]
            right = spin_matrix[ix + 1, iy] if ix < (num_spins - 1) else spin_matrix[0, iy]

            above = spin_matrix[ix, iy - 1] if iy > 0 else spin_matrix[ix, num_spins - 1]
            below = spin_matrix[ix, iy + 1] if iy < (num_spins - 1) else spin_matrix[ix, 0]
            # Calculating the energy change
            delta_energy = (2 * spin_matrix[ix, iy] * (left + right + above + below))
            # Evaluating the proposet new configuration
            if np.random.random() <= np.exp(-delta_energy / temperature):
                # Changing the configuration if accepted
                spin_matrix[ix, iy] *= -1.0
                E += delta_energy
                M += 2*spin_matrix[ix, iy]
                accepted += 1
        # Store values in output matrix
        exp_values[i-1,0] = E
        exp_values[i-1,1] = M
        exp_values[i-1,2] = E**2
        exp_values[i-1,3] = M**2
        exp_values[i-1,4] = np.abs(M)
        exp_values[i-1,5] = accepted

    return exp_values
