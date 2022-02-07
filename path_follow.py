import picar_4wd as fc
import time
import numpy as np
from collections import deque
import math
from enum import IntEnum
import pdb
import grid_world
import gw_driver
from utils import *
import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import sys

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

# class direction(IntEnum):
#     NORTH=0
#     WEST=1
#     SOUTH=2
#     EAST=3


class navigation_module:

    def __init__(self, turn_time=1.3, avg_speed=25, step_size=5, direction=direction.NORTH):
        self.turn_time = turn_time
        self.avg_speed = avg_speed # in cm/sec at power 1
        self.step_size = step_size # in cm
        self.turn_funcs = [self.turn_left, self.turn_right]
        self.current_direction = direction
        self.current_node = None
        
    def turn_right(self, current_direction):
        fc.turn_left(1) # due to a bug with picar
        time.sleep(self.turn_time + 0.1)
        fc.stop()
        return direction((current_direction + 4 - 1) % 4)

    def turn_left(self, current_direction):
        fc.turn_right(1) # due to a bug with picar
        time.sleep(self.turn_time)
        fc.stop()
        return direction((current_direction + 1) % 4)

    def step_forward(self, num_steps):
        pause_time = num_steps * self.step_size / self.avg_speed
        fc.backward(1) # due to a bug with picar
        time.sleep(pause_time)
        fc.stop()
        time.sleep(0.1)

    def follow_path_for_n(self, path, n=np.inf):
        # assume the starting point is the first element of the path
        # and that the car is facing the y-axis
        count = 0
        self.current_node = path.pop()
        # pdb.set_trace()
        while len(path) != 0 and count < n:
            next_node = path.pop()
            self.current_direction = self.face_next_node(next_node)
            self.current_node = next_node
            self.step_forward(1)
            count+=1
            

        return self.current_node, self.current_direction

    def face_next_node(self, next_node):
        idx = self.get_turn_idx(next_node)
        if idx is None:
            return self.current_direction
        time.sleep(0.1)
        new_direction = self.turn_funcs[idx](self.current_direction)
        time.sleep(0.1)
        return new_direction
    
    def get_turn_idx(self, next_node):
        dx = next_node[0] - self.current_node[0]
        dy = next_node[1] - self.current_node[1]

        if abs(dx) > 0:
            if self.current_direction == direction.WEST or self.current_direction == direction.EAST:
                return
            tmp = self.current_direction + dx + 1
        elif abs(dy) > 0:
            if self.current_direction == direction.NORTH or self.current_direction == direction.SOUTH:
                return
            tmp = self.current_direction + dy
        else:
          return

        idx = (tmp // 2) % 2
        return idx

    def detect_objects():
        wdith = 640
        height = 480
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        model = 'efficientdet_lite0.tflite'
        enable_edgetpu = false


        options = ObjectDetectorOptions(
            num_threads=num_threads,
            score_threshold=0.3,
            max_results=3,
            enable_edgetpu=enable_edgetpu)
        detector = ObjectDetector(model_path=model, options=options)
        try:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    cap.release()
                    # cv2.destroyAllWindows()
                    sys.exit('ERROR: Unable to read from webcam.  Please verify your webcam settings')

                counter += 1
                image = cv2.flip(image,0) # flip the image vertically
                detections = detector.detect(image)
                image = utils.visualize(image,detections)

                # if counter % fps_avg_frame_count == 0:
                  # end_time = time.time()
                  # fps = fps_avg_frame_count / (end_time - start_time)
                  # start_time = time.time()

                  # # Show the FPS
                  # fps_text = 'FPS = {:.1f}'.format(fps)
                  # text_location = (left_margin, row_size)
                  # cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color,font_thickness)

                for detection in detections:
                      for category in detection.categories:
                          if category.label == 'stop sign' or category.label == 'person':
                              bb = detection.bounding_box
                              pdb.set_trace()
                              dist = utils.linear_distance((bb.left, bb.top), (bb.right, bb.bottom))

                              if category.label == 'stop sign':
                                if dist > 400:
                                  fc.stop()
                              else:
                                if dist > 212:
                                  fc.stop()
                                  hasStopSign = True


                              hasStopSign = True

                              if not stopSignInLastFrame:
                                  #first time seeing a stop sign
                                  # fc.stop()
                                  print("[CAMERA] Stop sign detected")
                                  stopSignInLastFrame=True

                              break
                      if hasStopSign:
                          # break out of larger loop with all the detections
                          break

        except:
            print('ERROR: something happened with the car')
            
        cap.release()
        cv2.destroyAllWindows()
