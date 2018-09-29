import matplotlib.pyplot as plt
import numpy as np

#Number of iterations:
y = [1, 9, 6, 31, 35, 71, 92, 120, 137, 198, 208, 269, 317, 365, 474, 655, 1059, 1543, 2762, 4373, 17601]
#Corresponding N:
N = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 20, 25, 30, 40, 50, 100]

y_arr = np.array(y)
N_arr = np.array(N)

#Plotting the function g(x) = 1.75x^2
x = np.linspace(1,100, 100)
def g(x):
    return 1.75*x**2

plt.plot(N_arr, y_arr)
plt.plot(x, g(x))
plt.title("Iterations needed to get a diagonal matrix")
plt.xlabel("N for a NxN matrix")
plt.ylabel("Number of iterations")
plt.legend(["Our iterations", "$f(x) = 1.7x^2$"])
plt.show()
