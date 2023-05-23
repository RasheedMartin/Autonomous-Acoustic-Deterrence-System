from gpiozero import LED, MotionSensor
from time import sleep
from coordinate import *
from detect import main, data_cam, *


#when detect.py is operational. These will be values read in from the main fuction of detect.py

videostream, args = main()
	
while True:

	motion1 = MotionSensor(motion_detector1)
	motion2 = MotionSensor(motion_detector2)
	motion3 = MotionSensor(motion_detector3)
	motion4 = MotionSensor(motion_detector4)
	motion5 = MotionSensor(motion_detector5)
	
	# Find the location of the object
	axis(motion1, motion2, motion3, motion4, motion5)

	# What is it?
	try:
	  data = (data_cam(args.model, args.enableEdgeTPU, args.numThreads, videostream).detections[0].categories[0].category_name)
	except IndexError: 
	  data = "Nothing"
	
	# Play sound based on what the object is
	if data == "Bird":
		# Play sound from Speaker 
		
		time.sleep(10)

	elif detect_results == "Squirrel":
		time.sleep(10)
	elif detect_results == "Raccoon":
		time.sleep(10)
	else
		pass
