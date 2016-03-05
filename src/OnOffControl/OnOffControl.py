#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   05/03/2016
Rev:    2
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Main file for On/Off control
"""

import time
import sys ; sys.path.insert(0, '../dataLoggingTool')
from osTools import osTools
from xlsLogging import xlsLogging
from plotActiveGraph import plotActiveGraph
from OnOffController import OnOffController

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class
else:
    from Modbus import comClient            #Import Modbus Comms Class

        
class OnOffControl:
        
    def __init__(self):
        # Objects
        self.ext = osTools()            #Initialise data key press
        self.xls = xlsLogging(4)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #Initialise graphical plot
        self.ctrl = OnOffController()   #Initialise Controller
        if int(sys.argv[1]) == 1:
            self.r = testModel("../../tests/")  #Initialise simulated lab rig
        else:
            self.rw = comClient()               #Initialise Modbus comms class

        # Variables
        self.count = 0                          #For 'heart beat' counter
        self.cycleTime = 10                     #For Control Loop Interval


    def run(self):
        startTime = time.time()                 #For time reference
        while(True):
            loopTime = time.time()              #Itteration start time
            r = self.readDataPipe()             #Read data
            self.xls.writeXls(startTime,r)      #Log data in excel
            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot
            u = self.ctrl.run(r)                #Run controller
            
            if int(sys.argv[1]) == 1:
                self.r.writeModel(u)            #Write to model
            else:
                self.rw.dataHandler('w',u)      #Write to MODBUS system            
            
            if self.ext.kbdExit():              #Detect exit condition
                break            
            print self.count                    #Heartbeat
            self.count += 1                     #Heartbeat
            time.sleep(self.cycleTime - (time.time() - loopTime))
    
    
    def readDataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r') 


def main():
    OnOff = OnOffControl()
    OnOff.run()
    OnOff.pg.end()
    
if __name__ == '__main__':main()
