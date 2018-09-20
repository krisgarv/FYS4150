import Jacobi_class_K as J
import unittest

class MyTest(unittest.TestCase):

    def test_maxoffdiag(self):
        # 2x2 symmetric matrix
        A = np.array([[1, 4],[4, 5]])
        N = 3
        maxval, k, l = J.maxoffdiag(A)
        self.assertEqual(maxval, 4)


    def test_jacobi(self):
        # simple 2x2 symmetric matrix with known Eigenvalues
        A, R, initer = J.Jacobi(2, 2, -1)
        eig = np.diag(A)
        lmbda1 = 1.0
        lmbda2 = 3.0
        epsilon = 1e-12
        assert eig[1]-epsilon < lmbda1 < eig[1]+epsilon
        assert eig[0]-epsilon < lmbda2 < eig[0]+epsilon
        #self.assertEqual(eig[1], lmbda1)
        #self.assertEqual(eig[0], lmbda2)
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
