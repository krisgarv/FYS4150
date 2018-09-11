import numpy as np

class Complex:
    """
    Add docstring
    """

    def __init__(self, a, b):
        # Initialize a complex number where a is real, b is imaginary
        self.a = a
        self.b = b

    # Assignment 3.3:

    def conjugate(self):
    # Calculating the Complex conjugate:
        return Complex(self.a, -self.b)

    def modulus(self):
    # Calculating the modulus:
        return np.sqrt(self.a**2 + self.b**2)

    def __add__(self, other):
    # Addition between Complex number from Class Complex and
    # < another complex number from Class Complex >,
    # < complex number from Pythons complex() > or
    # < a float or integer >:
        if isinstance(other, Complex):
            return Complex(self.a + other.a, self.b + other.b)
        elif type(other) is complex:
            return Complex(self.a + other.real, self.b + other.imag)
        elif type(other) is int or type(other) is float:
            return Complex(self.a + other, self.b)
        else:
            return NotImplemented

    def __sub__(self, other):
    # Subtraction between Complex number from Class Complex and
    # < another complex number from Class Complex >,
    # < complex number from Pythons complex() > or
    # < a float or integer >:
        if isinstance(other, Complex):
            return Complex(self.a - other.a, self.b - other.b)
        elif type(other) is complex:
            return Complex(self.a - other.real, self.b - other.imag)
        elif type(other) is int or type(other) is float:
            return Complex(self.a - other, self.b)
        else:
            return NotImplemented

    def __mul__(self, other):
    # Multiplication between Complex number from Class Complex and
    # < another complex number from Class Complex >,
    # < complex number from Pythons complex() > or
    # < a float or integer >:
        if isinstance(other, Complex):
            return Complex(self.a*other.a - self.b*other.b, \
            self.a*other.b + self.b*other.a)
        elif type(other) is complex:
            return Complex(self.a*other.real - self.b*other.imag, \
            self.a*other.imag + self.b*other.real)
        elif type(other) is int or type(other) is float:
            return Complex(other*self.a, other*self.b)
        else:
            return NotImplemented

    def __div__(self, other):
    # Division of a Complex number from Class Complex with
    # < another complex number from Class Complex >,
    # < complex number from Pythons complex() > or
    # < a float or integer >:
        if isinstance(other, Complex):
            r = float(other.a**2 + other.b**2)
            return Complex((self.a*other.a + self.b*other.b)/r, \
                            (self.b*other.a + self.a*other.b)/r)
        elif type(other) is complex:
            r = float(other.real**2 + other.imag**2)
            return Complex((self.a*other.real + self.b*other.imag)/r, \
                            (self.b*other.real + self.a*other.imag)/r)
        elif type(other) is int or type(other) is float:
            r = float(other)
            return Complex(self.a/r, self.b/r)
        else:
            NotImplemented

    def __neg__(self):
    # Allows the user to write '-c', where c is a Complex number
    # from this Class.
        return Complex(-self.a, -self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
    # Output when printing complex numbers defined by Complex(a, b).
        # Rounding off floating numbers.
        if (isinstance(self.a, float) or isinstance(self.b, float)):
            # Avoid printing 'a+-bi'
            if self.b < 0:
                return "%.2f%.2fi" % (round(self.a), round(self.b))
            else:
                return "%.2f+%.2fi" % (round(self.a), round(self.b))
        else:
            # Avoid printing 'a+-bi'
            if self.b < 0:
                return "%d%di" % (self.a, self.b)
            else:
                return "%d+%di" % (self.a, self.b)

    # Assignment 3.4:

    # Addition from left of Complex number made by this Class.
    def __radd__(self, other):
        return self.__add__(other)

    # Subtraction from left of Complex number made by this Class.
    def __rsub__(self, other):
        if (type(other) is int or type(other) is float):
            return Complex(other - self.a, -self.b)
        elif type(other) is complex:
            return Complex(other.real - self.a, other.imag - self.b)
        else:
            return NotImplemented

    # Multiplication from left of Complex number made by this Class.
    def __rmul__(self, other):
        return self.__mul__(other)

    # Division of a python complex or real with a Complex number
    # made by this Class.
    def __rdiv__(self, other):
        return self.__div__(other)
