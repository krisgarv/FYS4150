import numpy as np
import ising_model as I
import matplotlib.pyplot as plt
import time
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
sns.set_context('talk')

#Energy_T1, MagnetizationAbs_T1, magnet_avg, C_v, X, accepted_list= I.MC(spin_matrix, MC_cycles, Temp[0])
#spin_matrix = np.random.choice((-1, 1), (num_spins, num_spins))

L = [40,60,80,100]
T = np.arange(2.0, 2.31, 0.05)
#print(T)

MC_cycles = 100000
#Make Energy like matrix, LXT?
E = np.zeros((len(L),len(T)))
M_abs = np.zeros((len(L),len(T)))
m_av = np.zeros((len(L),len(T)))
C_v = np.zeros((len(L),len(T)))
X = np.zeros((len(L),len(T)))

norm = 1/float(MC_cycles-40000)
for i, spins in enumerate(L):
    spin_matrix = np.ones((L[i],L[i]), np.int8)

    for j, temp in enumerate(T):
        t0 = time.time()
        exp_values = I.MC(spin_matrix, MC_cycles, temp)
        t1 = time.time()

        energy_avg = (np.cumsum(exp_values[40000:,0])/np.arange(40001, MC_cycles+1))#/(spins**2)
        magnet_abs_avg = (np.cumsum(exp_values[40000:, 4])/np.arange(40001, MC_cycles+1))#/(spins**2)
        energy_avg = np.sum(exp_values[40000:, 0])
        magnet_abs_avg = np.sum(exp_values[40000:, 4])
        energy2_avg = np.sum(exp_values[40000:,2])
        magnet2_avg = np.sum(exp_values[40000:,3])
        energy_var = (energy2_avg - energy_avg[-1]**2)*norm/((spins)**2)
        magnet_var = (magnet2_avg - magnet_abs_avg[-1]**2)*norm/((spins)**2)

        E[i,j] = (energy_avg)/(spins**2)
        M_abs[i,j] = (magnet_abs_avg)/(spins**2)
        C_v[i, j] = energy_var/temp**2
        X[i, j] = magnet_var/temp

print(energy_var)


fig, ax = plt.subplots(2, 2, figsize=(18, 12), sharex=True)
plt.suptitle('Something')
for i in range(4):
    ax[0, 0].plot(T, E[i, :], label='Energy')
    ax[0, 1].plot(T, M_abs[i, :], label='Magnetization')
    ax[1, 0].plot(T, C_v[i, :], label='Specific Heat')
    ax[1, 1].plot(T, X[i, :], label='Susceptibility')
    #ax[0, 0].set_xlabel('Temperature')
    #ax[0, 1].set_xlabel('Temperature')
    ax[1, 0].set_xlabel('Temperature')
    ax[1, 1].set_xlabel('Temperature')
plt.suptitle('Numerical studies of phase transitions')
plt.show()
