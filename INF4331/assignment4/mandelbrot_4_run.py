import numpy
from mandelbrot_4 import find_total_grid, find_numbers
import matplotlib.pyplot as plt

#When running the name of the program in the terminal, this is run:
import time
t0 = time.time()
grid = find_total_grid(x_min=-2.0, x_max=1.0, y_min=-1.3, y_max=1.3, nr_of_val=1000, max_iterations=100, limit=2.0)
#print(np.max(grid))
t1 = time.time()
fig, ax = plt.subplots(figsize=(10, 10), dpi=72)
ax.imshow(grid, cmap='RdGy' , origin='lower', interpolation='bicubic', extent=[-2.0, 1.0, 1.3, -1.3])
plt.gca().invert_yaxis()
plt.show()
print("Runtime:", t1-t0)
