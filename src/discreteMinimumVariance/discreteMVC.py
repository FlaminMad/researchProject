#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Main file for discrete minimum variance controller using online
        learning with recursive least squares
"""

import time                                 #Time based functions
import numpy as np                          #Import numpy for array & matrices
from MVController import MVController

import sys ; sys.path.insert(0, '../dataLoggingTool')
import sys ; sys.path.insert(0, '../systemParameterIdentification')
from RLS import RLS                         #Import Recursive Least Squares
from Modbus import comClient                #Import Modbus Comms Class
from xlsLogging import xlsLogging           #Import Data Logging Class
from plotActiveGraph import plotActiveGraph

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class

class discreteMVC:

    sampleTime = 40

    def __init__(self):
        # Objects
        self.rw = comClient()           #Initialise Modbus comms class 
        self.xls = xlsLogging(6)        #Initialise excel data logging
        self.pg = plotActiveGraph()     #For graphical plot (PV,SP,OP)
        self.rls = RLS()                #Initialise Recursive Least Squares Object
        self.MVC = MVController()       #Initialise Controller        
        if int(sys.argv[1]) == 1:
            self.r = testModel()        #Initialise simulated lab rig

        # Variables
        self.count = 0                  #For 'heart beat' counter
        self.sampleTime = 30            #Controller loop time       
       
        
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
            
            #Update graphical plot
            self.pgA.dataUpdate((time.time() - self.xls.startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))
            self.pgB.dataUpdate((time.time() - self.xls.startTime),self.rls.sysID[0],self.rls.sysID[1])
            
            #Call Controller
            ut = self.MVC.run(r.getRegister(2),(self.rls.sysID),r.getRegister(0))            
            
            #Write Ouput to valve (Limits already enforced by MVC method)
            self.rw.writeData(ut) 

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
    dmvc = discreteMVC()
    print "Please wait, Reading Initial Parameters..."
    dmvc.initialSetup()
    print "Done"
    dmvc.run()

if __name__ == '__main__':main()