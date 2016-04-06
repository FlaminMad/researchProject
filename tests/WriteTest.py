#!/usr/bin/env python
"""
Author: Alexander David Leech
Date:   30/09/2015
Rev:    2
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
    client.write_register(3,1000,unit=0x01)             # Write valve to 100%
    time.sleep(4)                                       # Sleep 4 seconds
    client.write_register(3,0,unit=0x01)                # Write valve to 0%
    time.sleep(4)                                       # Sleep 4 seconds

client.close()                                          # Close the connection