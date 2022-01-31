import utils
import numpy as np

def read_array():
    filename = 'test_map.txt'
    a=  utils.readArrayFromFile(filename)
    b = np.zeros((4,5), np.uint8)
    for i in range(3):
        b[0][i] = 1
    assert a == b
    
