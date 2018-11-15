import numpy as np
import ising_model as I
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')


#titles = ['Random input configuration', 'Ordered input configuration']
MC_cycles = 1000000
num_spins = 20
Temp = [1.0, 2.4]
ordered=False


def plot_MC_cycles(Temp):
    labels=['Ordered', 'Random']
    titles = ['Temperature: 1.0', 'Temperature: 2.4']
    steps = np.linspace(1, MC_cycles, MC_cycles, endpoint=True)
    for i, T in enumerate(Temp):
        spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        Energy_R, MagnetizationAbs_R, magnet_avg, C_v, X, accepted_list= I.MC(spin_matrix, MC_cycles, T)
        spin_matrix = np.ones((num_spins,num_spins), np.int8)
        Energy_O, MagnetizationAbs_O, magnet_avg, C_v, X, accepted_list= I.MC(spin_matrix, MC_cycles, T)

        #print('Run time: {}'.format(t1-t0))
        fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True) # plot the calculated values
        plt.suptitle('{}'.format(titles[i]))
        ax[0].plot(steps, Energy_O, color='C0', label='Ordered')
        ax[0].plot(steps, Energy_R, color='C1', label='Random')
        ax[0].set_ylabel("Energy", fontsize=20)
        #ax[0].legend()

        ax[1].plot(steps, MagnetizationAbs_O, color='C0', label='Ordered')
        ax[1].plot(steps, MagnetizationAbs_R, color='C1', label='Random')
        ax[1].set_ylabel("Magnetization ", fontsize=20)
        ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
        ax[1].legend()
        #ax[0].title(titles[i])
        #plt.savefig('MCT24C2-5.png')

    plt.show()

plot_MC_cycles(Temp)
