import picar_4wd as fc
import time
import numpy as np
from collections import deque
import math
from enum import IntEnum
import pdb
import grid_world
import gw_driver

# -----> y
# |
# |
# V
# x

#0  NORTH (+y)
#1  WEST  (-x)
#2  SOUTH (-y)
#3  EAST  (+x)


# gw = gw_driver.driver()

class direction(IntEnum):
    NORTH=0
    WEST=1
    SOUTH=2
    EAST=3

turn_time = 1.3  # time to turn 90 deg at 1 speed
avg_speed = 10 #cm/sec
step_size = 5 #cm

def turn_right(current_direction):
    fc.turn_right(1)
    time.sleep(turn_time)
    fc.stop()
    return direction((current_direction + 4 - 1) % 4)

def turn_left(current_direction):
    fc.turn_left(1)
    time.sleep(turn_time)
    fc.stop()
    return direction((current_direction + 1) % 4)

turn_funcs = [turn_left, turn_right]


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
    pdb.set_trace()
    while len(path) != 0:
        next_node = path.pop()
        cur_direction = face_next_node(current_node, next_node, cur_direction)
        current_node = next_node
        # step_forward(1)

def get_turn_idx(current_node, next_node, current_direction):
    dx = next_node[0] - current_node[0]
    dy = next_node[1] - current_node[1]

    if abs(dx) > 0:
        if current_direction == direction.WEST or current_direction == direction.EAST:
            return
        tmp = current_direction + dx + 1
    elif abs(dy) > 0:
        if current_direction == direction.NORTH or current_direction == direction.SOUTH:
            return
        tmp = current_direction + dy
    else:
      return
    
    idx = (tmp // 2) % 2
    return idx

def face_next_node(current_node, next_node, current_direction):
    # dx = next_node[0] - current_node[0]
    # dy = next_node[1] - current_node[1]

    # if abs(dx) > 0:
    #     tmp = current_direction + dx
    # elif abs(dy) > 0:
    #     tmp = current_direction + dy + 1
    # else:
    #   return current_direction
    
    # idx = (tmp // 2) % 2
    idx = get_turn_idx(current_node, next_node, current_direction)
    if idx is None:
        return current_direction
    new_direction = turn_funcs[idx](current_direction)
    return new_direction


    
