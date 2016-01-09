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
from PIDController import PIDController as controller

import sys ; sys.path.insert(0, '../dataLoggingTool')
from Modbus import comClient                #Import Modbus Comms Class
from xlsLogging4Vars import xlsLogging4Vars
from plotActiveGraph import plotActiveGraph


        
class researchProjectPID:
    
    ctrlType = "PID" #Incorperate control type. Perhaps use as a bool so it
                     #can be modified from a SCADA interface relatively easily?
    
    def __init__(self):
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise PID Controller
        self.ctrl = controller()
        #Initialise excel data logging
        self.xls = xlsLogging4Vars()
        #For graphical plot
        self.pg = plotActiveGraph()

    def run(self):
        #Main Method
        while(True):
            #For controller time loop
            startTime = time.time()
            
            #Read controller data as r     
            try:
                r = self.rw.readData()        
            except:
                print "Modbus Error: Read Connection Failed"
                break

            #Pass data to excel for logging purposes
            self.xls.writeXls(r)

            #Send data to controller
            try:
                u = self.ctrl.runCtrl(r.getRegister(0),r.getRegister(2),r.getRegister(3),self.ctrlType)
            except:
                print "Error: Bad data recieved"
            
            #Update graphical plot
            self.pg.dataUpdate((time.time() - self.xls.startTime),r.getRegister(0),r.getRegister(2),r.getRegister(3))            
            
            #Write output to valve     
            try:
                self.rw.writeData(u)        
            except:
                print "Modbus Error: Write Connection Failed"
                break            
                       
            time.sleep(self.ctrl.dT - (time.time() - startTime))


def main():
    rp = researchProjectPID()
    rp.run()

if __name__ == '__main__':main()
