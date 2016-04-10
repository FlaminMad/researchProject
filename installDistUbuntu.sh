#!/bin/bash
apt-get install python-numpy python-matplotlib python-yaml python-openpyxl python-pip
python2 -m pip install pyserial pymodbus
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python2 ./tests/TESTINSTALL.py
