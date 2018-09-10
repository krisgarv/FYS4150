from complex import Complex

#Assignment 3.2:

def test_add():
	""" Verifying that adding two complex numbers returns what it’s supposed to """
	complexnr1 = Complex(2, 2)
	complexnr2 = Complex(1, 4)
	assert complexnr1 + complexnr2 == Complex(3, 6)

def test_sub():
	""" Verifying that subtracting two complex numbers returns what it’s supposed to """
	complexnr1 = Complex(1, 1)
	complexnr2 = Complex(2, 2)
	assert complexnr1 - complexnr2 == Complex(-1, -1)

def test_mul():
	""" Verifying that multiplication between two complex numbers returns what it's supposed to """
	complexnr1 = Complex(1, 1)
	complexnr2 = Complex(2, 2)
	assert complexnr1*complexnr2 == Complex(0, 4)

def test_conjugate():
	""" Checking that the conjugate method works """
	assert Complex(1,3).conjugate() == Complex(1,-3)

def test_modulus():
	""" Checking that the modulus method works """
	assert Complex(3,-4).modulus() == 5

def test_eq():
	""" Checking that the eq method works """
	complex_b = Complex(3, -4)
	assert Complex(3, -4).__eq__(self, complex_b)

#Assignment 3.4:

def test_rmul():
	""" Check if the __rmul__ works """
	complexnr = 5*Complex(1, -2)
	assert complexnr == Complex(5, -10)

def test_radd():
	""" Check if the __radd__ works """
	complexnr = 4 + Complex(2, 2) + (1 - 1j)
	assert complexnr == Complex(7, 1)

def test_rsub():
	""" Check if the __rsub__ works """
	complexnr = 2 - Complex(4, 5) - (9 + 2j)
	assert complexnr == Complex(-11, -7)
 
if __name__ == "__main__":
	test_add()
	test_sub()
	test_mul()
	test_conjugate()
	test_modulus()
	test_radd()
	test_rsub()
	test_rmul()



