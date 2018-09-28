from Jacobi_class import Eigenvalues as J
import scipy.linalg as sl
import numpy as np
import time
import sys
import argparse
#-------------------------------------------------------------------------------
# Collecting necessary input arguments from command line
pa = argparse.ArgumentParser(description='Run script for Jacobi method \
        to solve one of three spesific eigenvalue problems.',\
        epilog='...')
pa.add_argument('N', type=int, help='Matrix dimension.')
pa.add_argument('Problem', type=str, help='Choose one of the following problems\
        to solve: \n BB - Bucling beam, \n HO1 - Harmonic oscillator with one \
        electron, \n HO2 - Harmonic oscillator with two electrons.')
pa.add_argument('-rho_max', type=float, default=None, help='To be able to \
        calculate the Haronic oscillator problems, the approximated max value \
        of the range must me given as an input argument.')
pa.add_argument('-both', action='store_true', default=False, help='Calculates eigenvalues \
        using both numpys built in method and Jacobis method. WARNING: slow')
arg = pa.parse_args()
N = arg.N
P = arg.Problem
rho_max = arg.rho_max
both = arg.both

#-------------------------------------------------------------------------------

def run(N, a, di):
    # Creating the input matrix
    A = np.zeros((N, N)) + np.diag(di) + np.diag(a*np.ones(N-1), k=1) +\
        np.diag(a*np.ones(N-1), k=-1)

    # Calling the Jacobi module with initial values for buckling beam.
    i = J(A)

    # Numpys solution:
    t0 = time.time()
    Nlmbda, Nvec = i.nmpy_eigenval()
    t1 = time.time()
    time_numpy = t1 - t0

    # Sorting eigenvalues by size to simplify comparison.
    NA = np.sort(Nlmbda)

    if both == True:
        # Jacobi solution:
        t2 = time.time()
        Jacobi_A, Jacobi_R, Jacobi_iter = i.Jacobi()
        t3 = time.time()
        time_jacobi = t3 - t2

        # Sorting eigenvalues by size to simplify comparison.
        JA = np.sort(np.diag(Jacobi_A))
        return  JA, NA, Jacobi_iter, time_jacobi, time_numpy
    else:
        return NA, time_numpy

# Function which calculates analytic solution for Buckling beam problem:
def analytic_eigenval(N, a, d):
    lmbda = []
    for i in range(1, N+1):
        l = d + 2.0*a*np.cos((i*np.pi)/(N+1))
    lmbda.append(l)
    #analytic = np.asarray(lmbda)
    return lmbda#analytic

#-------------------------------------------------------------------------------
# The buckling beam:
#-------------------------------------------------------------------------------
if P == 'BB':
    #Initial matrix elements
    h = 1.0/(N+1)
    a = (-1.0/h**2)
    d = (2.0/h**2)
    di = d*np.ones(N)
    analytic = analytic_eigenval(N, a, d)
    print ('SOLUTIONS FOR BUCKLING BEAM PROBLEM:')
    print("Eigenvalues obtained analytically: %a" %(analytic))
    if both == True:
        JA, NA, Jacobi_iter, time_jacobi, time_numpy = run(N, ai, di)
        print (' ')
        print("Eigenvalues obtained by library function from numpy: %a" \
                %(NA))
        print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
        print (' ')
        print ("Eigenvalues obtained by Jacobi's method: %a" % (JA) )
        print ("Time spendt by Jacobi's method, for a %dx%d matrix: %gs"\
            %(N, N, time_jacobi))
        print ("Number of similarity transformations, for %dx%d matrix:%d" \
            % (N, N, Jacobi_iter))
    else:
        NA, time_numpy = run(N, ai, di)
        print (' ')
        print("Eigenvalues obtained by library function from numpy: %a" \
            %(NA))
        print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
            %(N, N, time_numpy))

#-------------------------------------------------------------------------------
#Harmonic oscillator in three dimensions, with one electron:
#-------------------------------------------------------------------------------
if P == 'HO1':
    if rho_max != None:
        #Initial matrix elements:
        h = float(rho_max)/N
        a = -1.0/h**2
        di = np.zeros(N)
        for i in range(N):
            # rho_i = rho_0 + i*h = i*h
            di[i] = 2.0/h**2 + (i*h)**2
        print ('SOLUTIONS FOR HARMONIC OSCILLATOR IN THREE DIMENSIONS WITH ONE ELECTRON:')
        if both == True:
            JA, NA, Jacobi_iter, time_jacobi, time_numpy = run(N, a, di)
            print("Eigenvalues obtained by library function from numpy: %a" \
                %(NA))
            print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
            print (' ')
            print ("Eigenvalues obtained by Jacobi's method: %a" % (JA) )
            print ("Time spendt by Jacobi's method, for a %dx%d matrix: %gs"\
                %(N, N, time_jacobi))
            print ("Number of similarity transformations, for %dx%d matrix:%d" \
                % (N, N, Jacobi_iter))
        else:
            NA, time_numpy = run(N, a, di)
            print("Eigenvalues obtained by library function from numpy: %a" \
                %(NA))
            print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
    else:
        print('Initial value missing: rho_max. \n Go to help page:')
        print('$ python Jacobi_run.py --help')
#-------------------------------------------------------------------------------
##Harmonic oscillator in three dimensions, with two electrons:
#-------------------------------------------------------------------------------
if P == 'HO2':
    if rho_max != None:
        #Initial matrix elements
        h = float(rho_max)/N
        a = -1.0/h**2
        di = np.zeros(N)
        di[0] = 1/h**2
        omega = [0.01, 0.05, 1., 5.]
        for j in omega:
            for i in range(1,N):
                di[i] = (2 + j**2*i**2*h**4 + h*(1./i))/h**2
        print ('SOLUTIONS FOR HARMONIC OSCILLATOR IN THREE DIMENSIONS WITH TWO ELECTRONS:')
        if both == True:
            JA, NA, Jacobi_iter, time_jacobi, time_numpy = run(N, a, di)
            print("Eigenvalues obtained by library function from numpy: %a" \
                %(NA))
            print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
            print (' ')
            print ("Eigenvalues obtained by Jacobi's method: %a" % (JA) )
            print ("Time spendt by Jacobi's method, for a %dx%d matrix: %gs"\
                %(N, N, time_jacobi))
            print ("Number of similarity transformations, for %dx%d matrix:%d" \
                % (N, N, Jacobi_iter))
        else:
            NA, time_numpy = run(N, a, di)
            print("Eigenvalues obtained by library function from numpy: %a" \
                %(NA))
            print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
    else:
        print('BAD USAGE! Initial value missing: rho_max.')
        print('Go to help page: python Jacobi_run.py --help')

#-------------------------------------------------------------------------------
