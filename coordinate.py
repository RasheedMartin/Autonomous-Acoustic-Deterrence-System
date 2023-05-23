import RPi.GPIO as GPIO
import time
from time import sleep 
from gpiozero import AngularServo, Servo
from gpiozero import LED
from gpiozero import Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory  


my_factory = PiGPIOFactory()

#led1 = LED(21)
#led2 = LED(23)
#led3 = LED(24)


# Pin assignments for motion detectors 
motion_detector1 = 20
motion_detector2 = 16
motion_detector3 = 13
motion_detector4 = 6
motion_detector5 = 5




#servo = AngularServo(21,initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=my_factory)
#servo = Servo(21, pin_factory=my_factory)
# time.sleep(10) 


#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(21, GPIO.OUT)
#servo = GPIO.PWM(21, 50)
#servo.start(0)

# 5.0 = 90 degrees
# 10.65 = 180 degrees
# 12.5 = 270 degrees 






# for now, the different LED's are representing the servo postions. if motion is detected from one of the 4 sensors, the servo will move to the corresponding position 

def axis(motion_detector1, motion_detector2, motion_detector3, motion_detector4, motion_detector5):
	
	if motion_detector1:
		servo.angle = 0
		time.sleep(5)
		if motion_detector2 and motion_detector5:  
			pass
		elif motion_detector2: 
			servo.angle = 36
			time.sleep(5)
		else: 
			servo.angle = -36
			
	elif motion_detector2:
		servo.angle = 72
		time.sleep(5)
		if motion_detector1 and motion_detector3: 
			pass
		elif motion_detector3: 
			servo.angle = 108
			time.sleep(5)
		else: 
			servo.angle = 36
	elif motion_detector3:
		servo.angle = 144
		time.sleep(5)
		if motion_detector2 and motion_detector4: 
			pass
		elif motion_detector4: 
			servo.angle = 180
			time.sleep(5)
		else: 
			servo.angle = 108
			time.sleep(5)
	elif motion_detector4:
		servo.angle = 216
		time.sleep(5)
		if motion_detector3 and motion_detector5: 
			pass
		elif motion_detector5: 
			servo.angle = 252
			time.sleep(5)
		else: 
			servo.angle = 180
			time.sleep(5)
	elif motion_detector5:
		servo.angle = 288
		time.sleep(5)
		if motion_detector1 and motion_detector4: 
			pass
		elif motion_detector4: 
			servo.angle = 252
			time.sleep(5)
		else: 
			servo.angle = 324
		
