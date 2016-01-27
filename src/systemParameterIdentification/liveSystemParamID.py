#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   21/01/2016
Rev:    2
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   System Parameter identification using RLS based on MODBUS data comms
"""

import time                                 #Time based functions
import numpy as np                          #Import numpy for array & matrices
from RLS import RLS                         #Import Recursive Least Squares

import sys ; sys.path.insert(0, '../dataLoggingTool')
from Modbus import comClient                #Import Modbus Comms Class
from xlsLogging import xlsLogging           #Import Data Logging Class
from plotActiveGraph import plotActiveGraph #Graphing Tools

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class


class liveSystemParamID: 

    def __init__(self):
        # Objects
        self.rw = comClient()           #Initialise Modbus comms class 
        self.xls = xlsLogging(6)        #Initialise excel data logging
        self.pg = plotActiveGraph()    #For graphical plot (PV,SP,OP)
        self.rls = RLS()                #Initialise Recursive Least Squares Object
        if int(sys.argv[1]) == 1:
            self.r = testModel()        #Initialise simulated lab rig

        # Variables
        self.count = 0                  #For 'heart beat' counter
        self.sampleTime = 30            #Controller loop time

    def run(self):
        startTime = time.time()         #For time reference    
        y = self.Y[:,2]                 #Transition setup values into the main loop
        x = np.array([self.X[0,2],self.X[1,2]])

        while(True):
            loopTime = time.time()              #Itteration start time
            
            r = self.dataPipe()                 #Read controller data as r
            y = np.array([r.getRegister(0)])    #Update y value
            self.rls.solve(x,y)                 #Call recursive least squares method using y and x '-1'
            x = np.array([r.getRegister(0),r.getRegister(3)])   #Update x values            
            self.xls.writeXls(startTime,r,self.rls.sysID) #Pass data to excel for logging purposes
            self.pg.dataUpdate((time.time() - startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3),self.rls.sysID[0],self.rls.sysID[1])

           
            print self.count            #Heartbeat
            self.count += 1             #Heartbeat
            time.sleep(self.sampleTime - (time.time() - loopTime))
       
       
    def initialSetup(self):
            self.X = np.array([[0,0,0,0],[0,0,0,0]])
            self.Y = np.array([[0,0,0,0]])
            
            for i in range(0,4):
                r = self.dataPipe()
                self.X[0,i]   = r.getRegister(0)
                self.X[1,i]   = r.getRegister(3)
                if i > 0:
                    self.Y[:,i-1] = self.X[0,i]
                time.sleep(self.sampleTime)
                
            r = self.dataPipe()
            self.Y[:,3] = r.getRegister(0)
            print self.X
            print self.Y
            self.rls.setup(self.X,np.matrix.transpose(self.Y))
            print "Setup Complete"
       
    def dataPipe(self):
        if int(sys.argv[1]) == 1:
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