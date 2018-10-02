import numpy as np
import scipy.linalg as sl

"""
This module calculates the eigenvalues of a square matrix in two ways:
- The eigenvalues can be derived through Jacobi's method, where a similarity
transformation is repeatedly appleid to the matrix until all the
non-diagonal elements are approximately zero. The eigenvalues can then be
extracted from the diagonal of the output matrix.
- For comparison the eigenvalues are also calculated using the numpy.eig
function from the numpy library.
"""

class Eigenvalues():

    def __init__(self, A):
        """
        The module takes a square matrix as input variable and calculates
        the dimensionality of it. These make up the global variables of the
        module.
        """
        self.N = len(A[0, :])
        self.M = A

#-------------------------------------------------------------------------------
# Functions needed for Jacobi's method:
#-------------------------------------------------------------------------------

    # Finding the largest value off the diagonal:
    def maxoffdiag(self, A):
        """
        The maxoffdiag function loops through all matrix elements and finds the
        position of the element with gratest absolute value. It returns the
        maximum value and the position index.
        """
        k = 0        # Initial position, demanded by the following if statement.
        l = 1
        maxval = 0.0    # Reset maxvalue to zero before looking for next one.
        # Looping over every matrix element.
        for i in range(self.N):
            for j in range(self.N):
                # Only searching among the non-diagonal elements
                if i != j:
                    # Taking the absoulte value so that large negative elements
                    # are not ignored.
                    Aij = float(np.abs(A[i,j]))
                    # Testing if the element is greater than the current max value.
                    if Aij > maxval:
                        # If true, the maxval variable is assign the greater value.
                        maxval = Aij
                        k = i       # Saving the position of the max value.
                        l = j
                        # Repeated through all elements.
        return maxval, k, l # Returning the max value and its position.

    # Similarity transformation.
    def rotate(self, A, R, l, k):
        """
        This function performs a similarity transformation on the matrices
        A and R. The Jacobi rotation aims to eliminate the largest non-diagonal
        elements, A[k, l] and A[l, k], found from the maxoffdiag function.
        As we are dealing with symmetric matrices the operations are done
        symmetrically about the diagonal.
        The rotation is done with an angle which depends on the elements to be
        eliminated and their correstponding diagonal elements.
        The downside of Jacobi's method with maxvalue elimitation is that
        elements off the diagonal that initially was zero can become non-zero
        under the rotation.
        """
        # Testing that the element is not already zero
        if A[k, l] != 0.0 :
            # Calculating tau, to be able to find the appropriate angle.
            tau = (A[l,l] - A[k,k])/(2.0*A[k,l])
            if tau > 0 :
                # tan(theta) for tau > 0
                t = 1.0/(tau + np.sqrt(1.0 + tau**2))
            else:
                # tan(theta) for tau < 0
                t = -1.0/(-tau + np.sqrt(1.0 + tau**2))
            # cos(theta)
            c = 1.0/(np.sqrt(1 + t**2))
            # sin(theta)
            s = c*t
        # If the elements are already zero
        else:
            # cos(theta)
            c = 1.0
            # sin(theta)
            s = 0.0
        # Hardcoding the initial diagonal elements for calculations
        a_kk = A[k,k]
        a_ll = A[l,l]
        # The new value of the diagonal elements
        A[k,k] = c**2*a_kk - 2.0*c*s*A[k,l] + s**2*a_ll
        A[l,l] = s**2*a_kk + 2.0*c*s*A[k,l] + c**2*a_ll
        # The new value of the non-diagonal elements
        A[k,l] = 0.0
        A[l,k] = 0.0
        # Looping over the rest of the elements in the k and l rows anfd columns
        for i in range(self.N):
            if i != k and i != l :
                # Hardcoding element values for calculation
                a_ik = A[i,k]
                a_il = A[i,l]
                # The new element values
                # Here zero-elements can become non-zero
                A[i,k] = c*a_ik - s*a_il
                A[k,i] = A[i,k]             # symmetry
                A[i,l] = c*a_il + s*a_ik
                A[l,i] = A[i,l]             # symmetry
            # Rotating the R matrix
            r_ik = R[i,k]
            r_il = R[i,l]
            R[i,k] = c*r_ik - s*r_il
            R[i,l] = c*r_il + s*r_ik
        # Returning the two transformed matrices
        return A, R

    # Jacobi's method:
    def Jacobi(self):
        """
        Main function of the module.
        The Jacobi function takes on the input matrix finds the largest
        non-diagonal element through the maxoffdiag function. Then it performs
        the rotation with the rotation function and repeats this process until
        all non-diagonal elements are approximately zero.
        Finally the function extracts the eigenvalues of the input matrix from
        the diagonal of the transformed matrix and stores them in an array.
        The array is returned along with the matrix R which contains the
        eigenvectors and the number of rotations necessary to achieve a
        transformed matrix with non-diagonal elements smaller than some
        threshold epsilon. The transformation process are aborted if the
        number of transformation exceeds the dimention of the matrix cubed.
        """
        # The matrix to be evaluated is collected from the input.
        A = self.M
        # Creating an identity matrix to be filled with the eigenvectors
        R = np.identity(self.N)
        # Finding the first non-diagonal max value
        # (must be found before the while loop as the output is used in the
        # condition for the loop)
        max_offdiag, k, l = self.maxoffdiag(A)
        # non-diagonal lower threshold, approximately zero
        epsilon = 1.0e-8
        # Maximum number of transformation before function aborts
        maxtrans = float(self.N)**3
        # initial iteration value
        transformations = 0
        # Repeating the transformations for the largest non-diagonal elements
        # until iterations reaches its maximum or all non-diagonal elements are
        # smaller than epsilon.
        while (max_offdiag > epsilon and transformations < maxtrans):
            # see function rotate()
            A, R = self.rotate(A, R, k, l)
            # see function maxoffdiag()
            max_offdiag, k, l = self.maxoffdiag(A)
            # counting transformations
            transformations = transformations + 1
        # Extracting eigenvalues from the diagonal of the final A matrix
        # Sorting eigenvalues by size to simplify comparison.
        A_out = np.sort(np.diag(A))
        # Returning eigenvalues sorted from smallest to largest and stored in an
        # array. Returning the R matrix containing the eigenvectors and the
        # number of transformations performed.
        return A_out, R, transformations

#--------------------------------------------------------------------------

    # Eigenvalues found with numpys built-in solver:
    def nmpy_eigenval(self):
        """
        The mnpy_eigenval function uses the library function eig to calculate
        the eigenvalues and eigenvectors of the input matrix. The eigenvalues
        are sorted by size and returned together with the eigenvectors.
        """
        # The matrix to be evaluated is collected from the input.
        A = self.M
        Neigenval, Neigenvec = np.linalg.eig(A)
        # Sorting eigenvalues by size to simplify comparison.
        numpy_eigenval = np.sort(Neigenval)
        return numpy_eigenval, Neigenvec

#-------------------------------------------------------------------------
