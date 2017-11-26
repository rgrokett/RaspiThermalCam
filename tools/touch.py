#!/usr/bin/python
#
# Test Touch Screen controls
#
# Usage:  
# $ sudo python touch.py


import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO
 
print "NOTICE: PyGame SDL1.x Library DOES NOT WORK WITH TOUCH"

#Setup the GPIOs as outputs - only 23 and 27 are available
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
 
#Colours
WHITE = (255,255,255)
 
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
 
pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()
 
font_big = pygame.font.Font(None, 50)
 
touch_buttons = {'27 on':(80,60), '23 on':(240,60), '27 off':(80,180), '23 off':(240,180)}
 
for k,v in touch_buttons.items():
    text_surface = font_big.render('%s'%k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)
 
pygame.display.update()
 
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos
            #Find which quarter of the screen we're in
            x,y = pos
            if y < 120:
                if x < 160:
                    GPIO.output(27, False)
                else:
                    GPIO.output(23, False)
            else:
                if x < 160:
                    GPIO.output(27, True)
                else:
                    GPIO.output(23, True)
    sleep(0.1)
