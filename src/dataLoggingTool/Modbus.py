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
import logging
import yaml
import time


class comClient:

    def __init__(self):
        self.__parseConfig()
        # Configure logging on the client 
        logging.basicConfig()                            
        self.log = logging.getLogger()
        #Change to DEBUG for full information during runtime
        self.log.setLevel(logging.INFO)				
        #  Setup and Open the connection			
        self.client = ModbusClient(**self.comSettings)          


    def __parseConfig(self):
        try:
            with open("../../cfg/connection.yaml", "r") as f:       # safely opens the file and gets the text
                config = yaml.load(f)                               # parses the data into python
                self.comSettings = config                           # saves config to member variable
                
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


    def dataHandler(self, operation, *data):
        if operation == 'r':
            for i in range(3):
                r = self.__readData()
                if r != IOError:
                    break
                elif i == 2:
                    raise SystemExit('Modbus Error: Failed 3 Attemps')
                time.sleep(5)
            return r
        
        elif operation == 'w':
            try:            
                self.__writeData(data[0])
            except IndexError:
                raise SystemExit('No data passed to write!')
            return
            
        else:
            raise ValueError('Invalid Operation')

        
    def __readData(self):
        try:        
            self.client.connect()
            #REMEMBER: Controller is unit 0x01
            r = self.client.read_holding_registers(0, 4, unit=0x01)               
            self.client.close()
            return r
        except:
            print "Modbus Error: Read Connection Failed"
            return IOError


    def __writeData(self,op):
        #Set to write data to the controller output (MODBUS HR 3)
        self.client.connect()
        w = self.client.write_register(3,op,unit=0x01)
        self.client.close()
        return w