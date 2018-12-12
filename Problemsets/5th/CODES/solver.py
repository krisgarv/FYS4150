import numpy as np
import matplotlib.pyplot as plt
import numba
import scipy.linalg as sl

def ForwardEuler(alpha, v, N, T):
	#Explicit forward euler SCHEME
	for t in range(1, T): #T+1
		for x in range(1, N+1):
			v[t,x] = alpha*v[t-1,x-1] + (1.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
	return v

def LU_decomp(A, vPrev):
    lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
    LHS = sl.lu_solve((lu, piv), vPrev, trans=0, overwrite_b=True, check_finite=False)
    return LHS

def BackwardEuler(alpha, v, N, T):
    A = np.zeros((N+2, N+2)) + np.diag(1.0+2.0*alpha*np.ones(N+2)) + \
    np.diag(-alpha*np.ones(N+1), k=1) + np.diag(-alpha*np.ones(N+1), k=-1)
    for t in range(1, T): #Gammel: T+1
        v[t, :] = LU_decomp(A, v[t-1, :])
    return v

def CrankNicolson_LU(alpha, v, N, T):
    A = np.zeros((N+2, N+2)) + np.diag(2.0+2.0*alpha*np.ones(N+2)) + \
    np.diag(-alpha*np.ones(N+1), k=1) + np.diag(-alpha*np.ones(N+1), k=-1)
    for t in range(1, T): #Gammel: T+1
        for x in range(1, N+1):
            v[t, x]= alpha*v[t-1,x-1] + (2.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
            #v[t, 1:-1] = 2.0*FwdStep(alpha/2.0, v[t-1, :], N)
        v[t, :] = LU_decomp(A, v[t, :])
    return v
