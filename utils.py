import sys
import numpy as np
import re
import pdb
import math
from enum import IntEnum

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

def convertToCartesian(degrees, distance):
    # converts degrees and distance to x,y coordinates
    y_1 = distance * np.around(math.cos(math.radians(degrees)), 2)
    x_1 = distance * np.around(math.sin(math.radians(degrees)), 2) * -1
    return x_1, y_1


# -----> y
# |
# |
# V
# x
#0  NORTH (+y)
#1  WEST  (-x)
#2  SOUTH (-y)
#3  EAST  (+x)
class direction(IntEnum):
    NORTH=0
    WEST=1
    SOUTH=2
    EAST=3


def rotation_transform(theta, point):
    rotation_matrix = np.array([[math.cos(theta * math.pi/180), -1 * math.sin(theta * math.pi/180)], [math.sin(theta * math.pi/180), math.cos(theta * math.pi/180)]], dtype=np.float)
    to_multiply = np.array([[point[0]], [point[1]]], dtype=np.float)
    res = rotation_matrix @ to_multiply
    return np.round(res[0][0], 2), np.round(res[1][0], 2)




def getInterpolationCoordinates(x, y, previousPoint):
    x_prev = previousPoint[0]
    y_prev = previousPoint[1]
    
    if (x_prev < x ):
      x1 = x_prev
      y1 = y_prev
      x2 = x
      y2 = y
    else:
      x1 = x
      y1 = y
      x2 = x_prev
      y2 = y_prev

    dx = x2 - x1
    dy = y2 - y1
    m = dy / dx
    coords = []
    if abs(m) < 1:
        y_t = y1
        for x_t in range(round(x1), round(x2)):
            # buffer logic
            for i in range(3):
                coords.append((x_t, y_t - i))
                coords.append((x_t, y_t + i))
            coords.append((x_t, y_t))
            y_t += m
    else:
        if (m >= 0):
            iter = range(round(y1), round(y2))
        else:
            iter = reversed(range(round(y2+1),round(y1+1)))
        x_t = x1
        for y_t in iter:
            # buffer logic
            for i in range(3):
                coords.append((x_t - i, y_t))
                coords.append((x_t + i, y_t))
            coords.append((x_t, y_t))
            x_t += abs(1/m)
    coords.append((x2,y2))
    return coords



def is_point_in_bounds(point, x_max=0, y_max=0):
    x = point[0]
    y = point[1]
    retval = x >= 0 and x < x_max and y >= 0 and y < y_max
    return retval
    
    
def dump_map(array, filename="grid_world_dump.txt"):
    print_options = np.get_printoptions()
    threshold_old = print_options['threshold']
    linewidth_old = print_options['linewidth']
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    f = open(filename, 'w')
    f.write(np.array_str(array))
    np.set_printoptions(threshold=threshold_old, linewidth=linewidth_old)
    f.close()
    
