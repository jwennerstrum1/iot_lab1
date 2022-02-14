import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import sys
import utils
import pdb

class camera:
    def __init__(self):
      self.width = 640
      self.height = 480
      self.cap = None
      self.enable_edgetpu = False
      self.model = 'efficientdet_lite0.tflite'
      
      try:
          self.cap = cv2.VideoCapture(0)
          self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
          self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
      except:
          print('ERROR: Something occured while setting up the car')
          self.cap.release()

      options = ObjectDetectorOptions(
              num_threads=1,
              score_threshold=0.3,
              max_results=3,
              enable_edgetpu=self.enable_edgetpu)
      self.detector = ObjectDetector(model_path=self.model, options=options)

    def __del__(self):
        self.cap.release()


    def capture_image(self):
        success, image = self.cap.read()
        if not success:
            self.cap.release()
            print('ERROR: Unable to read from camera')
        return success, image

    def detect_obstacles(self):
        success, image = self.capture_image()
        image = cv2.flip(image, 0 )
        detections = self.detector.detect(image)
        pedestrian_in_view = False
        stop_sign_in_view = False
        for detection in detections:
            for category in detection.categories:
                if category.label == 'stop sign' :
                    stop_sign_in_view = True
                    
                elif category.label == 'person':
                    pedestrian_in_view = True
        return pedestrian_in_view, stop_sign_in_view
