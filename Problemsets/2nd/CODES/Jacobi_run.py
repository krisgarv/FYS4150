# Importing necessary functionalities:
from Jacobi import Eigenvalues as J
import scipy.linalg as sl
import numpy as np
import time
import sys
import argparse

"""
This script is made for solving the problems from Problem set 2 in FYS4150,
fall 2018, and uses hardcoded initial values from this problem set.
The dimensionality N, and which of the three problems to be solved must be
given as command line arguments.
In addition you can choose to change the upper boundary condition, rho_max for
the quantum dot problems. The scripts runs only the numpy solver as default,
as the Jacobi solver is very slow for large dimensions.
"""
# Collecting necessary input arguments from command line:
pa = argparse.ArgumentParser(description='Run script for Jacobi method \
        to solve one of three spesific eigenvalue problems.')
# Dimension is a mandatory input variable:
pa.add_argument('N', type=int, help='Matrix dimension.')
# Which problem to solve is a mandatory variable:
pa.add_argument('Problem', type=str, help='Choose one of the following problems\
        to solve: \n BB - Bucling beam, \n HO1 - Harmonic oscillator with one \
        electron, \n HO2 - Harmonic oscillator with two electrons.')
# Upper boundary for Haronic oscillator problems to be solved:
pa.add_argument('-rho_max', type=float, default=5.0, help='Upper boundary \
        condition for Harmonic oscillator problems. Optional variable, \
        Default = 5.0')
# Optional boolean variable, wheather to calculate eigenvalues with only Numpys
# built-in method or also our slow Jacobi method, makes calculations for large
# dimensionality possible.
pa.add_argument('-Jacobisolver', type=bool, default=False, \
        help=' Boolean variable. \
        If True: \
        Calculates eigenvalues using both numpys built in method and Jacobis \
        method. Default = False -> only computes by numpys \
        method. WARNING: SLOW, for large N when set to True.')
arg = pa.parse_args()
# Collecting the command line arguments and converting them to global variables.
N = arg.N
P = arg.Problem
rho_max = arg.rho_max
both = arg.Jacobisolver
#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
# Defining a function to make use of the functions from our module.
# Depending on the input variables.

def run(N, a, di):
    # Creating the input matrix, filling in diagonal elements with the array di,
    # the non-diagonal elements with the constant a, into a NxN matrix of zeros.
    A = np.zeros((N, N)) + np.diag(di) + np.diag(a*np.ones(N-1), k=1) +\
        np.diag(a*np.ones(N-1), k=-1)

    # Calling the Jacobi module with the matrix A.
    i = J(A)

    # Numpys solution:
    t0 = time.time()
    # The Numpy function in our module returns two elements:
    # Nlmbda is an array containing the eigenvalues of the input matrix.
    # Nvec is a matrix containing the eigenvectors of the input matrix.
    eigval_numpy, eigvec_numpy = i.nmpy_eigenval()
    t1 = time.time()
    # Taking the time of the calculation.
    time_numpy = t1 - t0


    # Jacobi's solution. Only computed if boolean variable -both is set to True.
    if both == True:
        # Jacobi solution:
        t2 = time.time()
        # The Jacobi function in our module retuns three elements:
        # Jacobi_A, an array containing the eigenvalues.
        # Jacobi_R is a matrix of eigenvectors.
        # Jacobi_iter is the number of rotaions necessary to make all
        # non-diagonal elements smaller epsilon = 1e-8
        eigval_Jacobi, eigvec_Jacobi, iter_Jacobi = i.Jacobi()
        t3 = time.time()
        # Taking the time of the calculation.
        time_jacobi = t3 - t2


        # Returning results from both Jacobis and numpys method.
        return  eigval_Jacobi, eigval_numpy, iter_Jacobi, \
                time_jacobi, time_numpy
    else:
        # Returning results only from numpys method.
        return eigval_numpy, time_numpy

#-------------------------------------------------------------------------------
# Function which calculates analytic solution for Buckling beam problem:
def analytic_eigenval(N, a, d):
    lmbda = []
    # Storing eigenvalues to empty list
    for i in range(1, N+1):
        l = d + 2.0*a*np.cos((i*np.pi)/(N+1))
        lmbda.append(l)
    # Returns list of analytic eigenvalues.
    return lmbda


