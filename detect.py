# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
# Import packages
import os
import numpy as np
from threading import Thread
import importlib.util
import RPi.GPIO as GPIO
from time import sleep

#Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, width, height, resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not self.stream.isOpened():
            raise IOError("Couldn't open webcam or video")
        
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        ret = self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        ret = self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        ret = self.stream.set(cv2.CAP_PROP_FPS, framerate)
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool, resolution: str) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

  

  # Start capturing video input from the camera
#   cap = cv2.VideoCapture(camera_id)
#   cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
  resW, resH = resolution.split('x')
  imW, imH = int(resW), int(resH)
  # Initialize video stream
  videostream = VideoStream(width, height, resolution=(imW,imH),framerate=60).start()
  time.sleep(1)

  
  return videostream


def data_cam(model, enable_edgetpu, num_threads, videostream):
  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()
  
  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10
  
  # Initialize the object detection model
  base_options = core.BaseOptions(
      file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
      max_results=3, score_threshold=0.1)
  options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)

  # Continuously capture images from the camera and run inference
  while videostream.stream.isOpened():
    image = videostream.read()
#     if not success:
#       sys.exit(
#           'ERROR: Unable to read from webcam. Please verify your webcam settings.'
#       )

    counter += 1
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    # Draw keypoints and edges on input image
    image = utils.visualize(image, detection_result)

    # Calculate the FPS
    #if counter % fps_avg_frame_count == 0:
     # end_time = time.time()
      #fps = fps_avg_frame_count / (end_time - start_time)
      #start_time = time.time()

    # Show the FPS
    #fps_text = 'FPS = {:.1f}'.format(fps)
    #text_location = (left_margin, row_size)
    #cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, 
    #font_size, text_color, font_thickness)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break
    cv2.imshow('object_detector', image)
    if detection_result is not None: 
      return detection_result
    
    
  #cv2.destroyAllWindows()
  #videostream.stop()
  return detection_result


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='Senior_Design/android.tflite')
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
  parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1920x1080')
  args = parser.parse_args()

  return run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
      int(args.numThreads), bool(args.enableEdgeTPU), args.resolution), args


if __name__ == '__main__':
  # Open the webcam
  videostream, args = main()
  # retrieve the data
  while True: 
    try:
      print(data_cam(args.model, args.enableEdgeTPU, args.numThreads, videostream).detections[0].categories[0].category_name)
    except IndexError: 
      pass
