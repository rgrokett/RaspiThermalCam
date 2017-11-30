# PiEyeR RaspiThermalCam
## Portable Raspberry Pi AMG8833 Grid-Eye IR Thermal Camera

version 0.5 - 2017-11-26

### Overview
The Adafruit AMG8833 IR Thermal Camera board can provide a “FLIR™”-like imaging camera at about 1/10th the price of previous IR Thermal imaging units.  Of course, the resolution and sensitivity are not as high as more advanced cameras, but hey, for $39 it’s a great deal.  

Note that IR Thermal Cameras are NOT the same as NOIR cameras. The former uses only the heat given off by the object being imaged, while the latter requires an infrared light source such as IR LEDs to illuminate the object. 

With this project, I took the excellent Adafruit tutorial [Raspberry Pi Thermal Camera](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor/raspberry-pi-thermal-camera) by Dean Miller and added extra functionality to the software and hardware.

The PiTFT display uses Adafruit's custom Linux Kernel. *(See below)* This project only needs the Jessie Lite-based PiTFT Resitive Image, as it does not use the GUI.

### New features:
- Safely shutdown/power up Raspberry
- Automatically runs software at powerup
- Battery Powered for portability
- Uses PiTFT GPIO buttons
- Sensitivity controls
- Potential for future additions

**See Full Instructions in the [RaspiThermalCam.pdf](https://github.com/rgrokett/RaspiThermalCam/raw/master/RaspiThermalCam.pdf) document**

### Requirements
**NOTE:** This project assumes the user has set up their Raspberry Pi using the Adafruit tutorial mentioned above, thus consists of:
1. [Raspberry Pi Thermal Camera](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor/raspberry-pi-thermal-camera) 
- Adafruit AMG8833 IR Thermal Camera Breakout [ID 3538](https://www.adafruit.com/product/3538)
2. It also specifically requires the Adafruit PiTFT Plus 2.8" 320x240 screen to be installed and running. 
- [Required PiTFT Kernal Install](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install)
- Download [Jessie Lite-based PiTFT image ](https://s3.amazonaws.com/adafruit-raspberry-pi/2016-10-18-pitft-28r-lite.zip)
- PiTFT Plus 2.8" TFT 320x240 Touch Screen [ID 2298](https://www.adafruit.com/product/2298)
3. Currently uses also:
- Raspberry Pi 3, 4GB or larger micro SD card
- 5V power supply, wiring, cables, etc.
4. It DOES NOT require the Cobbler as mentioned, but does need a cable to connect the camera. I suggest:
- Adafruit 40 Pin GPIO Cable [ID 1988](https://www.adafruit.com/product/1988)
- Adafruit 2X20 Pin IDC Box Header [ID 1993](https://www.adafruit.com/product/1993)

### Extras
- Faceplate and case for PiTFT and Raspberry Pi 3 [ID 2807](https://www.adafruit.com/product/2807)
- 5V external USB Battery (such as external cellphone rechargeable) with 2 amp output
- Box to hold battery, computer and camera 

### Installation
You **MUST** have the Adafruit tutorial version installed and working before using this. This project just replaces the Adafruit thermalcam.py with a new python program. IT WILL NOT WORK OTHERWISE. 

Also, it expects the assembled version of the Adafruit 2.8" 320x240 PiTFT Plus screen otherwise the screen layout will NOT ALIGN and the GPIO buttons will NOT FUNCTION as expected. The Raspbian GUI is NOT NEEDED, so uses their custom Jessie Lite. 

The camera should be facing forward, like a digital camera: LCD screen towards you and camera towards (hot) object. 

1. Log into the Raspberry Pi with SSH or keyboard (defaults to "pi/raspberry")
2. Download and install the enhanced thermal program:
```
git clone https://github.com/rgrokett/RaspiThermalCam.git
cd RaspiThermalCam
./install.sh
sudo reboot
```

Once rebooted, you should see the new PiEyeR screen. See Troubleshooting if needed.  

The 4 buttons on the TFT screen have been re-mapped to GPIO functions as shown:

1. Safely Shutdown/Start up Raspberry (Does not remove 5V power, must be done usually via the 5V USB battery on/off switch)
2. Increase Sensitivity (while in Camera Mode)
3. Decrease Sensitivity (while in Camera Mode)
4. Start/Stop Camera Mode


The stl/ subdirectory contains 3D Printed front case parts for the camera. See the PDF document for details.

### Future 
- Switch to using Raspberry Pi Zero W for lower cost & power/smaller size
- Add new mode button features for middle buttons
- Get pygame Touch Screen working for PiTFT
- Add Camera Screen Snapshot feature

### Troubleshooting

**I don't see any new screen, only the boot messages and login.** 

Did you run the ./install.sh script? 
Try running $ crontab -l and see if you see a @reboot line:
```
@reboot sudo python /home/pi/RaspiThermalCam/raspitherm.py >/dev/null 2>&1
``` 
You did set up your Pi Thermal Camera as detailed in the [Adafruit tutorial](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor/raspberry-pi-thermal-camera) 

**I get a python error message**
Most likely there is a missing python package. The last line of the Python error should say what is missing. Try Googling that message.
Else, leave an Issue here at Github.

**My screen is mangled up, but the buttons seem to work**
Are you using the PiTFT Plus 2.8" 320x240 screen?  

**My buttons don't work or are on the bottom not side of the PiTFT**
You have a different screen. If you have GPIO buttons on botton of TFT, you can try remapping them in the raspitherm.py program.

**The Touchscreen doesn't work**
Bugs in the SDL software used by pygame make for inconsistent operation of the touch screen. We have to wait for a better solution. This program doesn't use the touch, just buttons.

**My Camera screen is all BLUE or all RED**
Press the Sensitivity buttons (middle two) to increase/decrease sensitivity

**My Camera doesn't work**
Try manually running tools/thermal_cam.py program. This is the same program from Adafruit with no modifications.
You may need to kill the raspitherm.py program first by editing the crontab:
```
crontab -e
comment out the @reboot line
#@reboot ...
```
**What can I see with it?**
Find a cat. They glow hot!
So do water heaters!
