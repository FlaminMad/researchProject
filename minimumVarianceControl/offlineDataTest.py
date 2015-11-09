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

#import time                                                                    #Time based functions
from Modbus import comClient                                                   #Import Modbus Comms Class
from RLS import RLS
#from xlsLogging import xlsLogging
import numpy as np

        
class researchProjectMVC:
    
    
    def __init__(self):
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise Recursive Least Squares Object
        self.rls = RLS()
        #Initialise excel data logging
#        self.xls = xlsLogging()

    def run(self):
        #Main Method
        
        self.testData()

        self.rls.setup(self.X,np.matrix.transpose(self.Z))

        while(True):
            for i in range(3, 130):
                x = self.X[:,i]
                y = self.Z[:,i]
                
                self.rls.solve(x,y)
                print self.rls.sysID
            print "Done, SysID is:"
            print self.rls.sysID
            break
            
    def testData(self):
        U = np.array([[350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400]])
        Y = np.array([[99,94,100,103,95,95,104,89,90,92,89,86,92,96,97,94,96,92,88,85,87,93,104,110,114,122,130,130,138,144,151,155,165,173,177,179,183,192,200,208,207,211,223,225,230,237,238,249,252,261,266,263,268,270,274,284,292,298,300,305,301,307,303,314,317,326,328,328,331,330,332,338,342,343,351,355,357,354,360,360,366,366,371,368,371,371,380,381,389,389,392,388,393,397,398,398,402,399,406,411,411,417,416,416,420,422,422,424,423,424,426,428,428,428,428,430,433,436,428,430,438,441,447,447,444,449,451,452,448,453,455]])
        self.Z = np.array([[94,100,103,95,95,104,89,90,92,89,86,92,96,97,94,96,92,88,85,87,93,104,110,114,122,130,130,138,144,151,155,165,173,177,179,183,192,200,208,207,211,223,225,230,237,238,249,252,261,266,263,268,270,274,284,292,298,300,305,301,307,303,314,317,326,328,328,331,330,332,338,342,343,351,355,357,354,360,360,366,366,371,368,371,371,380,381,389,389,392,388,393,397,398,398,402,399,406,411,411,417,416,416,420,422,422,424,423,424,426,428,428,428,428,430,433,436,428,430,438,441,447,447,444,449,451,452,448,453,455,454]])
        self.X = np.concatenate((Y,U), axis=0)
        
def main():
    rp = researchProjectMVC()
    rp.run()

if __name__ == '__main__':main()








#For implementation in real life scenario
'''           
            #Read controller data as r     
            try:
                r = self.rw.readData()        
            except:
                print "Modbus Error: Read Connection Failed"
                break


            #Pass data to excel for logging purposes
            self.xls.writeXls(r)
            
            
            #Write output to valve     
            try:
                self.rw.writeData(u)        
            except:
                print "Modbus Error: Write Connection Failed"
                break 

            #Controller time loop
            startTime = time.time()
            
                        
            
            time.sleep(self.ctrl.dT - (time.time() - startTime))

'''    