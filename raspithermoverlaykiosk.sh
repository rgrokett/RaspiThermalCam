#!/bin/bash
cd

sudo python3 /home/pi/RaspiThermalCam/raspitherm.py

if [ $? -eq 0 ]
then
   sleep 10
   echo "thermal camera quit by user. quitting at " + $(date) >> /home/pi/RaspiThermalCam/raspitherm.log
   exit 0
else
   sleep 10
   echo "thermal cam self-quit. waiting to restart at " + $(date) >> /home/pi/RaspiThermalCam/raspitherm.log
   sudo reboot
fi
