import numpy as np
import ising_model as I
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')


def Accepted(ordered):
    titles = ['Random input configuration', 'Ordered input configuration']
    fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True)
    Steps=np.linspace(0, MC_cycles, MC_cycles, endpoint=True)
    for i in range(2):
        # Initializing the confiuration of the input spin matrix
        if ordered == False:
            #random configuration
            spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        else:
            #ground state
            spin_matrix = np.ones((num_spins,num_spins), np.int8)

        Energy, MagnetizationAbs, magnet_avg, C_v, X, accepted_list_T1= I.MC(spin_matrix, MC_cycles, Temp[0])
        Energy, MagnetizationAbs, magnet_avg, C_v, X, accepted_list_T24 = I.MC(spin_matrix, MC_cycles, Temp[1])

        ordered=True
        #plt.suptitle('{}'.format(titles[i]))
        ax[i].set_title('{}'.format(titles[i]))
        ax[i].plot(Steps, accepted_list_T1, color='C2', label='T = 1.0')
        ax[i].plot(Steps, accepted_list_T24, color='C4', label='T = 2.4')
        ax[i].legend(loc='best')
    ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
    fig.text(0.04, 0.5, 'Number of accepted configurations', va='center', rotation='vertical')


MC_cycles = 100000
num_spins = 20
Temp = [1.0, 2.4]
ordered=False
Accepted(ordered)
plt.show()
