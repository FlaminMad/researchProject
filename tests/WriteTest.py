#!/usr/bin/env python
"""
Author: Alexander David Leech
Date:   30/09/2015
Rev:    1
Lang:   Python 2.7
Deps:	Pyserial, Pymodbus
"""

import time

comSettings = {    
                "method"   : 'rtu',
                "port"     : '/dev/ttyUSB1',
                "stopbits" : 1,                
                "bytesize" : 8,                
                "parity"   : 'N',
                "baudrate" : 9600,
                "timeout"  : 1
              }


#                                   #
#  	 Import the MODBUS Protocol	  #
#                                   #

from pymodbus.client.sync import ModbusSerialClient as ModbusClient


#                                 #
# Configure logging on the client #
#                                 #

import logging
logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.INFO)


#                                 #
#  Setup and Open the connection  #
#                                 #

client = ModbusClient(**comSettings)
client.connect()


while(True):
    client.write_register(3,1000,unit=0x01)   
    time.sleep(4)
    client.write_register(3,0,unit=0x01)
    time.sleep(4)

client.close()




#ser = serial.Serial('COM4', 9600, parity='N', stopbits=1, timeout=1) 	#Configuration Settings as per RPI Tests



