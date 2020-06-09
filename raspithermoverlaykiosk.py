#!/usr/bin/python
# 
# PiEyeR - Raspberry Pi Thermal Camera 
#
# Enhanced version of Adafruit Raspberry Pi Thermal Camera
# Based on Adafruit AMG8833 Grid-Eye module and PiTFT 2.8" screen
#
# Normally run by pi crontab at bootup
# Turn off by commenting out @reboot... using $ crontab -e; sudo reboot
# Manually run using $ sudo python raspitherm.py
#
# NOTICE: This is designed for a 320x240 screen only!
#
# Version 0.5 2017.11.26 - initial release
#         0.7 2017.12.01 - added touch screen snapshots (via workaround) 
#         0.8 2017.12.02 - expanded camera screen added data 
#	  0.8.1 - minor update to screen data format
#
# License: GPLv3, see: www.gnu.org/licenses/gpl-3.0.html
#

#from Adafruit_AMG88xx import Adafruit_AMG88xx
import adafruit_amg88xx, board, busio
import pygame
import os
import math
import sys
import time, datetime
import logging
import subprocess
import numpy as np
import RPi.GPIO as GPIO

from scipy.interpolate import griddata
from pygame.locals import *
from colour import Color

pygame.init()

# MY IMPORTS
from picamera import PiCamera
from PIL import Image, ImageDraw

CAMERA = PiCamera()
CAMERA.rotation = 180
CAMERA_DISPLAYING = False


##### VARIABLES
DEBUG	= 0	# Debug 0/1 off/on (writes to debug.log)

# INITIAL TEMPERATURE VALUES
MINTEMP = 26	# Low temp range (blue)
MAXTEMP = 32	# High temp range (red)

COLORDEPTH = 1024	
MARGIN = 20

# GPIO BUTTONS
BTN1	= 17	# Top	
BTN2	= 22	# Second
BTN3	= 23	# Third
BTN4	= 27	# Fourth

# FULL SCREEN COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE  = (0,0,255)
YELLOW= (255,255,0)
CYAN  = (0,255,255)
RED   = (255,0,0)
GRAY  = (128,128,128)

F_WIDTH  = 320*2
F_HEIGHT = 240*2
PIXEL_WIDTH = F_WIDTH / 32
PIXEL_HEIGHT = F_HEIGHT / 24
OVERLAY_ALPHA = 70

###### FUNCTIONS
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Clear Screen
def cleartft(scolor):
    logger.info('cleartft('+str(scolor)+')')
    lcd = pygame.display.set_mode((F_WIDTH, F_HEIGHT))
    lcd.fill(scolor)
    pygame.display.update()

# Display the Mode Screen (Designed for 320x240 screen)
def displayMode():
    logger.info('displayMode()')
    cleartft(BLACK)
    lcd = pygame.display.set_mode((F_WIDTH, F_HEIGHT))
    # Title Screen
    fnt = pygame.font.Font(None, 40*2)
    txt = fnt.render('PiEyeR Camera',True,CYAN)
    lcd.blit(txt, (10*2,10*2))
    pygame.draw.lines(lcd,WHITE,False, [(10*2,50*2),(210*2,50*2)])
    # Info Box
    pygame.draw.rect(lcd,BLUE,[(10*2,60*2),(200*2,180*2)])
    pygame.draw.rect(lcd,WHITE,[(10*2,60*2),(200*2,180*2)],1)
    fnt = pygame.font.Font(None, 15*2)
    txt = fnt.render('AMG8833 Grid-Eye Thermal Camera',True,YELLOW)
    lcd.blit(txt, (20*2,70*2))
    txt = fnt.render('for Raspberry Pi',True,WHITE)
    lcd.blit(txt, (60*2,90*2))
    txt = fnt.render('PWR   = Shutdown/Startup',True,CYAN)
    lcd.blit(txt, (30*2,130*2))
    txt = fnt.render('UP/DN = Change Sensitivity',True,CYAN)
    lcd.blit(txt, (30*2,150*2))
    txt = fnt.render('CAM    = Camera Mode',True,CYAN)
    lcd.blit(txt, (30*2,170*2))
    txt = fnt.render('Touch Screen for Snapshot',True,WHITE)
    lcd.blit(txt, (30*2,190*2))
    # Function Buttons
    font_big = pygame.font.Font(None, 25*2)
    # The UP/DOWN text can be updated for supporting future features
    # They are separate from the camera sensitivity buttons.
    #mode_buttons = {'Power ->':(270,40),'Future->':(270,100),'Future->':(270,160),'Camera->':(270,220)}
    mode_buttons = {'PWR ->':(280*2,40*2), 'CAM ->':(280*2,100*2), 'FLIR->':(280*2,160*2), 'OVERLAY->':(260*2,220*2)}
    for k,v in mode_buttons.items():
        text_surface = font_big.render('%s'%k, True, YELLOW)
        rect = text_surface.get_rect(center=v)
        lcd.blit(text_surface, rect)
    pygame.display.update()

