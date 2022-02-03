import time
from utils import *
import picar_4wd as fc
import us_module as us
from grid_world import grid_world

class autonomous_vehicle:

    def __init__(self):
        self.gw = grid_world(np.zeros((75,100), dtype=np.uint8), (0,0), (75,90))
        self.previousPointOnObject = None
        self.my_location = (0,0)
        self.my_direction = direction.NORTH
        self.us = us.us_module(step_size=5)

    def translate_car_coords_to_world_coords(self, x_car, y_car):
        rotation_angle = self.my_direction * -90
        x_c1, y_c1 = rotation_transform(rotation_angle, (x_car, y_car))
        x_gw = x_c1 + self.my_location[0]
        y_gw = y_c1 + self.my_location[1]
        return round(x_gw), round(y_gw)

    def is_point_in_world_bounds(self, x_gw,y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        if is_point_in_bounds((x_gw, y_gw), max_horizon_x, max_horizon_y):
            addDetectionToMap(x_gw, y_gw)
            previousPointOnObject
    
        
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
                x_gw, y_gw = self.translate_car_coords_to_world_coords(x_car, y_car)
                if self.is_point_in_world_bounds(x_gw,y_gw):
                    self.addDetectionToMap(x_car, y_car)
                    self.previousPointOnObject = (x,y)
                else:
                    self.previousPointOnObject = None
            else:
                # if no object is found then we are definitely not looking at the continuation of an object
                self.previousPointOnObject = None
        

    def addDetectionToMap(self, x_gw, y_gw):
        if self.isPointContinuationOfObject():
            self.interpolateBorder(x_gw, y_gw)
        markPointOnMap(x_gw,y_gw)

    def isPointContinuationOfObject(self):
        retval = self.previousPointOnObject is not None
        return retval
        
    def markPointOnMap(self,x_gw, y_gw):
        self.gw.world_map[int(x_gw)][int(y_gw)] = 1

    def interpolateBorder(self, x_gw, y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        coords = getInterpolationCoordinates(x_gw, y_gw, self.previousPointOnObject)
        for i in range(len(coords)):
            point = coords[i]
            if is_point_in_bounds(point, max_horizon_x, max_horizon_y):
                x = point[0]
                y = point[1]
                self.markPointOnMap(x, y)

    

    # def scan_step():
    #     self.us_current_angle -= us_step
    #     distance = fc.get_distance_at(us_current_angle)
    #     return distance
    
                
    # def reset_us():
    #     self.us_current_angle= 90
    #     fc.servo.set_angle(self.us_current_angle)
    #     time.sleep(0.1)

        
if __name__ == "__main__":
    a = autonomous_vehicle()
    pdb.set_trace()
    a.scan_horizon()
    dump_map(a.gw.world, filename="gw_out.txt")
    
