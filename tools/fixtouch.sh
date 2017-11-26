#!/bin/bash
#
# Run this script if the touch.py example program gives 0,0 x/y 
# or the touch screen doesn't work as expected.
# 
# 11/2017 - NOTE: THIS NO LONGER APPEARS TO BE A VALID WORKAROUND
#	    Left here for documentation purposes only
#
# To remove:
# sudo rm /etc/apt/apt.conf.d/10defaultRelease
# sudo rm /etc/apt/preferences.d/libsdl
#
  
#enable wheezy package sources
echo "deb http://archive.raspbian.org/raspbian wheezy main" > /etc/apt/sources.list.d/wheezy.list

#set stable as default package source (currently jessie)
echo "APT::Default-release \"stable\";" > /etc/apt/apt.conf.d/10defaultRelease

#set the priority for libsdl from wheezy higher then the jessie package
echo "Package: libsdl1.2debian
Pin: release n=jessie
Pin-Priority: -10
Package: libsdl1.2debian
Pin: release n=wheezy
Pin-Priority: 900
" > /etc/apt/preferences.d/libsdl

#install
apt-get update
apt-get -y --force-yes install libsdl1.2debian/wheezy

