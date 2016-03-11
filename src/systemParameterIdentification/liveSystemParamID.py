#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   11/03/2016
Rev:    3
Lang:   Python 2.7.11
Deps:   Pymodbus
Desc:   System Parameter identification using RLS based on MODBUS data comms
"""

import time                                 #Time based functions
import numpy as np                          #Import numpy for array & matrices
from RLS import RLS                         #Import Recursive Least Squares

import sys ; sys.path.insert(0, '../dataLoggingTool')
from osTools import osTools                 #For detecting exit keypress
from xlsLogging import xlsLogging           #Import Data Logging Class
from plotActiveGraph import plotActiveGraph #Graphing Tools

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class
else:
    from Modbus import comClient            #Import Modbus Comms Class


class liveSystemParamID: 

    def __init__(self):
        # Objects
        self.ext = osTools()            #Initialise data key press
        self.xls = xlsLogging(6)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #For graphical plot (PV,SP,OP)
        self.rls = RLS()                #Initialise Recursive Least Squares Object
        if int(sys.argv[1]) == 1:
            self.r = testModel("../../tests/")              #Initialise simulated lab rig
        else:
            self.rw = comClient()       #Initialise Modbus comms class

        # Variables
        self.count = 0                  #For 'heart beat' counter
        self.intDataPoints = 4          #Initial Data Points to be read
        self.sampleTime = 10            #Calculation loop time

    def run(self):
        z = np.array([[0,self.X[0,self.intDataPoints-1]],[0,self.X[1,self.intDataPoints-1]]])     #Array in the form Yt, Ut      
        time.sleep(self.sampleTime - (time.time()-self.timer))
        startTime = time.time()                             #For time reference
        
        while(True):
            loopTime = time.time()                          #Itteration start time
            r = self.dataPipe()                             #Read controller data as r
            z[:,0] = z[:,1]                                 #Shift Array
            z[:,1] = r.getRegister(0),r.getRegister(3)      #Update Array
            self.rls.solve(z[:,0],z[0,1])                   #Call recursive least squares method
            self.xls.writeXls(startTime,r,self.rls.sysID)   #Pass data to excel for logging purposes
            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3),self.rls.sysID[0],self.rls.sysID[1])
            if self.ext.kbdExit():                          #Detect exit condition
                break
            print self.count                                #Heartbeat
            self.count += 1                                 #Heartbeat
            time.sleep(self.sampleTime - (time.time() - loopTime))
       
    def initialSetup(self):
            self.X = np.array([np.zeros(self.intDataPoints),np.zeros(self.intDataPoints)])
            self.Y = np.array([np.zeros(self.intDataPoints)])
            
            for i in range(0,self.intDataPoints):
                r = self.dataPipe()
                self.X[0,i]   = r.getRegister(0)
                self.X[1,i]   = r.getRegister(3)
                if i > 0:
                    self.Y[:,i-1] = self.X[0,i]
                if i < (self.intDataPoints-1):
                    time.sleep(self.sampleTime)
            self.timer = time.time()
            self.rls.setup(self.X[:,:-1],np.matrix.transpose(self.Y[:,:-1]))
            print "Setup Complete"
            
    def dataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r')
       
       
def main():
    print "Starting"
    ID = liveSystemParamID()
    print "Please wait, Reading Initial Parameters..."
    ID.initialSetup()
    print "Running Main Method..."
    ID.run()
    ID.pg.end()

if __name__ == '__main__':main()    