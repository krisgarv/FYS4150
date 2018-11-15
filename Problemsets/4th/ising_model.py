import numpy as np
import numba


@numba.njit(cache = True)
def initial_energy(spin_matrix, num_spins, temp):
    E = 0
    M = spin_matrix.sum()

    for i in range(num_spins):
        for j in range(num_spins):
            left = spin_matrix[i-1, j] if i>0 else spin_matrix[num_spins - 1, j]
            above = spin_matrix[i, j-1] if j>0 else spin_matrix[i, num_spins - 1]

            E -= spin_matrix[i,j]*(left+above)

    return E, M


@numba.njit(cache=True)
def MC(spin_matrix, num_cycles, temperature):
    num_spins = len(spin_matrix)
    # Matrix for storing calculated expectation and variance values, five variables
    exp_values = np.zeros((int(num_cycles), 6))
    accepted = 0

    E, M = initial_energy(spin_matrix, num_spins, temperature)

    for i in range(1, num_cycles+1):
        for j in range(num_spins*num_spins):
            ix = np.random.randint(num_spins)
            iy = np.random.randint(num_spins)

            left = spin_matrix[ix - 1, iy] if ix > 0 else spin_matrix[num_spins - 1, iy]
            right = spin_matrix[ix + 1, iy] if ix < (num_spins - 1) else spin_matrix[0, iy]

            above = spin_matrix[ix, iy - 1] if iy > 0 else spin_matrix[ix, num_spins - 1]
            below = spin_matrix[ix, iy + 1] if iy < (num_spins - 1) else spin_matrix[ix, 0]

            delta_energy = (2 * spin_matrix[ix, iy] * (left + right + above + below))

            if np.random.random() <= np.exp(-delta_energy / temperature):
                spin_matrix[ix, iy] *= -1.0
                E = E + delta_energy
                M = M + 2*spin_matrix[ix, iy]
                accepted += 1

        exp_values[i-1,0] += E
        exp_values[i-1,1] += M
        exp_values[i-1,2] += E**2
        exp_values[i-1,3] += M**2
        exp_values[i-1,4] += np.abs(M)
        exp_values[i-1,5] += accepted

    return exp_values
    """
    norm = 1/float(num_cycles)

    energy_avg = np.cumsum(exp_values[:,0])/np.arange(1, num_cycles+1)
    magnet_abs_avg = np.cumsum(exp_values[:, 4])/np.arange(1, num_cycles+1)

    #energy_avg = np.sum(exp_values[:,0])*norm
    magnet_avg = np.sum(exp_values[:,1])*norm
    energy2_avg = np.sum(exp_values[:,2])*norm
    magnet2_avg = np.sum(exp_values[:,3])*norm
    #abs_magnet_avg = np.sum(exp_values[:,4])*norm/num_spins**2
    accepted_list = exp_values[:,5]

    energy_var = (energy2_avg - energy_avg[-1]**2)/(num_spins**2)
    magnet_var = (magnet2_avg - magnet_abs_avg[-1]**2)/(num_spins**2)

    energy_avg = energy_avg/num_spins**2
    magnet_abs_avg = magnet_abs_avg/num_spins**2
    magnet_avg = magnet_avg/num_spins**2
    C_v = energy_var/temperature**2
    X = magnet_var/temperature

    return energy_avg, magnet_abs_avg, magnet_avg, C_v, X, accepted_list
    """
