import numpy as np
import matplotlib.pyplot as plt
import numba
import scipy.linalg as sl
"""
@numba.njit(cache = True)
def FwdStep(alpha, vPrev, N):
    v = np.zeros(N-1)
    for x in range(0,N-1):
        v[x] = alpha*vPrev[x-1] + (1.0-2*alpha)*vPrev[x] + alpha*vPrev[x+1]
    return v
"""
def tridiag(alpha, u, N):
    b = 2.0 + 2.0*alpha
    a = c = -alpha
    b_hat = np.zeros(N+1) + b

    # Forward Substitute
    for i in range(1, N):
        b_hat[i] = b - a*c/float(b_hat[i-1])
        u[i] = u[i] - a*u[i+1]/float(b_hat[i])
    # Backward substitute
    for i in range(N, 0, -1):
        u[i] = (u[i]-c*u[i+1])/float(b_hat[i])
    return u


def ForwardEuler(alpha, v, N, T):
	#Explicit forward euler SCHEME
	for t in range(1, T+1):
		for x in range(1, N):
			v[t,x]= alpha*v[t-1,x-1] + (1.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
	return v

def LU_decomp(A, vPrev, N):
    lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
    LHS = sl.lu_solve((lu, piv), vPrev, trans=0, overwrite_b=True, check_finite=False)
    return LHS

def BackwardEuler(alpha, v, N, T):
    A = np.zeros((N, N)) + np.diag(1.0+2.0*alpha*np.ones(N)) + \
    np.diag(-alpha*np.ones(N-1), k=1) + np.diag(-alpha*np.ones(N-1), k=-1)
    for t in range(1, T+1):
        v[t, 1:-1] = LU_decomp(A, v[t-1, 1:-1], N)
    return v

def CrankNicolson_LU(alpha, v, N, T):
    A = np.zeros((N, N)) + np.diag(2.0+2.0*alpha*np.ones(N)) + \
    np.diag(-alpha*np.ones(N-1), k=1) + np.diag(-alpha*np.ones(N-1), k=-1)
    for t in range(1, T+1):
        for x in range(1, N):
            v[t, x]= alpha*v[t-1,x-1] + (2.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
            #v[t, 1:-1] = 2.0*FwdStep(alpha/2.0, v[t-1, :], N)
        v[t, 1:-1] = LU_decomp(A, v[t, 1:-1], N)
    return v

def CrankNicolson_TD(alpha, v, N, T):
    for t in range(1, T+1):
        for x in range(1, N):
            v[t, x]= alpha*v[t-1,x-1] + (2.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
        v[t, :] = tridiag(alpha, v[t, :], N)
    return v
