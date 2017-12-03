#!/bin/bash
# Install RaspiThermalCam
# 
# Run using:
# $ ./install.sh
#
# Can be safely run multiple times
#
# version 20171203
#

# Make sure python requirements are installed
sudo apt-get update
sudo apt-get install -y build-essential python-pip python-dev python-smbus 
sudo apt-get install -y python-scipy python-pygame fbcat
sudo apt-get install evtest tslib libts-bin

echo 

# Verify Adafruit packages for PiTFT 
X=`grep pitft /boot/config.txt`

if [ -z "$X" ];
then
        echo "NO Adafruit PiTFT Resistive Touch Display! SEE DOCS."
	exit
else
        echo "Found Adafruit PiTFT Resistive Touch Display OK"
fi


# Verify Adafruit packages for GPIO
X=`pip list |grep Adafruit-GPIO`

if [ -z "$X" ];
then
        echo "NO Adafruit_Python_GPIO package! SEE DOCS."
	exit
else
        echo "Found Adafruit_Python_GPIO package OK"
fi

# Verify Adafruit packages for AMG8833
X=`pip list |grep Adafruit-AMG88xx`

if [ -z "$X" ];
then
        echo "NO Adafruit_AMG88xx_python package! SEE DOCS."
	exit
else
        echo "Found Adafruit_AMG88xx_python package OK"
fi

# VERIFY BUTTONS ARE INSTALLED
# Move the on/off button to top row
X=`grep rpi_power_switch /etc/modules`

if [ -z "$X" ];
then
        sudo bash -c "cp -p /etc/modules /etc/modules.BAK"
        sudo bash -c "echo 'rpi_power_switch' >> /etc/modules"
	echo "Added power button to /etc/modules"
else
	echo "Found power button OK"
fi
	
X=`grep "rpi_power_switch" /etc/modprobe.d/adafruit.conf`
Y=`grep "17" /etc/modprobe.d/adafruit.conf`
if [ -z "$X" ]; then
        sudo bash -c "cp -p /etc/modprobe.d/adafruit.conf /etc/modprobe.d/adafruit.conf.BAK"
        sudo bash -c "echo 'options rpi_power_switch gpio_pin=17 mode=0' > /etc/modprobe.d/adafruit.conf"
	echo "Added rpi_power_switch to /etc/modprobe.d/adafruit.conf"
elif [ -z "$Y" ]; then
        sudo bash -c "echo 'options rpi_power_switch gpio_pin=17 mode=0' > /etc/modprobe.d/adafruit.conf"
	echo "Added rpi_power_switch to /etc/modprobe.d/adafruit.conf"
else
	echo "Found power button is assigned OK"
fi

# NOW WITH THE REAL INSTALL

crontab ./cronfile
echo "Crontab entry installed for pi userid. OK"


# Install tslib touchscreen libs & pgm
sudo cp tslib/pointercal /usr/local/etc/
sudo cp tslib/ts.conf /usr/local/etc/
sudo cp tslib/ts_check /usr/local/bin/
sudo cp -rp tslib/ts /usr/local/lib/
sudo cp -P tslib/libts.so.0.9.0 /usr/lib/arm-linux-gnueabihf/libts.so.0

# DIRECTORY FOR SCREENSHOTS 
mkdir -p /home/pi/snapshot

# FINISHED!
echo "Finished installation. See Readme.md for more info"
echo "Reboot your pi now:  $ sudo reboot"
echo


