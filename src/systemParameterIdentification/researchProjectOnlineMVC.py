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

import time                                 #Time based functions
from Modbus import comClient                #Import Modbus Comms Class
from RLS import RLS                         #Import Recursive Least Squares
from xlsLogging import xlsLogging           #Import Data Logging Class
import numpy as np                          #Import numpy for array & matrices


class liveSystemParamID: 

    sampleTime = 30

    def __init__(self):
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise Recursive Least Squares Object
        self.rls = RLS()
        #Initialise excel data logging
        self.xls = xlsLogging()

    def run(self):
        #Take already setup algorithm and incorperate
        y = self.Y[:,2]
        x = np.array([self.X[0,2],self.X[1,2]])
        #Main Method
        print "Running Main Method..."        
        while(True):
            #Controller time loop
            startTime = time.time()
        
            #Read controller data as r
            r = self.rw.readData()
           
            #Update y value
            y = np.array([r.getRegister(0)])
            
            #Call recursive least squares method using y and x '-1'
            self.rls.solve(x,y)
       
            #Pass data to excel for logging purposes
            self.xls.writeXls(r,self.rls.sysID)
            
            #Update x values
            x = np.array([r.getRegister(0),r.getRegister(3)])  
            
            #Remove later, for debugging only
            print self.rls.sysID
            
            #Controller time keeping loop
            time.sleep(self.sampleTime - (time.time() - startTime))
       
       
    def initialSetup(self):
            self.X = np.array([[0,0,0],[0,0,0]])
            self.Y = np.array([[0,0,0]])
            r = self.rw.readData()
            self.X[0,0] = r.getRegister(0)
            self.X[1,0] = r.getRegister(3)
            
            for i in range(1,3):         
                r = self.rw.readData()
                self.X[0,i]   = r.getRegister(0)
                self.X[1,i]   = r.getRegister(3)
                self.Y[:,i-1] = self.X[0,i]
                time.sleep(self.sampleTime)
            r = self.rw.readData()
            self.Y[:,2] = r.getRegister(0)
      
            self.rls.setup(self.X,np.matrix.transpose(self.Y))
            print "Setup Complete"
       
def main():
    print "Starting"
    ID = liveSystemParamID()
    print "Please wait, Reading Initial Parameters..."
    ID.initialSetup()
    print "Done"
    ID.run()

if __name__ == '__main__':main()    