import pdb
import cv2
import utils
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import sys
import argparse
import time

# picar interaction
import picar_4wd as fc
from picar_4wd.servo import Servo
from picar_4wd.pwm import PWM
from picar_4wd.ultrasonic import Ultrasonic
from picar_4wd.pin import Pin

# keyboard interaction
import tty
import termios
import asyncio



def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Initialize the object detection model
  options = ObjectDetectorOptions(
      num_threads=num_threads,
      score_threshold=0.3,
      max_results=3,
      enable_edgetpu=enable_edgetpu)
  detector = ObjectDetector(model_path=model, options=options)

  us = Ultrasonic(Pin("D8"), Pin("D9"))
  fc.backward(1)

  stopSignInLastFrame = False
  hasStopSign = False
  # Continuously capture images from the camera and run inference
  try:
      while cap.isOpened():

          success, image = cap.read()
          if not success:
              sys.exit('ERROR: Unable to read from webcam.  Please verify your webcam settings')

          counter += 1
          image = cv2.flip(image,0) # flip the image vertically
          detections = detector.detect(image)
          image = utils.visualize(image,detections)

          if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

            # Whow the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color,font_thickness)

          for detection in detections:
                for category in detection.categories:
                    if category.label == 'stop sign' or category.label == 'person':
                        pdb.set_trace()
                        left = detection.bounding_box.left
                        top = detection.bounding_box.top
                        right = detection.bounding_box.right
                        bottom = detection.bounding_box.bottom
                        start_point = (left, top)
                        end_point = (right, bottom)
                        dist = utils.linear_distance(start_point, end_point)
                        
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
                        # key = readkey()
                        # if key == 'w':
                        #     # fc.backward(5)
                        #     print("[human] moving forward")
                        # else:
                        #     break
                if hasStopSign:
                    # break out of larger loop with all the detections
                    break

          if not hasStopSign:
            # stop sign dissapeared from view, continue moving
            fc.backward(1)
            stopSignInLastFrame = False
                
          # pdb.set_trace()
          cv2.imshow('object_detector', image)
          key = cv2.waitKey(100)
          if key == 27:
              # press ESC to quit
              print('User ending program')
              fc.stop()
              break
          
          hasStopSign = False
  except:
      print('ERROR: somehting happend with the car')
      # fc.stop()
      
  cap.release()
  cv2.destroyAllWindows()

    
    
def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU))


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


if __name__ == '__main__':
  main()
