import time
import utils
import picar_4wd as fc
import us_module as us
from grid_world import grid_world
import path_follow as pf
import sys
import pdb
import numpy as np
import cam_module

class autonomous_vehicle:
    # scale_factor = the size of each grid cell in the grid world (in cm)
    def __init__(self, start=(25,0), end=(8,0), world_size=(50,50), scale_factor=5, starting_direction=utils.direction.NORTH, turn_time=1.3):
        if start[0] < 0  or start[0] >= world_size[0] or start[1] < 0 or start[1] >= world_size[1]:
            print("ERROR: start coordinate not in bounds")
            sys.exit(0)
            
            
        if end[0] < 0  or end[0] >= world_size[0] or end[1] < 0 or end[1] >= world_size[1]:
            print("ERROR: end coordinate not in bounds")
            sys.exit(0)
        
        self.scale_factor = scale_factor
        self.gw = grid_world(np.zeros(world_size, dtype=np.uint8), start, end)
        self.previousPointOnObject = None
        self.my_location = start
        self.my_direction = starting_direction
        self.end = end
        self.us = us.us_module(step_size=5, scale = 1/scale_factor) # angle step, not grid cell length
        self.pf = pf.navigation_module(step_size = scale_factor, direction=starting_direction, turn_time=turn_time)
        self.scan_count=0
        self.steps_after_stop_sign = np.inf
        self.camera = cam_module.camera()

    def translate_car_coords_to_world_coords(self, x_car, y_car):
        rotation_angle = ((self.my_direction + 1) % 4) * 90
        x_c1, y_c1 = utils.rotation_transform(rotation_angle, (x_car, y_car))
        x_gw = x_c1 + self.my_location[0]
        y_gw = y_c1 + self.my_location[1]
        return x_gw, y_gw

    def translate_camera_coords_to_car(self, x_cam, y_cam):
        x_car = x_cam + 10.16 * 1/self.scale_factor
        y_car = y_cam
        return x_car, y_car

    def is_point_in_world_bounds(self, x_gw,y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        return utils.is_point_in_bounds((x_gw, y_gw), max_horizon_x, max_horizon_y)
        
    def scan_horizon(self):
        self.scan_count += 1
        scan_results = self.us.scan_horizon()
        for i in range(len(scan_results)):
            res = scan_results[i]
            distance = res[0]
            angle = res[1]
            if distance > 0:
                # if an object is detected, get the location of an object with respect to the grid world
                # and mark it on the map
                x_cam, y_cam = utils.convertToCartesian(angle, distance)
                x_car, y_car = self.translate_camera_coords_to_car(x_cam, y_cam)
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
        if self.isPointContinuationOfObject(x_gw_float, y_gw_float):
            self.interpolateBorder(x_gw_float, y_gw_float)
        self.markPointOnMap(round(x_gw_float), round(y_gw_float), identifier=self.scan_count)

    def isPointContinuationOfObject(self, x_gw_float, y_gw_float):
        if self.previousPointOnObject is not None:
            dist_to_last_point = utils.linear_distance((x_gw_float, y_gw_float), self.previousPointOnObject)
            if dist_to_last_point > 2:
                # distance between objects must be greater than 2*scaling_factor cm for this
                # detection to be a considered a continuation of an object
                return True
        return False
        
    def markPointOnMap(self,x_gw, y_gw, identifier=1):
        self.gw.world[int(x_gw)][int(y_gw)] = identifier

    def interpolateBorder(self, x_gw, y_gw):
        max_horizon_x = self.gw.get_x_length()
        max_horizon_y = self.gw.get_y_length()
        coords = utils.getInterpolationCoordinates(x_gw, y_gw, self.previousPointOnObject)
        # coords are floating-point values
        for i in range(len(coords)):
            point = coords[i]
            if utils.is_point_in_bounds(point, max_horizon_x, max_horizon_y):
                x = round(point[0])
                y = round(point[1])
                self.markPointOnMap(x, y, identifier=self.scan_count)

    def follow_path(self, path_list, n=6):
        count = 0
        pedestrian_spotted = False
        while len(path_list) != 0 and count < n:
            pedestrian_in_view, stop_sign_in_view = self.camera.detect_obstacles()
            if (pedestrian_in_view):
                print("Pedestrian detected")
                distance_to_pedestrian = self.get_distance_to_next_barrier()
                if distance_to_pedestrian < 15:
                    pedestrian_spotted = True
                    time.sleep(1)
                    # wait a second and continue scanning until they are gone
                    continue
            elif pedestrian_spotted:
                print("Pedestrian gone - proceeding")
                pedestrian_spotted = False
                # if a pedestrian was spotted but has left view,
                # remove any barriers in the gridworld that were due to
                # the pedestrian since they are no longer there.
                # then break out of navigation loop to trigger
                # a rescan of the environment
                self.clear_pedestrian_barrier()
                break
                
    
            if stop_sign_in_view and self.steps_after_stop_sign > 20:
                print("Stop Sign detected")
                distance_to_stop_sign = self.get_distance_to_next_barrier()
                if distance_to_stop_sign < 15:
                    print("Stopping at stop sign")
                    # stop at sighgt of stop sign for 2 seconds if a stop
                    # sign is in view and it is close to you
                    # don't stop if it sees the stop sign within 10 steps
                    # after seeing another stop sign.  This is likely going to
                    # be the same stop sign
                    time.sleep(5)
                    self.steps_after_stop_sign = 0
                else:
                    print("Already stopped at stop sign")
                
            next_node = path_list.pop()
            self.my_direction, self.my_location = self.pf.move_to_next_coord(next_node)
            self.steps_after_stop_sign += 1
            count += 1


    def clear_pedestrian_barrier(self):
        self.gw.remove_barriers_in_path(self.my_location, self.my_direction)
            
    def get_distance_to_next_barrier(self):
        distance_to_barrier = self.gw.get_distance_to_closest_barrier(self.my_location, self.my_direction)
        return distance_to_barrier
        
            
    def main_loop(self):
        self.pf.current_node = self.my_location
        
        count = 1
        while self.my_location != self.end:
            # mark my location
            self.markPointOnMap(self.my_location[0], self.my_location[1], identifier=255)
            
            # scan 
            self.scan_horizon()
            utils.dump_map(self.gw.world, filename=("dump_world_" + str(count)  + "_scan.txt"))

            # path plan
            self.gw.run_a_star()
            self.markPointOnMap(self.my_location[0], self.my_location[1], identifier=255)
            utils.dump_map(self.gw.world, filename=("dump_world_" + str(count)  + "_astar.txt"))

            # path execution
            # clear current location on map before moving point
            self.markPointOnMap(self.my_location[0], self.my_location[1], identifier=0)
            self.follow_path(self.gw.path_to_dest, n=6) # follow path for n steps

            # prepare for next iteratio
            self.gw.reset()
            self.gw.set_start(self.my_location)
            count += 1
    
        
if __name__ == "__main__":
    # a = autonomous_vehicle(scale_factor = 5, world_size=(20,15), start=(14,0), end=(5,0))
    # a = autonomous_vehicle(world_size=(50,50), start=(25,2), end=(8,2), scale_factor=5, starting_direction=utils.direction.NORTH, turn_time=1.25) # WESTWARD
    # a = autonomous_vehicle(world_size=(50,50), end=(25,2), start=(8,2), scale_factor=5, starting_direction=utils.direction.NORTH, turn_time=1.25)
    # a = autonomous_vehicle(world_size=(50,50), end=(45,2), start=(8,2), scale_factor=5, starting_direction=utils.direction.NORTH, turn_time=1.25) # EASTWARD
    a = autonomous_vehicle(world_size=(50,50), start=(45,2), end=(45,30), scale_factor=5, starting_direction=utils.direction.NORTH, turn_time=1.25) # EASTWARD 
    a.main_loop() 
    
    
    
