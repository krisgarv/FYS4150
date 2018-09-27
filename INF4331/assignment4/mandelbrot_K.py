import numpy as np
import matplotlib.pyplot as plt
import argparse
import time
import sys
from mandelbrot_1 import mandelbrot as M1
from mandelbrot_2 import mandelbrot as M2
from mandelbrot_3 import mandelbrot as M3
from mandelbrot_4 import mandelbrot as M4

#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(prog=sys.argv[0], \
        description='Plot of the fractal Mandelbrot',\
        epilog='This program plots the Mandelbrot set. The user must choose \
        one of the four script types to do the calculation. The Python script \
        is slow and time consuming while the vectorized Numpy, the \
        "just-in-time" Numba and the Cython scripts are more efficient.')
parser.add_argument('solver', type=str, help='Choose one of the following \
        solvers: python, numpy, numba, cython')
parser.add_argument('-filename', type=str, \
        help='Specify output image filename', default=None)
parser.add_argument('-xmin', type=float, default=-2.0,\
        help='Minimum value for x-axis. Default = -2.0')
parser.add_argument('-xmax', type=float, default=0.5,\
        help='Maximum value for x-axis. Default = 0.5')
parser.add_argument('-ymin', type=float, default=-1.25,\
        help='Minimum value for y-axis. Default = -1.25')
parser.add_argument('-ymax', type=float, default=1.25,\
        help='Maximum value for y-axis. Default = 1.25')
parser.add_argument('-mesh', type=int, default=1000, \
        help='Step size for fractal resolution. Default = 1000')
parser.add_argument('-maxiter', type=int, default=80, \
        help='Maximum number of iterations before pixel is set \
                inside Mandelbrot set. Default = 1000')
args = parser.parse_args()
#------------------------------------------------------------------------------
def calculate(M):
    t0 = time.time()
    image = M(args.xmin, args.xmax, args.ymin, args.ymax, args.mesh, \
            args.maxiter)
    t1 = time.time()
    Time = t1 - t0
    return image, Time

def view(image, Title):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=72)
    ax.imshow(image, cmap='flag', origin='lower',\
                interpolation='bicubic', \
                extent=[args.xmin, args.xmax, args.ymin, args.ymax])
    plt.xlabel('Max nr. of iterations: %i \n Step size: %i' \
                %(args.maxiter,args.mesh))
    plt.title(Title)
    if args.filename != None:
        fig.savefig(args.filename + '.png')
    plt.show()
#------------------------------------------------------------------------------

if args.solver == 'python':
    image, Time = calculate(M1)
    Title='Mandelbrot set derived by Pure Python'
    view(image, Title)
    print('Pure Python: Time used for maximum %i iterations and step size %i:\
            %.5gs' %(args.maxiter, args.mesh, Time))

elif args.solver == 'numpy' or 'Numpy':
    image, Time = calculate(M2)
    Title='Mandelbrot set derived by vectorized Numpy'
    view(image, Title)
    print('Vectorized Numpy: Time used for maximum %i iterations and step size %i:\
            %.5gs' %(args.maxiter, args.mesh, Time))

elif args.solver == 'numba' or 'Numba':
    image, Time = claculate(M3)
    Title='Mandelbrot set derived by Numbas "just-in-time"'
    view(image, Title)
    print('Numba: Time used for maximum %i iterations and step size %i:\
            %.5gs' %(args.maxiter, args.mesh, Time))

elif args.solver == 'cython' or 'Cython':
    image, Time = calculate(M4)
    Title='Mandelbrot set derived by Cython'
    view(image, Title)
    print('Cython: Time used for maximum %i iterations and step size %i:\
            %.5gs' %(args.maxiter, args.mesh, Time))

else:
    print('Bad usage: state "python Mandelbrot.py -h" for help.')



"""
    ax.text(args.xmin+.025, args.ymin+.025, Text, color='k', \
                fontsize=14, alpha=0.5)

solver=args.solver
filename=args.filename
xmin=args.xmin
xmax=args.xmax
ymin=args.ymin
ymax=args.ymax
h=args.mesh
maxiter=args.maxiter

#------------------------------------------------------------------------------

"""