# TouchScreen - using pygame (current not working)
# Checks for screen touch
# commented out
'''
def touch():
    logger.info('touch()')
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
	    pos = pygame.mouse.get_pos()
            logger.info('mousedown')
	    time.sleep(0.1)
        elif(event.type is MOUSEBUTTONUP):
	    pos = pygame.mouse.get_pos()
            logger.info('mouseup')
	    screensnap()
	    break
''' and None

# TouchScreen - using tslib and custom pgm (workaround)
# due to bug in SDL lib with using pygame.
# Checks for screen touch
def touch():
    logger.info('touch() -- removed. No library tslib in Raspbian Buster.')
#    xy = subprocess.check_output(["ts_check"])
#    if(xy):
#        logger.info('screen touched'+str(xy))
#        screensnap()
    
# Screen snapshot 
# Snapshots go into snapshot subdirectory
# (Future: add transfer mechanism)
def screensnap():
    logger.info('screensnap()')
    cur_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S') 
    filename="/home/pi/snapshot/"+cur_date+".png"
    subprocess.call(["sudo","fbgrab","-d","/dev/fb1",filename])
    time.sleep(0.2)
    lcd = pygame.display.set_mode((F_WIDTH, F_HEIGHT))
    lcd.fill(WHITE)
    pygame.display.update()
    time.sleep(0.2)
    lcd.fill(BLUE)
    pygame.display.update()
    time.sleep(0.2)

# TODO FUTURE FEATURES
def future(msg):
    logger.info('future('+msg+')')
    cleartft(BLUE)
    lcd = pygame.display.set_mode((F_WIDTH, F_HEIGHT))
    font_big = pygame.font.Font(None, 50)
    text_surface = font_big.render('FUTURE', True, WHITE)
    rect = text_surface.get_rect(center=(160,120))
    lcd.blit(text_surface, rect)
    pygame.display.update()
    time.sleep(2)

# IR Thermal Camera
def ir_camera():
    logger.info('ir_camera()')
    lcd = pygame.display.set_mode((F_WIDTH, F_HEIGHT))
    lcd.fill(BLUE)
    pygame.display.update()
    time.sleep(0.5)
    showBtns = 0
    offset = 15 #was zero - works better this way with new adafruit library.
    loop = 1
    while (loop):
        # read the pixels
 #        pixels_d = sensor.readPixels()
        pixels_d = []
        for row in sensor.pixels:
            pixels_d = pixels_d + row
        # Remap pixels
        pixels_d = [map(p, MINTEMP+offset, MAXTEMP+offset, 0, COLORDEPTH - 1) for p in pixels_d]
        #Perform interpolation
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
        #Draw Image
        for ix, row in enumerate(bicubic):
                for jx, pixel in enumerate(row):
                    pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (PIXEL_HEIGHT * ix, PIXEL_WIDTH * jx, PIXEL_HEIGHT, PIXEL_WIDTH))
	
        # Flip the screen horizontally to match front facing IP camera
        surf = pygame.transform.flip(lcd,True,False)
        lcd.blit(surf,(0,0))
        # Add buttons (show for X seconds)
        if (showBtns < 25):
            fnt = pygame.font.Font(None, 15*2)
            mode_buttons = {'PWR ->':(280*2,40*2), '   UP ->':(280*2,100*2), 'DOWN->':(280*2,160*2), 'MODE->':(280*2,220*2)}
            for k,v in mode_buttons.items():
                text_surface = fnt.render('%s'%k, True, GRAY)
                rect = text_surface.get_rect(center=v)
                lcd.blit(text_surface, rect)
        showBtns = showBtns + 1
        # Add Data to screen
        fnt = pygame.font.Font(None, 15*2)
        cur_date = datetime.datetime.now().strftime('%a  %d  %b %H : %M : %S %Z %Y') 
        text_surface = fnt.render(cur_date, True, GRAY)
        lcd.blit(text_surface, (10*2,220*2))
        text = "Min  = {0:.0f} C".format(min(pixels_d))
        text_surface = fnt.render(text, True, GRAY)
        lcd.blit(text_surface, (10*2,20*2))
        text = "Max = {0:.0f} C".format(max(pixels_d))
        text_surface = fnt.render(text, True, GRAY)
        lcd.blit(text_surface, (10*2,30*2))
        pygame.display.update()
        # GPIO Button Press 
        if GPIO.input(BTN4) == GPIO.LOW:
            logger.info("stopping ir_camera()")
            loop = 0
            time.sleep(0.5)	
        if GPIO.input(BTN2) == GPIO.LOW:
            logger.info("UP")
            offset = offset - 1
            showBtns = 0
            time.sleep(0.5)	
        if GPIO.input(BTN3) == GPIO.LOW:
            logger.info("DOWN")
            offset = offset + 1
            showBtns = 0
            time.sleep(0.5)	
        # Touch Screen Snapshot
        #touch()


def camera(cam_displaying):
	if cam_displaying:
		CAMERA.stop_preview()
		CAMERA.close()
		return False
	else:
		CAMERA = PiCamera()
		CAMERA.rotation = 180
		CAMERA_DISPLAYING = false
		CAMERA.start_preview()
		return True


