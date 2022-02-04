import time
from utils import *
import picar_4wd as fc
import us_module as us
from grid_world import grid_world
import path_follow as pf
import sys

class autonomous_vehicle:

    def __init__(self, start=(25,0), end=(25,50), world_size=(50,50), step_size=1):
        if start[0] < 0  or start[0] >= world_size[0] or start[1] < 0 or start[1] >= world_size[1]:
            print("ERROR: start coordinate not in bounds")
            sys.exit(0)
            
            
        if end[0] < 0  or end[0] >= world_size[0] or end[1] < 0 or end[1] >= world_size[1]:
            print("ERROR: end coordinate not in bounds")
            sys.exit(0)
        
        self.step_size = step_size
        self.gw = grid_world(np.zeros(world_size, dtype=np.uint8), start, end)
        self.previousPointOnObject = None
        self.my_location = start
        self.my_direction = direction.NORTH
        self.end = end
        self.us = us.us_module(step_size=5, scale = 1/step_size) # angle step, not grid cell length
        self.pf = pf.navigation_module(step_size = step_size)

    def translate_car_coords_to_world_coords(self, x_car, y_car):
        rotation_angle = self.my_direction * -90
        x_c1, y_c1 = rotation_transform(rotation_angle, (x_car, y_car))
        x_gw = x_c1 + self.my_location[0]
        y_gw = y_c1 + self.my_location[1]
        return x_gw, y_gw

    def is_point_in_world_bounds(self, x_gw,y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        return is_point_in_bounds((x_gw, y_gw), max_horizon_x, max_horizon_y)
            # self.addDetectionToMap(x_gw, y_gw)
            # previousPointOnObject
    
        
    def scan_horizon(self):
        # self.reset_us()
        # global previousPointOnObject
        # global max_horizonx,min_horizon,max_horizony
        scan_results = self.us.scan_horizon()
        for i in range(len(scan_results)):
            res = scan_results[i]
            distance = res[0]
            angle = res[1]
            if distance > 0:
                # if an object is detected, get the location of an object with respect to the grid world
                # and mark it on the map
                x_car, y_car = convertToCartesian(angle, distance)
                x_gw_float, y_gw_float = self.translate_car_coords_to_world_coords(x_car, y_car)
                if self.is_point_in_world_bounds(x_gw_float, y_gw_float):
                    self.addDetectionToMap(x_gw_float, y_gw_float)
                    self.previousPointOnObject = (x_gw_float,y_gw_float)
                else:
                    self.previousPointOnObject = None
            else:
                # if no object is found then we are definitely not looking at the continuation of an object
                self.previousPointOnObject = None
        

    def addDetectionToMap(self, x_gw_float, y_gw_float):
        # if self.isPointContinuationOfObject():
        #     self.interpolateBorder(x_gw_float, y_gw_float)
        self.markPointOnMap(round(x_gw_float), round(y_gw_float))

    def isPointContinuationOfObject(self):
        retval = self.previousPointOnObject is not None
        return retval
        
    def markPointOnMap(self,x_gw, y_gw, identifier=1):
        self.gw.world[int(x_gw)][int(y_gw)] = identifier

    def interpolateBorder(self, x_gw, y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        coords = getInterpolationCoordinates(x_gw, y_gw, self.previousPointOnObject)
        # coords are floating-point values
        for i in range(len(coords)):
            point = coords[i]
            if is_point_in_bounds(point, max_horizon_x, max_horizon_y):
                x = round(point[0])
                y = round(point[1])
                self.markPointOnMap(x, y)

            
    def main_loop(self):
        while self.my_location != self.end:
            self.scan_horizon()
            dump_map(a.gw.world)
            self.gw.run_a_star()
            dump_map(a.gw.world)
            self.my_location, self.my_direction = self.pf.follow_path_for_n(self.gw.path_to_dest, 5)
    

    # def scan_step():
    #     self.us_current_angle -= us_step
    #     distance = fc.get_distance_at(us_current_angle)
    #     return distance
    
                
    # def reset_us():
    #     self.us_current_angle= 90
    #     fc.servo.set_angle(self.us_current_angle)
    #     time.sleep(0.1)

        
if __name__ == "__main__":
    a = autonomous_vehicle(step_size = 5, world_size=(20,15), start=(14,0), end=(5,0))
    a.main_loop()
    # a.scan_horizon()
    # dump_map(a.gw.world)
    # a.gw.run_a_star()
    # dump_map(a.gw.world)
    # a.pf.followPath(a.gw.path_to_dest)
    
    
    