#-------------------------------------------------------------------------------
# Function which prints results to terminal in a nice way.
def printing(N, a, di):
    # Checking weather to calculate and print both Jacobis and Numpys solution.
    if both == True:
        # Results of both Jacobis and Numpys method are extracted from run function.
        eigval_Jacobi, eigval_numpy, iter_Jacobi, time_jacobi, time_numpy = run(N, a, di)
        # Printing to terminal.
        print (' ')
        print("Eigenvalues obtained by library function from numpy: %a" \
                %(eigval_numpy))
        print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
                %(N, N, time_numpy))
        print (' ')
        print ("Eigenvalues obtained by Jacobi's method: %a" % (eigval_Jacobi))
        print ("Time spendt by Jacobi's method, for a %dx%d matrix: %gs"\
            %(N, N, time_jacobi))
        print ("Number of similarity transformations, for %dx%d matrix:%d" \
            % (N, N, iter_Jacobi))
    # Or calculating and printing only Numpys solutions.
    else:
        # Results of Numpys method are extracted from run function.
        eigval_numpy, time_numpy = run(N, a, di)
        # Printing to terminal.
        print (' ')
        print("Eigenvalues obtained by library function from numpy: %a" \
            %(eigval_numpy))
        print("Time spendt by numpys method, for a %dx%d matrix: %gs" \
            %(N, N, time_numpy))

#-------------------------------------------------------------------------------
# The buckling beam problem:
#-------------------------------------------------------------------------------
# Checking input string from command line:
if P == 'BB':
    # Initial matrix elements
    h = 1.0/(N+1)         # Step size
    a = (-1.0/h**2)     # Non-diagonal element, constant
    d = (2.0/h**2)      # Diagonal element, constant
    di = d*np.ones(N)   # Create input array of diagonal elements
    # Solving Buckling beam problem analytically through function analytic_eigenval.
    analytic = analytic_eigenval(N, a, d)
    # Printing header to terminal.
    print ('SOLUTIONS FOR BUCKLING BEAM PROBLEM:')
    # Printing analytic eigenvalues to terminal.
    print("Eigenvalues obtained analytically: %a" %(analytic))
    # Printing the other solutions through the function printing.
    printing(N, a, di)

#-------------------------------------------------------------------------------
# Harmonic oscillator in three dimensions, with one electron:
#-------------------------------------------------------------------------------
elif P == 'HO1':
    #Initial matrix elements:
    h = float(rho_max)/N        # Step size
    a = -1.0/h**2               # Non-diagonal element, constant
    di = np.zeros(N)            # Initial array of zeros for diagonal elements
    for i in range(N):          # Calculating diagonal elements
        di[i] = 2.0/h**2 + (i*h)**2
    # Printing header to terminal
    print ('SOLUTIONS FOR HARMONIC OSCILLATOR IN THREE DIMENSIONS WITH ONE ELECTRON:')
    # Printing solutions through the function printing.
    printing(N, a, di)

#-------------------------------------------------------------------------------
# Harmonic oscillator in three dimensions, with two electrons:
#-------------------------------------------------------------------------------
# Checking input string from command line:
elif P == 'HO2':
    #Initial matrix elements
    h = float(rho_max)/N        # Step size
    a = -1.0/h**2               # Non-diagonal element, constant
    di = np.zeros(N)            # Initial array of zeros for diagonal elements
    di[0] = 1/h**2
    omega = [0.01, 0.5, 1., 5.]
    print ('SOLUTIONS FOR HARMONIC OSCILLATOR IN THREE DIMENSIONS WITH TWO ELECTRONS:')
    for j in omega:
        for i in range(1,N):
            di[i] = (2 + j**2*i**2*h**4 + h*(1./i))/h**2
        print (' ')
        print('Omeaga = %f'%(j))
        printing(N, a, di)
#-------------------------------------------------------------------------------
else:
    # If the problem name is not recognizeable, refer to help page.
    print('Problem not recognized. See: $ python Jacobi_run.py --help')
