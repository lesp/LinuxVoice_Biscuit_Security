#IImport the modules that we need.
import RPi.GPIO as GPIO
import time

#Setup the GPIO to use the logical board reference.
GPIO.setmode(GPIO.BOARD)

#Variables to contain the pin references used in our project.
PIR_PIN = 7
reed = 26
trigger = 11
echo = 13

#Global is a method of using a variable both inside and outside of a function.
global distance

#Setup each of the GPIO pins as inputs and outputs.
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(reed, GPIO.IN)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, GPIO.LOW)

#Our default loading text
print("Welcome to the LV Biscuit Barrier - System Loading Please Wait")
time.sleep(2)
print("Scanning for intruders")

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


#Our main loop of code.
while True:
	#Take a reading using the ultrasonic sensor
    ultra(0)
    #First condition this handles the PIR sensor being tripped
    if GPIO.input(PIR_PIN) == True:
        print("Motion Detected near the biscuits")
    	time.sleep(1)
    #Second condition handles the reed switch being triggered by our magnetic biscuit tin lid
    elif GPIO.input(reed) == True:
        print("Biscuit tin has been opened CODE RED!!!")
    	time.sleep(1)
    #Our third and final condition uses the output from the ultra() function to tell us if the thief's hand is less than 10cm away
    elif distance < 10:
    	print("Biscuit thief has struck again, deploy ill tempered jack russell terrier")
