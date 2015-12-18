#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Class for communications to the honeywell controller using
        the modbus protocol library (pymodbus).
"""

from pymodbus.client.sync import ModbusSerialClient as ModbusClient            #Import the MODBUS Protocol
import logging                                                                 #For debugging purposes
import yaml
import pprint as pp

class comClient:

#    comSettings = { 
#                    "method"   : 'rtu',
#                    "port"     : 'COM3',    #COM2 for virtual serial port tests & COM3/4 for online running
#                    "stopbits" : 1,                
#                    "bytesize" : 8,                
#                    "parity"   : 'N',
#                    "baudrate" : 9600,
#                    "timeout"  : 1
#                  }


    def parseConfig(self):
        try:
            with open("conneNOFILEction.yaml", "r") as f:       # safely opens the file and gets the text
                config = yaml.load_all(f)                 # parses the data into python
                self.comSettings = config               # saves config to member variable
                # print [i for i in config]                 # DEBUG - prints it
        except IOError:
            print('Failed to set config from file. Falling back to default values:')
            self.comSettings = { 
                    "method"   : 'rtu',
                    "port"     : 'COM3',    #COM2 for virtual serial port tests & COM3/4 for online running
                    "stopbits" : 1,                
                    "bytesize" : 8,                
                    "parity"   : 'N',
                    "baudrate" : 9600,
                    "timeout"  : 1
                  }
            pp.pprint(self.comSettings)

    def __init__(self):
	self.parseConfig()
        # Configure logging on the client 
        logging.basicConfig()                            
        self.log = logging.getLogger()
        #Change to DEBUG for full information during runtime
        self.log.setLevel(logging.INFO)				
        #  Setup and Open the connection			
        self.client = ModbusClient(**self.comSettings)          

    def readData(self):
        self.client.connect()
        #REMEMBER: Controller is unit 0x01
        r = self.client.read_holding_registers(0, 4, unit=0x01)               
        self.client.close()
        return r

    def writeData(self,op):
        #Set to write data to the controller output (MODBUS HR 3)
        self.client.connect()
        w = self.client.write_register(3,op,unit=0x01)
        self.client.close()
        return w