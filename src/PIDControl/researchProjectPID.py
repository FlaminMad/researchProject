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
from PIDController import PIDController as controller

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel               #Import Simulation Class

        
class researchProjectPID:
    
    
    def __init__(self):
        # Objects
        self.rw = comClient()           #Initialise Modbus comms class 
        self.xls = xlsLogging(4)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #Initialise graphical plot
        self.ctrl = controller()        #Initialise PID Controller
        self.r = testModel()            #Initialise simulated lab rig

        # Variables
        self.count = 0                  #For 'heart beat' counter

    def run(self, sim):
        startTime = time.time()         #For time reference

        while(True):
            loopTime = time.time()      #Itteration start time
            
            if sim:
                self.r.readModel()      #Read simulation data
                self.xls.writeXls(startTime, self.r) #Log data in excel
                self.pg.dataUpdate((time.time() - startTime),self.r.getRegister(0),self.r.getRegister(2),self.r.getRegister(3)) #Add data to plot
                u = self.ctrl.runCtrl(self.r.getRegister(0),self.r.getRegister(2),self.r.getRegister(3))
                self.r.writeModel(u)
                
            else:
                r = self.rw.dataHandler('r')  #Read live data
                self.xls.writeXls(startTime,r)  #Log data in excel
                self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot
                u = self.ctrl.runCtrl(r.getRegister(0),r.getRegister(2),r.getRegister(3))
                self.rw.dataHandler('w',u)

            print self.count            #Heartbeat
            self.count += 1             #Heartbeat
            time.sleep(self.ctrl.dT - (time.time() - loopTime))


def main(sim):
    rp = researchProjectPID()
    rp.run(sim[1])
    rp.pg.end()
    
if __name__ == '__main__':main(sys.argv)
