import numpy as np
# from picar_4wd.servo import Servo
# from picar_4wd.pwm import PWM
import picar_4wd as fc
import time
import math
import sys, getopt


np.set_printoptions(threshold=np.inf, linewidth=np.inf)

world_map = np.zeros((100,100), np.uint8)
x_offset = int(len(world_map)/2)
max_horizonx = x_offset
min_horizonx = -1 * x_offset
max_horizony = len(world_map[0])
us_step = 5
us_current_angle = -95 # start looking to the left
previousPointOnObject = None
file_name = 'world_map'

def reset_us():
    global us_current_angle
    us_current_angle= 90
    fc.servo.set_angle(us_current_angle)
    time.sleep(0.1)

def convertToCartesian(degrees, distance):
    # converts degrees and distance to x,y coordinates
    y_1 = distance * np.around(math.cos(math.radians(degrees)), 2)
    x_1 = distance * np.around(math.sin(math.radians(degrees)), 2) * -1
    
    return x_1, y_1

def scan_horizon():
    reset_us()
    global us_current_angle, previousPointOnObject
    global max_horizonx,min_horizon,max_horizony
    while us_current_angle > -90:
        distance = scan_step()
        if distance > 0:
            # if an object is detected, mark the map
            x, y = convertToCartesian(us_current_angle, distance)
            if round(x) > min_horizonx and round(x) < max_horizonx and round(y) < max_horizony:
               addDetectionToMap(x, y)
               previousPointOnObject = (x,y)
        else:
            # if no object is found then we are definitely not looking at the continuation of an object
            previousPointOnObject = None

def addDetectionToMap(x,y):
    global world_map
    if lookingAtContinuingObject():
        interpolateBorder(x, y)
    markPointOnMap(x,y)
        
def markPointOnMap(x,y):
    global world_map, x_offset
    world_map[round(x) + x_offset][round(y)] = 1

def lookingAtContinuingObject():
    global previousPointOnObject
    return previousPointOnObject is not None

def interpolateBorder(x,y):
    global world_map, previousPointOnObject
    coords = getInterpolationCoordinates(x, y, previousPointOnObject)
    for i in range(len(coords)):
        x1 = coords[i][0]
        y1 = coords[i][1]
        markPointOnMap(x1, y1)

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
            coords.append((x_t, y_t))
            y_t += m
    else:
        if (m >= 0):
            iter = range(round(y1), round(y2))
        else:
            iter = reversed(range(round(y2+1),round(y1+1)))
        x_t = x1
        for y_t in iter:
            print(y_t)
            coords.append((x_t, y_t))
            x_t += abs(1/m)
    coords.append((x2,y2))
    return coords
            
    
def scan_step():
    global us_current_angle, us_step
    us_current_angle -= us_step
    distance = fc.get_distance_at(us_current_angle)
    return distance

def printMap():
    global world_map
    f = open( file_name + '.txt', 'w')
    f.write(np.array_str(world_map))
    f.close


def main(argv):
    global world_map, file_name
    try:
        opts, args = getopt.getopt(argv,"ho:",["ofile="])
    except getopt.GetoptError:
        print('mapRoom.py -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('mapRoom.py -o <outputfile>')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            file_name = arg

    scan_horizon()
    printMap()
    return 

if __name__ == "__main__":
    main(sys.argv[1:])


