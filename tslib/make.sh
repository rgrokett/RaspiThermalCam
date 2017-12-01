#!/bin/bash
# Requires tslib source
# sudo apt-get install evtest tslib libts-bin					
# sudo apt-get install git automake libtool
# git clone git://github.com/kergoth/tslib.git
# See: http://www.impulseadventure.com/elec/rpi-install-tslib.html

gcc -Wall -W -c -o ts_check.o ts_check.c
/bin/bash /home/pi/tslib/libtool --tag=CC --mode=link gcc -Wall -W -o ts_check ts_check.o /home/pi/tslib/src/libts.la -ldl

