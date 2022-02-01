import picar_4wd as fc
import time
import numpy as np

turn_time=1.3 # time to turn 90 deg at 1 speed
def turn_right():
    fc.turn_right(1)
    time.sleep(turn_time)
    fc.stop()

def turn_left():
    fc.turn_left(1)
    time.sleep(turn_time)
    fc.stop()
    
def turn_left():
    fc.turn_left(1)
    time.sleep(turn_time)
    fc.stop()


avg_speed = 10 #cm/sec



world = np.array
