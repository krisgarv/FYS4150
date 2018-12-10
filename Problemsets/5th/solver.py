import numpy as np
import matplotlib.pyplot as plt
import numba
import scipy.linalg as sl

@numba.njit(cache = True)
def FwdStep(alpha, vPrev, N):
    v = np.zeros(N-1)
    for x in range(0,N-1):
        v[x] = alpha*vPrev[x-1] + (1.0-2*alpha)*vPrev[x] + alpha*vPrev[x+1]
    return v
"""

def FwdStep(alpha, vPrev, N):
    A = np.zeros((N+1, N+1)) + np.diag(2.0-2.0*alpha*np.ones(N+1)) + \
    np.diag((alpha)*np.ones(N), k=1) + np.diag((alpha)*np.ones(N), k=-1)
    v = np.matmul(A, vPrev)
    return v
def LU_decomp(alpha, vPrev, N):
    A = np.zeros((N+1, N+1)) + np.diag(1.0+2.0*alpha*np.ones(N+1)) + \
    np.diag(-alpha*np.ones(N), k=1) + np.diag(-alpha*np.ones(N), k=-1)
    lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
    LHS = sl.lu_solve((lu, piv), vPrev, trans=0, overwrite_b=True, check_finite=False)
    return LHS
def ForwardEuler(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, :] = FwdStep(alpha, v[t-1, :], N)
    return v

def BackwardEuler(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, :] = LU_decomp(alpha, v[t-1, :], N)
    print(v[0, :]) # BURDE VÆRE UENDRET [0, 0, ..., 0, 0, 1], MEN ER IKKE DET!
    return v

def CrankNicolson(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, :] = FwdStep(alpha/2, v[t-1, :], N)
        v[t, :] = LU_decomp(alpha/2, v[t, :], N)
    return v

def FwdStep(alpha, vPrev, N):
    A = np.zeros((N-1, N-1)) + np.diag(2.0-2.0*alpha*np.ones(N-1)) + \
    np.diag((alpha)*np.ones(N-2), k=1) + np.diag((alpha)*np.ones(N-2), k=-1)
    v = np.matmul(A, vPrev)
    return v
"""
def LU_decomp(alpha, vPrev, N):
    A = np.zeros((N-1, N-1)) + np.diag(1.0+2.0*alpha*np.ones(N-1)) + \
    np.diag(-alpha*np.ones(N-2), k=1) + np.diag(-alpha*np.ones(N-2), k=-1)
    lu, piv = sl.lu_factor(A, overwrite_a=True, check_finite=False)
    LHS = sl.lu_solve((lu, piv), vPrev, trans=0, overwrite_b=True, check_finite=False)
    return LHS


def ForwardEuler(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, 1:-1] = FwdStep(alpha, v[t-1, :], N)
    print(v[0, :])
    return v

def BackwardEuler(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, 1:-1] = LU_decomp(alpha, v[t-1, 1:-1], N)
    print(v[0, :]) # BURDE VÆRE UENDRET [0, 0, ..., 0, 0, 1], MEN ER IKKE DET!
    return v

def CrankNicolson(alpha, v, T, N):
    for t in range(1, T+1):
        v[t, 1:-1] = FwdStep(alpha/2, v[t-1, :], N)
        v[t, 1:-1] = LU_decomp(alpha/2, v[t, 1:-1], N)
    return v
