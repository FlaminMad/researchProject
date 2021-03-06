#!/usr/bin/env python
"""
Author: Alexander David Leech
Date:   30/09/2015
Rev:    2
Lang:   Python 2.7
Deps:	  Pyserial, Pymodbus, logging
Desc:   Cycles the output from 0 to 100% in steps of 10% at a defined rate
"""

import time                                            # For sleep functionality
import logging                                         # For detailed error output
from pymodbus.client.sync import ModbusSerialClient \
as ModbusClient                                        # Import MODBUS support class

vlvTime = 2                                            # Time (s) between changes 

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
    for i in range(0, 11):                              # Loop from 0 to 10
        client.write_register(3,(i*100),unit=0x01)      # Write output to controller
        time.sleep(vlvTime)                             # Sleep <predefined above> seconds

client.close()                                          # Close the connection