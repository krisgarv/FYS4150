import numpy as np
import sys
import matplotlib.pyplot as plt
import time

n = int(sys.argv[1])

a = -1.0
b= 2.0
c = -1.0
x = np.linspace(0, 1, n+2)
v = np.zeros_like(x)

#Creating the vectors:
a_vec		= np.zeros(n-1)
a_vec[:]	= a

b_vec		= np.zeros(n)
b_vec[:]	= b
b_tilde		= np.zeros(n)

c_vec 		= np.zeros(n-1)
c_vec[:] 	= c

d_vec		= np.zeros(n)
d_tilde		= np.zeros(n)
d_hat		= np.zeros(n)

b_tilde[0] = b_vec[0]

b_tilde[1] = b_vec[1] - c_vec[0]*a_vec[0]/b_tilde[0]

d_tilde[0] = d_vec[0]

d_tilde[1] = d_vec[1] - d_tilde[0]*a_vec[0]/b_vec[0]
"""
t0 = time.time()
for i in range(2, n+1):
	b_tilde[i] = b_vec[i] - c_vec[i-1]*a_vec[i-1]/b_tilde[i-1]
	d_tilde[i] = d_vec[i] - d_tilde[i-1]*a_vec[i-1]/b_tilde[i-1]

for i in range(n-1, -1, -1):
	d_hat[i] = d_tilde[i] - d_tilde[i+1]*c_vec[i]/b_tilde[i+1]

t1 = time.time()

print(t1-t0)
print(np.size(a_vec), np.size(a_tilde))
print(b_tilde)
"""
