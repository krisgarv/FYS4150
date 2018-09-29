from scipy.linalg import toeplitz
import numpy as np
N=4
rho = np.linspace(0,1,N+1)
h = 1./N
v = np.zeros_like(rho)
lmbda = np.zeros(N-1)
r = np.zeros(N-1)
c = np.zeros(N-1)
r[0]=2
r[1]=-1
A = (1./h**2)*toeplitz(r,r)
#print(A)

EigVal,EigVec = np.linalg.eig(A)
print(EigVal)

eigen=[]
for i in range(1,N):
    eigen.append((2/h**2)*(1-1*np.cos((np.pi*i)/(N))))
print (eigen)

#Jacobi's rotational algorithm
# define matrix R for eigenvectorsself.
R_ = np.zeros(N-1)
R_[0] = 1
R = toeplitz(R_,R_)
print(R)

tolerance = 1.0E-10
iterations = 0
def Jacobi(a,tolerance):

    def maxElm(A):

        #This function find the largest off-diagonal element
        #in the matrix by itterating over every element in the matrix.

        max = 0.0
        for i in range(N-1):
            for j in range(i+1,N):
                if abs(A[i,j]) >= max
                    max = abs([i,j])
                    k = i; l = j
        return max,k,l

        def rotate(A,R,p,k,l,N):

            #This function rotate to make the off-diagonal elements
            #zero.

            if (A(k,l) != 0.0):
                tau = (A[l,l]-A[k,k])/(2*A[k,l])
                if tau >= 0:
                    t = 1.0/(tau + np.sqrt(1.0+tau**2))
                else:
                    t = -1.0/(-tau + np.sqrt(1.0+tau**2))
                c = 1/np.sqrt(1.0+t**2)
                s = c*t
            else:
                c = 1.0
                s = 0.0
            a_kk = A[k,k]
            a_ll = A[l,l]
            A[k,k] = c**2*a_kk - 2.0*c*s*A[k,l] + s**2*a_ll
            a[l,l] = s**2*a_kk + 2.0*c*s*A[k,l] + c**2*a_ll
            A[k,l] = 0.0 #Hard-coding non-diagonal elements by hand
            A[l,k] = 0.0 # Same here
            for i in range(N-1):
                if (i != k and i<N):
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

maxiter = 10
p = np.identity(N)*1.0
while (max > tolerance and iterations <= maxiter):
    rotate()
