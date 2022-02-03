from mapRoom import getInterpolationCoordinates, convertToCartesian
import numpy as np


def test_getInterpolationCoordinates_1():
    # negative, large slope, reversed values
    coords = getInterpolationCoordinates(4, -10, (3,-6))
    assert coords == [(3, -6), (3.25, -7), (3.5, -8), (3.75, -9), (4, -10)]

def test_getInterpolationCoordinates_2():
    # positive, small slope
    coords = getInterpolationCoordinates(1, 1, (5, 3))
    assert coords == [(1, 1), (2, 1.5), (3, 2.0), (4, 2.5), (5, 3)]

def test_getInterpolationCoordinates_3():
    # negative, small slope
    coords = getInterpolationCoordinates(4, 5, (8, 3))
    assert coords == [(4, 5), (5, 4.5), (6, 4.0), (7, 3.5), (8, 3)]


def test_convertToCartesian_1():
    x, y = convertToCartesian(-90,1)
    assert np.around(x, 2) == 1
    assert np.around(y, 2) == 0

def test_convertToCartesian_2():
    x, y = convertToCartesian(0,1)
    assert np.around(x, 2) == 0
    assert np.around(y, 2) == 1

def test_convertToCartesian_3():
    x, y = convertToCartesian(90, 1)
    assert np.around(x,2) == -1
    assert np.around(y,2) == 0


    

    
