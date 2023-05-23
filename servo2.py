import RPi.GPIO as GPIO
import time
from gpiozero.pins.pigpio import PiGPIOFactory  

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.OUT)

servo = GPIO.PWM(15,50)

servo.start(0)
print ("waiting for 1 sec")
time.sleep(1)

print ("Rotating at the intervals of 12 degrees")
duty = 5
while duty <= 17:
	servo.ChangeDutyCycle(duty)
	time.sleep(1)
	duty = duty +1
	
print ("Turning back to 0 degrees")
servo.ChangeDutyCycle(2)
time.sleep(1)
sevo.ChangeDutyCycle(0)

Servo.stop()
GPIO.cleanup()
print ("Everything's cleaned up")
