#!/bin/sh
apt-get -S python-numpy python-matplotlib python-pyserial python-yaml python-pip
python2 -m pip install pymodbus
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python2 ./tests/TESTINSTALL.py