import numpy as np
import scipy.linalg as sl

"""
NUMERICAL SOLVER - 3 methods
Input:
	alpha = dt/dx^2
	v = Initial matrix with time steps as columns and spatial position as rows.
	N = Number of spatial steps
	T = Number of time steps
Output:
	v = Output matrix v(t, x)
"""

def ForwardEuler(alpha, v, N, T):
	#Explicit forward euler scheme
	for t in range(1, T):
		for x in range(1, N+1):
			v[t,x] = alpha*v[t-1,x-1] + (1.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
	return v

def LU_decomp(A, vPrev):
	# Lower-Upper decomposition function from scipy.linalg library
	# Takes the left-hand-side(LHS) matrix that is multiplied with an unknown vector
	# and the known right-hand-side(RHS) vector (previous time step), as input.
    lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
    LHS = sl.lu_solve((lu, piv), vPrev, trans=0, overwrite_b=True, check_finite=False)
    return LHS

def BackwardEuler(alpha, v, N, T):
	# Implicit Backward Euler scheme
	# Matrix for decomposition
    A = np.zeros((N+2, N+2)) + np.diag(1.0+2.0*alpha*np.ones(N+2)) + \
    np.diag(-alpha*np.ones(N+1), k=1) + np.diag(-alpha*np.ones(N+1), k=-1)
	# Looping over each time step, solving the next by LU-decomposition
    for t in range(1, T):
        v[t, :] = LU_decomp(A, v[t-1, :])
    return v

def CrankNicolson(alpha, v, N, T):
	# Ckrank Nicolson method
	# Matrix for decomposition
    A = np.zeros((N+2, N+2)) + np.diag(2.0+2.0*alpha*np.ones(N+2)) + \
    np.diag(-alpha*np.ones(N+1), k=1) + np.diag(-alpha*np.ones(N+1), k=-1)
	# Looping over each time step, solving first the (RHS) matrix-vector multiplication
	# And then feed the resulting vector to the LU-decomposition function
	# as the previous time step.
    for t in range(1, T):
        for x in range(1, N+1):
            v[t, x]= alpha*v[t-1,x-1] + (2.0-2.0*alpha)*v[t-1,x] + alpha*v[t-1,x+1]
        v[t, :] = LU_decomp(A, v[t, :])
    return v
