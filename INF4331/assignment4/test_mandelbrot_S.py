""" Unit tests run by using pytest. Imported compute_mandelbrot from the module mandelbrot """

import numpy as np
from mandelbrot_solver.mandelbrot import compute_mandelbrot
import pytest

def test_outside():
    #Fails if no Exception:
    with pytest.raises(Exception):
        compute_mandelbrot(x_min=3.0, x_max=4.0, y_min=3.0, y_max=4.0, columns=10, rows=10)

def test_inside():
    grid = compute_mandelbrot(x_min=-0.5, x_max=0.5, y_min=-0.5, y_max=0.5, columns=10, rows=10)
    # Testing if the iteration-matrix (named grid) does not only consist of 1's.
    assert (grid != 1).all()
