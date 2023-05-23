from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory  


my_factory = PiGPIOFactory()


servo = AngularServo(21,min_angle = 0, max_angle = 180, min_pulse_width = 0.0005, max_pulse_width = 0.0023)

while(True):
	servo.angle = 90
	#sleep(5)
	#servo.angle = 0
	#sleep(5)
	#servo.angle = 180
	#sleep(5)
	

	
