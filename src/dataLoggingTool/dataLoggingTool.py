#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   14/10/2015
@rev:    1
@lang:   Python 2.7
@deps:   Pyserial, Pymodbus
@desc:   Main file for data logging
"""
import sys
import time                                   #Time based functions
from Modbus import comClient                  #Import Modbus Comms Class
from xlsLogging4Vars import xlsLogging4Vars   #Import Excel Logging Class
from plotActiveGraph import plotActiveGraph   #Import Graph Plotting Class
from testModel import testModel               #Import Simulation Class
        
class dataLoggingTool:
    
    def __init__(self):
        # Objects
        self.rw = comClient()           #Initialise Modbus comms class 
        self.xls = xlsLogging4Vars()    #Initialise excel data logging
        self.pg = plotActiveGraph()     #Initialise graphical plot
        self.r = testModel()            #Initialise simulated lab rig

        # Variables
        self.Interval = 5               #For Time Interval
        self.count = 0                  #For 'heart beat' counter
        

    def run(self,sim):
        startTime = time.time()         #For time reference

        while(True):
            loopTime = time.time()      #Itteration start time
            
            if sim:
                self.r.readModel()      #Read simulation data
                self.xls.writeXls(self.r,startTime) #Log data in excel
                self.pg.dataUpdate((time.time() - startTime),self.r.getRegister(0),self.r.getRegister(2),self.r.getRegister(3)) #Add data to plot
                
            else:
                try:
                    r = self.rw.readData()  #Read live controller data as r  
                except:
                    print "Modbus Error: Read Connection Failed"
                    raise SystemExit()
                self.xls.writeXls(r,startTime) #Log data in excel
                self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot                
            
            print self.count            #Heartbeat
            self.count += 1             #Heartbeat
            time.sleep(self.Interval - (time.time() - loopTime))   #Loop Interval


def main(sim):
    rp = dataLoggingTool()
    rp.run(sim[1])
    rp.pg.end()

if __name__ == '__main__':main(sys.argv)
