#!/usr/bin/env python
"""
Author: Alexander David Leech
Date:   30/09/2015
Rev:    1
Lang:   Python 2.7
Deps:	Pyserial, Pymodbus, logging
"""

import time                                            # For sleep functionality
import logging                                         # For detailed error output
from pymodbus.client.sync import ModbusSerialClient \
as ModbusClient                                        # Import MODBUS support class

comSettings = {    
                "method"   : 'rtu',
                "port"     : 'COM3',
                "stopbits" : 1,                
                "bytesize" : 8,                
                "parity"   : 'N',
                "baudrate" : 9600,
                "timeout"  : 1
              }

logging.basicConfig()                                   # Setup error logging
log = logging.getLogger()                               # Start logging

client = ModbusClient(**comSettings)                    # Setup connection object
client.connect()                                        # Open the MODBUS connection

while(True):
    r = client.read_holding_registers(0, 4, unit=0x01)  # Read data back from the controller
    print ("PV: ", str(r.getRegister(0)))               # Print PV register
    print ("SP: ", str(r.getRegister(2)))               # Print SP register
    print ("OP: ", str(r.getRegister(3)))               # Print OP register
    time.sleep(4)                                       # Sample delay

client.close()                                          # Close the connection