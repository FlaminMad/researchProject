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
from Modbus import comClient                #Import Modbus Comms Class
from xlsLogging import xlsLogging
from plotActiveGraph import plotActiveGraph
from neuralNetwork import neuralNetwork

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')
    from testModel import testModel     #Import Simulation Class

        
class researchProjectAIControl:
    
    
    def __init__(self):
        # Objects
        self.rw = comClient()           #Initialise Modbus comms class 
        self.xls = xlsLogging(4)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #Initialise graphical plot
        self.NNctrl = neuralNetwork()        #Initialise Neural Network
        if int(sys.argv[1]) == 1:
            self.r = testModel()        #Initialise simulated lab rig

        # Variables
        self.count = 0                  #For 'heart beat' counter
        self.sampleTime = 10

    def run(self):
        startTime = time.time()         #For time reference

        while(True):
            loopTime = time.time()      #Itteration start time
            r = self.readDataPipe()                 #Read data
            #self.xls.writeXls(startTime,r)      #Log data in excel
            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot
            u = self.NNctrl.activate(r.getRegister(0),r.getRegister(2))
            
            if int(sys.argv[1]) == 1:
                self.r.writeModel(u)            #Write to model
            else:
                self.rw.dataHandler('w',u)      #Write to MODBUS system

            print self.count                    #Heartbeat
            self.count += 1                     #Heartbeat
            time.sleep(self.sampleTime - (time.time() - loopTime))
    
    def readDataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r') 

def main():
    rp = researchProjectAIControl()
    rp.run()
    rp.pg.end()
    
if __name__ == '__main__':main()
