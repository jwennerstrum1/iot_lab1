import sys
import numpy as np
import re
import pdb

# filename = 'tmpFile.txt'
# filename = 'block_left.txt'

def readArrayFromFile(filename):
    # pdb.set_trace()
    f = open(filename, 'r')
    line = f.readline()
    cleanedString = clean_string(line)
    world = str2arr(cleanedString)
    dim_y = len(world)
    dim_x = 1
    line = f.readline()
    while line != '' and line != '\n':
      # pdb.set_trace()
      cleanedString = clean_string(line)
      array_column = str2arr(cleanedString)
      # pdb.set_trace()
      world = np.concatenate((world, array_column), 0)
      dim_x+=1
      line = f.readline()
    f.close()
    # pdb.set_trace()
    world = np.reshape(world, (dim_x, dim_y))
    return world

def str2arr(string):
    array_column = np.fromstring(string, dtype=np.uint8, sep=' ')
    return array_column

    
def clean_string(line):
    loc = re.search('[01]',line)
    start = loc.start()
    end = line.find(']')
    line = line[start:end]
    # line = ','.join(line.split(' '))
    return line

