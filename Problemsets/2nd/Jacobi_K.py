import numpy as np
import sys
import scipy.linalg as sl
from math import *
#N = int(sys.argv[1])
# Initial values
N = 3
h = 1.0/N
d = (1.0/h**2)*2.0
a = (1.0/h**2)*-1.0

# Creating input arrays for toeplitz matrix:
r = np.zeros(N-1)
r[0] = d
r[1] = a
A = sl.toeplitz(r, r)

# Creating a identity matrix:
R = np.identity(N-1)

# Finding the largest value off the diagonal
def maxoffdiag(A):
    maxval = 0.0
    for i in range(N-2):
        for j in range(1, N-1):
            k = i
            l = j
            Aij = float(np.abs(A[i,j]))
            if Aij > maxval:
                maxval = Aij
    return maxval, k, l

# Rotation
def rotate(A, k, l):
    if A[l,k] != 0.0 :
        tau = (A[l,l] - A[k,k])/(2.0*A[k,l])
        if tau > 0 :
            t = 1.0/(tau + np.sqrt(1.0 + tau**2))
        else:
            t = -1.0/(tau - np.sqrt(1.0 + tau**2))

        c = 1.0/np.sqrt(1 + t**2)
        s = c
    else:
        c = 1.0
        s = 0.0
    a_kk = A[k,k]
    a_ll = A[l,l]
    A[k,k] = c**2*a_kk - 2.0*c*s*A[k,l] + s**2*a_ll
    A[l,l] = s**2*a_kk + 2.0*c*s*A[k,l] + c**2*a_ll
    A[k,l] = 0.0
    A[l,k] = 0.0
    for i in range(N-1):
        if i != k and i != l :
            a_ik = A[i,k]
            a_il = A[i,l]
            A[i,k] = c*a_ik - s*a_il
            A[k,i] = A[i,k]
            A[i,l] = c*a_il + s*a_ik
            A[l,i] = A[i,l]
        r_ik = R[i,k]
        r_il = R[i,l]
        R[i,k] = c*r_ik - s*r_il
        R[i,l] = c*r_il + s*r_ik
    return A, R

# Input from functions to Jacobi's method:
epsilon = 1.0e-8
maxiter = float(N)**3  # maximum number of iterations
max_offdiag, k, l = maxoffdiag(A) # max value of off diagonal elements
initer = 0 # initial iteration value

# Jacobi's method:
while (max_offdiag > epsilon and initer < maxiter):
    max_offdiag, k, l = maxoffdiag(A)
    A, R = rotate(A, k, l)
    initer = initer + 1

print (A, R)
