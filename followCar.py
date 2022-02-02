import picar_4wd as fc
import time
import numpy as np
from collections import deque
import math
from enum import Enum

import grid_world

# -----> y
# |
# |
# V
# x

#0 -x
#1 -y
#2 +x
#3 +y

class direction(Enum):
    WEST:0
    SOUTH:1
    EAST:2
    NORTH:3
    

turn_time = 1.3  # time to turn 90 deg at 1 speed
avg_speed = 10 #cm/sec
step_size = 20 #cm

def turn_right(direction):
    fc.turn_right(1)
    time.sleep(turn_time)
    fc.stop()
    return (direction + 4 - 1) % 4

def turn_left():
    fc.turn_left(1)
    time.sleep(turn_time)
    fc.stop()

def step_forward(num_steps):
    pause_time = num_steps * step_size / avg_speed
    fc.forward(1)
    time.sleep(pause_time)
    fc.stop

turn_funcs = [turn_right(), turn_left()]


def followPath(path, stepSize):
    # assume the starting point is the first element of the path
    # and that the car is facing the y-axis
    current_node = path.pop()
    direction = direction.NORTH
    while len(path) != 0:
        next_node = path.pop()
        direction_of_motion = face_next_node(current_node, next_node, direction)



def face_next_node(current_node, next_node, current_direction):
    dx = next_node[0] - current_node[0]
    dy = next_node[0] - current_node[0]

    if math.abs(dx) > 0:
        tmp = current_direction + dx
    elif math.abs(dy) > 0:
        tmp = current_direction + dy + 1
    
    idx = (tmp // 2) % 2
    new_direction = turn_funcs[idx](current_direction)
    return new_direction
    
