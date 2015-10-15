#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Main file for PID Controller
"""

import time                                                                    #Time based functions
from Modbus import comClient                                                   #Import Modbus Comms Class
from PIDController import PIDController as controller
from xlsLogging import xlsLogging
        
class researchProject:
    
    def __init__(self):
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise PID Controller
        self.ctrl = controller()
        #Initialise excel data logging
        self.xls = xlsLogging()

    def run(self):
        #Main Method
        while(True):
            #For controller time loop
            startTime = time.time()
            
            #Read controller data as r     
            try:
                r = self.rw.readData()        
            except:
                print "Modbus Error: Read Connection Failed"
                break

            #Pass data to excel for logging purposes
            self.xls.writeXls(r)

            #Send data to controller
            u = self.ctrl.runCtrl(r.getRegister(0),r.getRegister(2))
            
            #Write output to valve     
            try:
                self.rw.writeData(u)        
            except:
                print "Modbus Error: Write Connection Failed"
                break            
                        
            time.sleep(self.ctrl.dT - (time.time() - startTime))


def main():
    rp = researchProject()
    rp.run()

if __name__ == '__main__':main()
