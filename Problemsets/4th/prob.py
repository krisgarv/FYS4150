import numpy as np
import numba
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')

MC_cycles = [140000, 200000] #T1, T2
num_spins = 20
Temp = [1.0, 2.4]
ordered=True

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
    exp_values = np.zeros(int(num_cycles))
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

        exp_values[i-1] += E
    return exp_values


def plot_MC_cycles(ordered):
    for cycles, T in zip(MC_cycles, Temp):
        # Initializing the confiuration of the input spin matrix
        if ordered == False:
            #random configuration
            spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        else:
            #ground state
            spin_matrix = np.ones((num_spins,num_spins), np.int8)

        t0 = time.time()
        Energy = MC(spin_matrix, cycles, T)
        t1 = time.time()
        if T == 1.0:
            sp = 30
            Energy = Energy[19999:-1]
        else:
            sp = 160
            Energy = Energy[99999:-1]

        Energy = Energy/(num_spins**2)
        n, bins, patches = plt.hist(Energy, sp, facecolor='blue')
        plt.xlabel('$E$')
        plt.ylabel('Energy distribution P(E)')
        plt.title('Energy distribution at  $k_BT=%s$'%str(T))
        plt.grid(True)
        plt.show()

plot_MC_cycles(ordered)
