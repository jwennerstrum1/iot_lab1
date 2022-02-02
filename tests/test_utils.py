import utils
import numpy as np

def test_read_array(resource_path_root):
    filename = 'test_map.txt'
    a=  utils.readArrayFromFile(str(resource_path_root) + "/" + filename)
    b = np.zeros((4,5), np.uint8)
    for i in range(3):
        b[i][2] = 1
    assert (a == b).all()
    
