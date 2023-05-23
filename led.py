import picamera 
from time import sleep 

camera = picamera.PiCamera()
camera.start_preview()
sleep(10)
camera.stop_preview()
