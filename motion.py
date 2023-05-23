import RPi.GPIO as GPIO
import time
from time import sleep 
GPIO.setmode(GPIO.BCM)

motionPin = 12




GPIO.setup(motionPin, GPIO.IN)

time.sleep(10) ## 10 second delay



try:
       while True:
              motion = GPIO.input(motionPin) ## is motion detected
              print(motion) 
              sleep(.1) ## small delay
except KeyboardInterrupt:
       GPIO.cleanup()
       print('GPIO Good to Go')






##if (detection_result.detections and hasattr(detection_result.detections[0].categories[0], "category_name"):
    ##   if(detection_result.detections[0].categories[0].category_name == 'Bird'):
       ##    GPIO.output(8, GPIO.HIGH)
      ##     sleep(1)
       ##    GPIO.output(8, GPIO.LOW)
       ##    sleep(1)
      ##     print(detection_result.detections[0].categories[0].category_name)
           
           
