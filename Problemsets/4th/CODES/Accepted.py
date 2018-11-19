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
ordered=False

def Accepted(ordered):
    """
    This function plots the number of accepted configurations in the Ising model
    as function of Monte Carlo cycles, calculated by the imported function MC from
    ising_model.py.
    Two subplots are produced, one for steady initial configuration of the lattice
    and one for a random configuration, both containing the accepted values for
    temperature, T=1.0 and T=2.4.
    """
    titles = ['Random input configuration', 'Ordered input configuration']
    fig, ax = plt.subplots(2, 1, figsize=(18, 7), sharex=True)
    Steps = np.linspace(0, MC_cycles, MC_cycles, endpoint=True)
    for i in range(2):
        # Initializing the confiuration of the input spin matrix
        if ordered == False:
            #random configuration
            spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))
        else:
            #ground state
            spin_matrix = np.ones((num_spins,num_spins), np.int8)
        # Extracting the relevant values from the output matrix from the ising_model
        exp_values_T1= I.MC(spin_matrix, MC_cycles, Temp[0])
        exp_values_T24 = I.MC(spin_matrix, MC_cycles, Temp[1])
        accepted_list_T1 = exp_values_T1[:,5]
        accepted_list_T24 = exp_values_T24[:,5]
        ordered=True
        ax[i].set_title('{}'.format(titles[i]))
        ax[i].loglog(Steps, accepted_list_T1, color='C2', label='T = 1.0')
        ax[i].loglog(Steps, accepted_list_T24, color='C4', label='T = 2.4')
        ax[i].legend(loc='best')
    ax[1].set_xlabel("Monte Carlo cycles", fontsize=20)
    fig.text(0.04, 0.5, 'Number of accepted configurations', va='center', rotation='vertical')


Accepted(ordered)
plt.show()
