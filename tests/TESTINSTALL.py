# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 17:14:55 2016

@author: Alex
"""
errors = 0

print "Testing all dependancies are correctly installed... \n"

try:
    import numpy
except:
    print "Error - Verify numpy installation"
    errors += 1

try:
    import matplotlib.pyplot as plt
except:
    print "Error - Verify matplotlib installation"
    errors += 1
    
try:
    import openpyxl
except:
    print "Error - Verify openpyxl installation"
    errors += 1
    
try:
    import serial
except:
    print "Error - Verify pyserial installation"
    errors += 1
    
try:
    import yaml
except:
    print "Error - Verify yaml installation"
    errors += 1
    
try:
    from pymodbus.client.sync import ModbusSerialClient
except:
    print "Error - Verify pymodbus installation"
    errors += 1

if errors == 0:
    print "\nAll Tests Successful with Zero Errors"
elif errors == 1:
    print '\n' + str(errors)+ " error encountered during tests"
    print "See above for details of package to be reinstalled"
else:
    print '\n' + str(errors)+ " errors encountered during tests"
    print "See above for details of packages to be reinstalled"