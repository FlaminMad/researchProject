#!/bin/sh
pacman -S --needed python2-numpy python2-matplotlib python2-pyserial python2-yaml python2-pip
python2 -m pip install pymodbus
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python2 ./tests/TESTINSTALL.py