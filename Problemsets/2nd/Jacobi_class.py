import numpy as np
import scipy.linalg as sl

class Eigenvalues():

    def __init__(self, A):
        self.N = len(A[0, :])
        self.M = A

#---------------------------------------------------------------------
    # Functions needed for Jacobi's method:
    # Finding the largest value off the diagonal:
    def maxoffdiag(self, A):
        k = 0
        l = 1
        maxval = 0.0
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    Aij = float(np.abs(A[i,j]))
                    if Aij > maxval:
                        maxval = Aij
                        k = i
                        l = j
        return maxval, k, l

    # Defining the rotation matrix
    def rotate(self, A, R, l, k):
        if A[k, l] != 0.0 :
            tau = (A[l,l] - A[k,k])/(2.0*A[k,l])
            if tau > 0 :
                t = 1.0/(tau + np.sqrt(1.0 + tau**2))
            else:
                t = -1.0/(-tau + np.sqrt(1.0 + tau**2))
            c = 1.0/(np.sqrt(1 + t**2))
            s = c*t
        else:
            c = 1.0
            s = 0.0
        a_kk = A[k,k]
        a_ll = A[l,l]
        A[k,k] = c**2*a_kk - 2.0*c*s*A[k,l] + s**2*a_ll
        A[l,l] = s**2*a_kk + 2.0*c*s*A[k,l] + c**2*a_ll
        A[k,l] = 0.0
        A[l,k] = 0.0
        for i in range(self.N):
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
    def Jacobi(self):
        A = self.M
        # Creating a identity matrix:
        R = np.identity(self.N)
        # Initial input for Jacobi's method:
        max_offdiag, k, l = self.maxoffdiag(A) # initital max value off diagonal
        epsilon = 1.0e-8
        maxiter = float(self.N)**3  # maximum number of iterations
        initer = 0 # initial iteration value
        while (max_offdiag > epsilon and initer < maxiter):
            A, R = self.rotate(A, R, k, l)
            max_offdiag, k, l = self.maxoffdiag(A)
            initer = initer + 1
        return A, R, initer

#--------------------------------------------------------------------------

    # Eigenvalues found with numpys solver eig:
    def nmpy_eigenval(self):
        A = self.M
        lmbda, eigenvec = np.linalg.eig(A)
        return lmbda, eigenvec

#-------------------------------------------------------------------------
