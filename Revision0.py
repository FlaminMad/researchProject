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
                "port"     : 'COM3',
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
log.setLevel(logging.DEBUG)


#                                 #
#  Setup and Open the connection  #
#                                 #

client = ModbusClient(**comSettings)
client.connect()


def dataLogging


while(True):
    pv = client.read_input_registers(0,1,unit=0x01)
    
    if pv.getRegister(0) < 500:
        wc = client.write_register(3,1000,unit=0x01)
    else:     
        wc = client.write_register(3,000,unit=0x01)
    time.sleep(5)

client.close()




#ser = serial.Serial('COM4', 9600, parity='N', stopbits=1, timeout=1) 	#Configuration Settings as per RPI Tests



