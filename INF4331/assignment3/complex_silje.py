import numpy as np

class Complex(object):

# Class that calculates addition, subtraction, multiplication of complex numbers. It also calculates the complex conjugate and the modulus.

	def __init__(self, a, b):
	# Initialize the complex number, where a is the real number and b the imaginary number.
		self.a = a
		self.b = b

	# Assignment 3.3:

	def conjugate(self):
	# Calculate the complex conjugate.
		return Complex(self.a, -self.b)

	def modulus(self):
	# Calculate the modulus.
		return np.sqrt(self.a**2 + self.b**2)

	def __add__(self, other):
	# Add our complex number by eighter a complex number made by this Class, a float/integer or by a complex number by Python.
		if isinstance(other, Complex):
			return Complex(self.a + other.a, self.b + other.b)
		elif (type(other) is int or type(other) is float):
			return Complex(self.a + other, self.b)
		elif type(other) is complex:
			return Complex(self.a + other.real, self.b + other.imag) 
		else:
			return NotImplemented

	def __sub__(self, other): 
	# Subtraction bewteen our complex number and eighter a complex number made by this Class, a float/integer or by a complex number by Python.
		if isinstance(other, Complex):
			return Complex(self.a - other.a, self.b - other.b)
		elif (type(other) is int or type(other) is float): 
			return Complex(self.a - other, self.b)
		elif type(other) is complex:
			return Complex(self.a - other.real, self.b - other.imag) 
		else:
			return NotImplemented

	def __mul__(self, other):
	# Multiplication between our complex number and eighter a complex number made by this Class, a float/integer or by a complex number by Python
		if isinstance(other, Complex):
			return Complex(self.a*other.a - self.b*other.b, self.a*other.b + self.b*other.a)
		elif (type(other) is int or type(other) is float):
			return Complex(other*self.a, other*self.b)
		elif type(other) is complex:
			return Complex(self.a*other.real - self.b*other.imag, self.a*other.imag + self.b*other.real)
		else:
			return NotImplemented
	
	def __eq__(self, other):
	# So we can write == to compare equality
		return self.a == other.a and self.b == other.b

	def __str__(self):
	# What is printed when typing print(insert something here). Also checking if the complex number uses integers or floats.
		if (isinstance(self.a, float) or isinstance(self.b, float)):
			if self.b < 0:
				return "%.2f%.2fj" % (round(self.a,2), round(self.b,2))
			else:
				return "%.2f+%.2fj" % (round(self.a,2), round(self.b,2))
		else:
			if self.b < 0:
				return "%d%dj" % (self.a, self.b)
			else:
				return "%d+%dj" % (self.a, self.b)

	# Assignment 3.4:

	def __radd__(self, other):
	# To be able to do addition from the left hand side of the complex number made by this Class.
		return self.__add__(other)

	def __rsub__(self, other):
	# To be able to do subtraction from the left hand side of the complex number made by this Class.
		if (type(other) is int or type(other) is float):
			return Complex(other - self.a, -self.b)
		elif type(other) is complex:
			return Complex(other.real - self.a, other.imag - self.b)
		else:
			return NotImplemented

	def __rmul__(self, other):
	# To be able to do multiplication from the left hand side of the complex number made by this Class.
		return self.__mul__(other)	

