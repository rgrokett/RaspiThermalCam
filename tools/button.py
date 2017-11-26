#!/usr/bin/python
#
# Test TFT GPIO Buttons
#
# Usage:
# $ sudo python touch.py


import RPi.GPIO as GPIO
import time


channel = 27

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(channel):
    print('Input was HIGH')
else:
    print('Input was LOW')

while GPIO.input(channel) == GPIO.HIGH:
    time.sleep(0.01)  

if GPIO.input(channel) == GPIO.LOW:
	print('Button down LOW')

