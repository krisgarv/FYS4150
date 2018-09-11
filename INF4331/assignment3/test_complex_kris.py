from complex import Complex

# Assignment 3.2

#Addition test
def test_add():
    a = Complex(1, 2)
    b = Complex(2, 3)
    assert a + b == Complex(3, 5)

#Subtraction test
def test_sub():
    a = Complex(5, 4)
    b = Complex(3, 2)
    assert a - b == Complex(2, 2)

#Multiplication test
def test_mul():
    a = Complex(2, 1)
    b = Complex(3, 2)
    assert a * b == Complex(4, 7)

#Division test
def test_div():
    a = Complex(1, 3)
    b = Complex(1, 1)
    assert a/b == Complex(2, 1)

#Negative test
def test_neg():
    a = Complex(2, 1)
    assert -a == Complex(-2, -1)

#Conjugate test
def test_conjugate():
    a = Complex(3, 2)
    assert a.conjugate() == Complex(3, -2)

#Modulus test
def test_modulus():
    a = Complex(3, -4)
    assert a.modulus() == 5

#Equality test
def test_eq():
    a = Complex(1, 3)
    assert Complex(1, 3).__eq__(self, a)

# Assignment 3.4

# Test addition with Python's comlex and real numbers
def test_radd():
    a = 2
    b = Complex(2, 3)
    c = complex(2, 2)

    assert a + b + c == Complex(6, 5)

# Test subtraction with Python's comlex and real numbers
def test_rsub():
    a = 6
    a = Complex(2, 3)
    b = complex(2, 2)
    assert a - b - c == Complex(2, -5)

# Test multiplication with Python's comlex and real numbers
def test_rmul():
    a = 2
    b = Complex(3, 4)
    assert a*b == Complex(6, 8)

def test_rdiv():
    a = Complex(1, 3)
    b = Complex(1, 1)
    assert a/b == Complex(2, 1)
