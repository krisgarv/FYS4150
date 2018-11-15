import numpy as np
import ising_model as I
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')


#titles = ['Random input configuration', 'Ordered input configuration']
MC_cycles = 100000
num_spins = 20
Temp = [1.0, 2.4]
ordered=False

def plot_MC_cycles(ordered):
    titles = ['Random input configuration', 'Ordered input configuration']
    steps = np.linspace(1, MC_cycles, MC_cycles, endpoint=True)
    for i in range(2):
        # Initializing the confiuration of the input spin matrix
        if ordered == False:
            #random configuration
            spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        else:
            #ground state
            spin_matrix = np.ones((num_spins,num_spins), np.int8)

        exp_values_T1= I.MC(spin_matrix, MC_cycles, Temp[0])

        energy_avg_T1 = np.cumsum(exp_values_T1[:,0])/np.arange(1, MC_cycles+1)
        magnet_abs_avg_T1 = np.cumsum(exp_values_T1[:, 4])/np.arange(1, MC_cycles+1)
        Energy_T1 = energy_avg_T1/num_spins**2
        MagnetizationAbs_T1 = magnet_abs_avg_T1/num_spins**2

        exp_values_T24 = I.MC(spin_matrix, MC_cycles, Temp[1])

        energy_avg_T24 = np.cumsum(exp_values_T24[:,0])/np.arange(1, MC_cycles+1)
        magnet_abs_avg_T24 = np.cumsum(exp_values_T24[:, 4])/np.arange(1, MC_cycles+1)
        Energy_T24 = energy_avg_T24/num_spins**2
        MagnetizationAbs_T24 = magnet_abs_avg_T24/num_spins**2

        ordered=True

        fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True); # plot the calculated values
        plt.suptitle('{}'.format(titles[i]))

        ax[0].plot(steps, Energy_T1, color='C0', label='T = 1.0')
        ax[0].plot(steps, Energy_T24, color='C1', label='T = 2.4')
        ax[0].set_ylabel("Energy", fontsize=20);
        ax[0].legend(loc='best')

        ax[1].plot(steps, MagnetizationAbs_T1, color='C0', label='T = 1.0')
        ax[1].plot(steps, MagnetizationAbs_T24, color='C1', label='T = 2.4')
        ax[1].set_ylabel("Magnetization ", fontsize=20)

        ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
        ax[1].legend(loc='best')
    plt.show()

plot_MC_cycles(ordered)