def overlay():
    CAMERA = PiCamera()
    CAMERA.rotation = 180
    CAMERA.start_preview()
    sensitivity = -7 #BT edit: was -5
    overlay1, overlay2 = None, None
    loop = True
    startT = time.time()
    while loop:
        endT = time.time()
        if (endT - startT > 3600):
            print('restarting overlay...')
            logger.info('restarting overlay...')
            startT = time.time()
            loop = False

        pad = Image.new('RGB', (F_WIDTH,F_HEIGHT))
        draw = ImageDraw.Draw(pad)

        #read the pixels
#        pixels_d = sensor.readPixels()
        pixels_d = []
        for row in sensor.pixels:
            pixels_d = pixels_d + row
        # Remap pixels
        # Remap pixels
        pixels = [map(p, MINTEMP+sensitivity, MAXTEMP+sensitivity, 0, COLORDEPTH - 1) for p in pixels_d]
        #Perform interpolation
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')

        #Draw Overlay
        x = 31 * PIXEL_WIDTH
        y = -6 * PIXEL_HEIGHT
        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                draw.rectangle((
                    x, y, x + PIXEL_WIDTH, y + PIXEL_HEIGHT),
                    fill = colors[constrain(int(pixel), 0, COLORDEPTH- 1)])
                y = y + PIXEL_HEIGHT
            x = x - PIXEL_WIDTH
            y = -6 * PIXEL_HEIGHT

        if overlay1 == None:
            overlay1 = CAMERA.add_overlay(pad.tobytes(), size=pad.size, layer=3, alpha=OVERLAY_ALPHA)
            if not overlay2 == None:
                CAMERA.remove_overlay(overlay2)
                overlay2 = None
        else:
            overlay2 = CAMERA.add_overlay(pad.tobytes(), size=pad.size, layer=3, alpha=OVERLAY_ALPHA)
            if not overlay1 == None:
                CAMERA.remove_overlay(overlay1)
                overlay1 = None

        if GPIO.input(BTN2) == GPIO.LOW:
            sensitivity = sensitivity - 1
            time.sleep(0.5)
        elif GPIO.input(BTN3) == GPIO.LOW:
            sensitivity = sensitivity + 1
            time.sleep(0.5)
        elif GPIO.input(BTN4) == GPIO.LOW:
            loop = False
            time.sleep(0.5)

    if not overlay1 == None:
        CAMERA.remove_overlay(overlay1)
    if not overlay2 == None:
        CAMERA.remove_overlay(overlay2)
    CAMERA.stop_preview()
    CAMERA.close()


######
# MAIN
######
# Setup Logging
logger = logging.getLogger()
handler = logging.FileHandler('debug.log')
if DEBUG:
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
else:
    logger.setLevel(logging.ERROR)
    handler.setLevel(logging.ERROR)
log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)

logger.info('Starting')

# Setup OS Env
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


# Setup GPIO buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

## Thermal Sensor
#sensor = Adafruit_AMG88xx()
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c)
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# Set Color range
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

# Create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]


# PYGAME SCREEN
#pygame.init() # initialized earlier
pygame.mouse.set_visible(False)
cleartft(BLACK)

logger.info('setup complete')

# Display MODE screen
displayMode()

# Wait for sensor initialize
time.sleep(.1)

# BT edit: Run this upon start after 15secs of menu screen
#          if user presses "mode," it will go back to menu screen
CAMERA.close()
CAMERA_DISPLAYING = False
startT = time.time()
overlayRun = 0
while True:
        if (overlayRun == 12):
                print('quitting after 12 overlays...')
                logger.info('quitting after 12 overlays...')
                cleartft(BLACK)
                time.sleep(5)
                sys.exit(1)

        endT = time.time() #BT edit: if no button pressed in 1min, start overlay
        if (endT - startT > 60):
                overlayRun = overlayRun + 1
                print('entering overlay by default...')
                logger.info('entering overlay by default')
                overlay()
                displayMode()
                startT = time.time()
                time.sleep(.5)

        # GPIO Button Press to exit
        if GPIO.input(BTN1) == GPIO.LOW:
            cleartft(BLACK)
            time.sleep(5)
            sys.exit(0)

        if GPIO.input(BTN2) == GPIO.LOW:
        # CAMERA
            if not CAMERA_DISPLAYING:
                CAMERA = PiCamera()
                CAMERA.rotation = 180
                CAMERA.start_preview()
                CAMERA_DISPLAYING = True
                #displayMode()
                time.sleep(0.5)

        if GPIO.input(BTN3) == GPIO.LOW:
        # IR_CAMERA
            cleartft(BLACK)
            time.sleep(0.1)
            ir_camera()
            displayMode()
            time.sleep(0.5)

        if GPIO.input(BTN4) == GPIO.LOW:
            if CAMERA_DISPLAYING:
                CAMERA.stop_preview()
                CAMERA_DISPLAYING = False
                CAMERA.close()
            else:
                # OVERLAY
                overlay()
                displayMode()
                time.sleep(0.5)

        time.sleep(.1)

### END
