import numpy as np
import ising_model as I
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')


# Initial conditions
MC_cycles = 100000
num_spins = 20
Temp = [1.0, 2.4]
titles = ['Temperature: 1.0', 'Temperature: 2.4']
ordered=False


def plot_MC_cycles(Temp):
    """
    This function creates two plots, each containing subplots of the mean energy
    and absolute magnetization as functions of Monte Carlo cycles, for random and
    ordered initial lattice configurations.
    The two plots show the results of two different input temperatures.
    """
    steps = np.linspace(1, MC_cycles, MC_cycles, endpoint=True)
    for i, T in enumerate(Temp):

        # Random initial confiuration
        spin_matrix_R = np.random.choice((-1, 1), (num_spins, num_spins))

        exp_values_R = I.MC(spin_matrix_R, MC_cycles, T)
        energy_avg_R = np.cumsum(exp_values_R[:,0])/np.arange(1, MC_cycles+1)
        magnet_abs_avg_R = np.cumsum(exp_values_R[:, 4])/np.arange(1, MC_cycles+1)
        Energy_R = energy_avg_R/num_spins**2
        MagnetizationAbs_R = magnet_abs_avg_R/num_spins**2

        # Ordered initial confiuration
        spin_matrix_O = np.ones((num_spins,num_spins), np.int8)

        exp_values_O = I.MC(spin_matrix_O, MC_cycles, T)
        energy_avg_O = np.cumsum(exp_values_O[:,0])/np.arange(1, MC_cycles+1)
        magnet_abs_avg_O = np.cumsum(exp_values_O[:, 4])/np.arange(1, MC_cycles+1)
        Energy_O = energy_avg_O/(num_spins**2)
        MagnetizationAbs_O = magnet_abs_avg_O/(num_spins**2)
        #print('Run time: {}'.format(t1-t0))
        fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True) # plot the calculated values
        plt.suptitle('{}'.format(titles[i]))
        ax[0].plot(steps, Energy_O, color='C0', label='Ordered')
        ax[0].plot(steps, Energy_R, color='C1', label='Random')
        ax[0].set_ylabel("Energy", fontsize=20)
        ax[0].legend(loc='best')

        ax[1].plot(steps, MagnetizationAbs_O, color='C0', label='Ordered')
        ax[1].plot(steps, MagnetizationAbs_R, color='C1', label='Random')
        ax[1].set_ylabel("Magnetization ", fontsize=20)
        ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
        ax[1].legend(loc='best')
        #ax[0].title(titles[i])
        #plt.savefig('MCT24C2-5.png')

    plt.show()

plot_MC_cycles(Temp)
