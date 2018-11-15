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

def plot_MC_cycles(ordered):
    steps = np.linspace(1, MC_cycles, MC_cycles, endpoint=True)
    for i in range(2):
        # Initializing the confiuration of the input spin matrix
        if ordered == False:
            #random configuration
            spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        else:
            #ground state
            spin_matrix = np.ones((num_spins,num_spins), np.int8)

        t0 = time.time()
        Energy_T1, MagnetizationAbs_T1, magnet_avg, C_v, X, accepted_list= I.MC(spin_matrix, MC_cycles, Temp[0])
        Energy_T24, MagnetizationAbs_T24, magnet_avg, C_v, X, accepted_list = I.MC(spin_matrix, MC_cycles, Temp[1])
        t1 = time.time()
        ordered=True

        print('Run time: {}'.format(t1-t0))
        fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True); # plot the calculated values

        ax[0].plot(steps, Energy_T1, color='C0', label='T = 1.0')
        ax[0].plot(steps, Energy_T24, color='C1', label='T = 2.4')
        ax[0].set_ylabel("Energy", fontsize=20);
        ax[0].legend(loc='upper right')

        ax[1].plot(steps, MagnetizationAbs_T1, color='C0', label='T = 1.0')
        ax[1].plot(steps, MagnetizationAbs_T24, color='C1', label='T = 2.4')
        ax[1].set_ylabel("Magnetization ", fontsize=20)

        ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
        #ax[1].legend(loc='lower right')
        #ax[0].title(titles[i])
        #plt.savefig('MCT24C2-5.png')

    plt.show()

plot_MC_cycles(ordered)
