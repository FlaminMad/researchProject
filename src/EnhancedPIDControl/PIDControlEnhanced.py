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

import time
import sys ; sys.path.insert(0, '../dataLoggingTool')

from osTools import osTools                 #For detecting exit keypress
from xlsLogging import xlsLogging
from plotActiveGraph import plotActiveGraph
from PIDControllerEnhanced import PIDControllerEnhanced as controller

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class
else:
    from Modbus import comClient            #Import Modbus Comms Class

        
class PIDControlEnhanced:
        
    def __init__(self):
        # Objects
        self.ext = osTools()            #Initialise data key press
        self.xls = xlsLogging(6)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #Initialise graphical plot
        self.ctrl = controller()        #Initialise PID Controller
        if int(sys.argv[1]) == 1:
            self.r = testModel("../../tests/")        #Initialise simulated lab rig
        else:
            self.rw = comClient()       #Initialise Modbus comms class

        # Variables
        self.count = 0                  #For 'heart beat' counter


    def run(self):
        startTime = time.time()                 #For time reference

        while(True):
            loopTime = time.time()              #Itteration start time
            r = self.readDataPipe()             #Read data

            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot
            u = self.ctrl.runCtrl(r.getRegister(0),r.getRegister(2),r.getRegister(3))       #Run the controller
            self.xls.writeXls(startTime,r,[self.ctrl.spErr,"-"])      #Log data in excel
            
            if int(sys.argv[1]) == 1:
                self.r.writeModel(u)            #Write to model if active
            else:
                self.rw.dataHandler('w',u)      #Write to MODBUS system if active
            
            if self.ext.kbdExit():              #Detect exit condition
                break
            print self.count                    #Heartbeat
            self.count += 1                     #Heartbeat
            time.sleep(self.ctrl.dT - (time.time() - loopTime))
    
    
    def readDataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r') 


def main():
    rp = PIDControlEnhanced()
    rp.run()
    rp.pg.end()
    
if __name__ == '__main__':main()
