from Jacobi_class import Eigenvalues as J
import unittest
import numpy as np


class MyTest(unittest.TestCase):

    def test_maxoffdiag(self):
        # 2x2 symmetric matrix
        i = J(2, 1, 1)
        A = np.array([[1, 4],[4, 5]])
        maxval, k, l = i.maxoffdiag(A)
        self.assertEqual(maxval, 4)


    def test_jacobi(self):
        # simple 2x2 symmetric matrix with known Eigenvalues
        i = J(2, 2.0, -1.0)
        A, R, initer = i.Jacobi()
        eig = np.diag(A)
        lmbda1 = 1.0
        lmbda2 = 3.0
        epsilon = 1e-12
        self.assertAlmostEqual(eig[1], lmbda1, places=12)
        self.assertAlmostEqual(eig[0], lmbda2, places=12)

    #def test_rotate(self):
