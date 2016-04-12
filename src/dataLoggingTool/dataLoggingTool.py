#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   14/10/2015
@rev:    1
@lang:   Python 2.7
@deps:   Pyserial, Pymodbus, openpyxl, matplotlib, numpy
@desc:   Main file for data logging
"""
import sys                                      #System Functions Import 
import time                                     #Time based functions
from osTools import osTools                     #For detecting exit keypress
from xlsLogging import xlsLogging               #Import Excel Logging Class
from plotActiveGraph import plotActiveGraph     #Import Graph Plotting Class

if int(sys.argv[1]) == 1:                       #Test if in 'simulation' mode
    sys.path.insert(0, '../../tests')    
    from testModel import testModel             #Import Simulation Class
else:
    from Modbus import comClient                #Import Modbus Comms Class


class dataLoggingTool:
    
    def __init__(self):
        # Objects
        self.ext = osTools()                    #Initialise data key press
        self.xls = xlsLogging(4)                #Initialise excel data logging
        self.pg = plotActiveGraph()             #Initialise graphical plot
        if int(sys.argv[1]) == 1:
            self.r = testModel("../../tests/")  #Initialise simulated lab rig
        else:
            self.rw = comClient()               #Initialise Modbus comms class

        # Variables
        self.Interval = 5                       #For Time Interval
        self.count = 0                          #'Heart beat' counter start number
        

    def run(self):
        startTime = time.time()                 #For time reference

        while(True):
            loopTime = time.time()              #Itteration start time
            r = self.dataPipe()                 #Read live controller data as r
            self.xls.writeXls(startTime,r)      #Log data in excel
            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))    #Add data to plot                
            
            if self.ext.kbdExit():              #Detect exit condition
                break
            print self.count                    #Heartbeat
            self.count += 1                     #Heartbeat
            time.sleep(self.Interval - (time.time() - loopTime))   #Loop Interval


    def dataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()                  #Read data from test model
            return self.r                       #Return test model data
        else:
            return self.rw.dataHandler('r')     #Return data from MOBUS comms


def main():
    rp = dataLoggingTool()                      #Initialise the data logging tool class
    rp.run()                                    #Run main method
    rp.pg.end()                                 #Keep data plot open until exit

if __name__ == '__main__':main()
