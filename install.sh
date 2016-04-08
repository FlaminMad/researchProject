#!/bin/sh
pacman -S python2-numpy python2-matplotlib python2-pyserial python2-pyyaml
git clone https://github.com/bashwork/pymodbus.git
python ./pymodbus/setup.py install
echo "Your good to go!"