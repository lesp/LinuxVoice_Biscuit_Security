#IImport the modules that we need.
import RPi.GPIO as GPIO
import time
from easygui import *

#Setup the GPIO to use the logical board reference.
GPIO.setmode(GPIO.BOARD)

#Variables to contain the pin references used in our project.
PIR_PIN = 7
reed = 26
trigger = 11
echo = 13
logo = "./Images/masthead.gif"

#A list is used to store the possible answers for our splash question
activate = ["Yes","No"]

#Global is a method of using a variable both inside and outside of a function.
global distance

#Setup each of the GPIO pins as inputs and outputs.
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(reed, GPIO.IN)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, GPIO.LOW)

#Our default loading text is replaced with a splash screen.
splash_title = "Linux Voice Biscuit Securiy System V2"
splash_msg = "Would you like to protect the biscuits?"
start = buttonbox(title=splash_title,image=logo,msg=splash_msg,choices=activate)

#Creating a function to handle using the Ultrasonic sensor, as it is a little trickier to use.
def ultra(sensor):
    global distance
    if sensor == 0:

        time.sleep(0.3)

        GPIO.output(trigger, True)

        time.sleep(0.00001)
        GPIO.output(trigger, False)
        while GPIO.input(echo) == 0:
          signaloff = time.time()
        while GPIO.input(echo) == 1:
          signalon = time.time()

        timepassed = signalon - signaloff

        distance = timepassed * 17000
        
        return distance

    else:
        print "Error."
if start == "Yes":
	#Our main loop of code.
	while True:
		#Take a reading using the ultrasonic sensor
	    ultra(0)
	    #First condition this handles the PIR sensor being tripped
	    if GPIO.input(PIR_PIN) == True:
	        msgbox(title="Motion Detected", msg="--ALERT-- I have detected movement")
	    	time.sleep(1)
	    #Second condition handles the reed switch being triggered by our magnetic biscuit tin lid
	    elif GPIO.input(reed) == True:
	        msgbox(title="Biscuit tin has been opened CODE RED!!!", msg="--ALERT-- I have detected that the tin has been opened")
	    	time.sleep(1)
	    #Our third and final condition uses the output from the ultra() function to tell us if the thief's hand is less than 10cm away
	    elif distance < 10:
	    	msgbox(title="Hand in the biscuit tin", msg="--ALERT-- Biscuit thief has struck again, deploy ill tempered jack russell terrier")
else:
	print("EXIT")
