# Importing necessary packages
from Jacobi_class import Eigenvalues as J
import unittest
import numpy as np

# Defining a test class:
class MyTest(unittest.TestCase):
    """
    The tests are run in the terminal using py.test.
    Execute:
    $ py.test Jacobi_tests.py
    Both tests successfully pass.
    """
    # Testing the function maxoffdiag from the Eigenvalues module.
    def test_maxoffdiag(self):
        # input 2x2 matrix, largest non-diagonal element is |-6|.
        A_in = np.array([[1, -6],[4, 5]])
        # Calling the Eigenvalues module with A_in as input matrix.
        i = J(A_in)
        # Extracting the output from the specified function.
        maxval, k, l = i.maxoffdiag(A_in)
        # Testing if the function sets the right element as the largest one.
        self.assertEqual(maxval, 6)

    # Testing the function jacobi which is dependent on both maxoffdiag and
    # the function rotate in the module. Testing that the module calculates
    # correct eigenvalues.
    def test_jacobi(self):
        # Simple 2x2 symmetric matrix with known Eigenvalues as input.
        A_in = np.array([[2.0, -1.0], [-1.0, 2.0]])
        # Calling the Eigenvalues module with the input matrix.
        i = J(A_in)
        # Computing the eigenvalues with Jacobi's method.
        eigval, eigvec, initer = i.Jacobi()
        # True eigenvalues.
        lmbda1 = 1.0
        lmbda2 = 3.0
        # Testing that the calculated eigenvalues are equal to the true
        # eigenvalues within a acceptable limit, 1e-12.
        self.assertAlmostEqual(eigval[0], lmbda1, places=12)
        self.assertAlmostEqual(eigval[1], lmbda2, places=12)
