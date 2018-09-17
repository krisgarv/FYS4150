import numpy as np
import sys
import scipy.linalg as sl
from math import *
import time
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

#--------------------------------------------------------------------
# Solution found from library functions:
def nmpy_eigenval(A):
    lmbda, eigenvec = np.linalg.eig(A)
    return lmbda

# Function which calculates analytic solution:
def analytic_eigenval(N, d, a):
    lmbda = []
    for i in range(1, N):
        l = d + 2.0*a*np.cos((i*np.pi)/(N))
        lmbda.append(l)
    return lmbda

#---------------------------------------------------------------------
# Functions needed for Jacobi's method:
# Finding the largest value off the diagonal:
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

# Defining the rotation matrix
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


# Jacobi's method:
def Jacobi(A):
    # Initial input for Jacobi's method:
    max_offdiag, k, l = maxoffdiag(A) # initital max value off diagonal
    epsilon = 1.0e-8
    maxiter = float(N)**3  # maximum number of iterations
    initer = 0 # initial iteration value
    while (max_offdiag > epsilon and initer < maxiter):
        max_offdiag, k, l = maxoffdiag(A)
        A, R = rotate(A, k, l)
        initer = initer + 1
    return A, R, initer

# Analytic calculation:
analytic = analytic_eigenval(N, d, a)

# Numpys solution:
t0 = time.time()
library = nmpy_eigenval(A)
t1 = time.time()
time_numpy = t1 - t0

# Jacobi solution:
t0 = time.time()
Jacobi_A, Jacobi_R, Jacobi_iter = Jacobi(A)
t1 = time.time()
time_jacobi = t1 - t0

print("Eigenvalues obtained analytically: %a" %(analytic))
print (' ')
print("Eigenvalues obtained by library function from numpy: %a" \
    %(library))
print("Time spendt by numpys method, for a %dx%d matrix: %g" \
    %(N-1, N-1, time_numpy))
print (' ')
print ("Eigenvalues obtained by Jacobi's method: %a" % (np.diag(Jacobi_A)) )
print ("Time spendt by Jacobi's method, for a %dx%d matrix: %g"\
    %(N-1, N-1, time_jacobi))
print ("Number of similarity transformations, for %dx%d matrix:\
 %d" % (N-1, N-1, Jacobi_iter))

#-------------------------------------------------------------------------

import unittest

class MyTest(unittest.TestCase):

    def test_maxoffdiag(self):
        # 2x2 symmetric matrix
        A = [[1, 4],[4, 5]]
        maxval, k, l = maxoffdiag(A)
        self.assertEqual(maxval, 4)


    def test_jacobi(self):
        # simple 2x2 symmetric matrix with known Eigenvalues
        Ax = [[2, -1],[-1, 2]]
        max_offdiag = -1.0
        initer = 0
        A, R, initer = Jacobi(Ax)
        eigenvalues = np.diag(A)
        lmbda1 = 1
        lmbda2 = 3
        self.assertEqual(eigenvalues[1] == lmbda1)
        self.assertEqual(eigenvalues[0] == lmbda2)
"""
 2c)
Implement tests for:
-the rotation function
    is orthogonality preserverd?
-the maxoffdiag function
    is maxval the largest one?
-the jacobi method
    for a simple 2x2 matrix
    correct eigenvalues?
-OTHER TESTS?
"""
