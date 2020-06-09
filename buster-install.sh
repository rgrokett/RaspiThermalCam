#!/bin/bash
# Install RaspiThermalCam on Raspbian Buster List
#
# Run using:
# $ ./buster-install.sh
#
# Can be safely run multiple times
#
# version 20200608
#

echo "Installing required libraries..."
sudo apt-get update
sudo apt-get install -y build-essential python3 python3-pip python3-dev python3-smbus python3-scipy python3-pygame fbcat evtest libts0 libts-dev libts-bin

echo "Installing required Python 3 modules..."
sudo pip3 install colour RPi.GPIO

echo "Verifying Adafruit packages for PiTFT..."
X=`grep pitft /boot/config.txt`

if [ -z "$X" ];
then
        echo "NO Adafruit PiTFT Resistive Touch Display! SEE DOCS."
        echo "Installing Adafruit PiTFT driver. Follow screen instructions:"
        wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
        chmod +x adafruit-pitft.sh
        sudo ./adafruit-pitft.sh
	#exit
else
        echo "Found Adafruit PiTFT Resistive Touch Display OK"
fi


echo "Verifying Adafruit packages for GPIO..."
X=`pip3 list |grep Adafruit-GPIO`

if [ -z "$X" ];
then
        echo "NO Adafruit_Python_GPIO package! SEE DOCS."
        echo "Installing Adafruit Python GPIO component..."
        rm -rf Adafruit_Python_GPIO/
        git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
        sudo python3 Adafruit_Python_GPIO/setup.py install
	#exit
else
        echo "Found Adafruit_Python_GPIO package OK"
fi

echo "Verifying Adafruit packages for AMG8833..."
X=`pip3 list |grep adafruit-circuitpython-amg88xx`

if [ -z "$X" ];
then
        echo "NO adafruit-circuitpython-amg88xx package! SEE DOCS."
        echo "Installing required Python 3 modules..."
        sudo pip3 install adafruit-circuitpython-amg88xx
	#exit
else
        echo "Found adafruit-circuitpython-amg88xx package OK"
fi

echo "Verifying buttons are installed..."
echo "Move the on/off button to top row..."
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

crontab ./buster-cronfile
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
