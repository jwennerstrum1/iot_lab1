import picar_4wd as fc
import time
import numpy as np
from collections import deque
import math
from enum import IntEnum

import grid_world
import gw_driver

# -----> y
# |
# |
# V
# x

#0 -x
#1 -y
#2 +x
#3 +y


gw = gw_driver.driver()

class direction(IntEnum):
    WEST=0
    SOUTH=1
    EAST=2
    NORTH=3
    

turn_time = 1.3  # time to turn 90 deg at 1 speed
avg_speed = 10 #cm/sec
step_size = 20 #cm

def turn_right(current_direction):
    fc.turn_right(1)
    time.sleep(turn_time)
    fc.stop()
    return direction((current_direction + 1) % 4)

def turn_left(current_direction):
    fc.turn_left(1)
    time.sleep(turn_time)
    fc.stop()
    return direction((current_direction + 4 - 1) % 4)

turn_funcs = [turn_right, turn_left]


def step_forward(num_steps):
    pause_time = num_steps * step_size / avg_speed
    fc.forward(1)
    time.sleep(pause_time)
    fc.stop()


def followPath(path, stepSize):
    # assume the starting point is the first element of the path
    # and that the car is facing the y-axis
    current_node = path.pop()
    cur_direction = direction.NORTH
    while len(path) != 0:
        next_node = path.pop()
        cur_direction = face_next_node(current_node, next_node, cur_direction)
        step_forward(1)



def face_next_node(current_node, next_node, current_direction):
    dx = next_node[0] - current_node[0]
    dy = next_node[1] - current_node[1]

    if abs(dx) > 0:
        tmp = current_direction + dx
    elif abs(dy) > 0:
        tmp = current_direction + dy + 1
    
    idx = (tmp // 2) % 2
    new_direction = turn_funcs[idx](current_direction)
    return new_direction
    
