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
    
    ctrlType = "PID" #Incorperate control type. Perhaps use as a bool so it
                     #can be modified from a SCADA interface relatively easily?
    
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
            for i in range(3, 155):
                x = self.X[:,i]
                y = self.Z[:,i]
                
                self.rls.solve(x,y)
                print x
                print y
                print self.rls.sysID
            print "Done, SysID is:"
            print self.rls.sysID
            break
            
    def testData(self):
        U = np.array([[350,350,350,350,350,350,350,350,350,350,350,350,350,350,350,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400,400]])
        Y = np.array([[90,90,91,87,95,93,100,87,93,86,87,94,91,91,97,92,104,109,115,123,126,134,131,146,149,154,163,170,178,180,180,193,194,203,209,212,210,218,230,239,240,241,245,247,251,263,259,271,273,274,278,284,281,294,298,302,303,305,308,309,320,321,322,326,327,333,336,337,343,350,352,353,358,358,363,366,365,367,367,372,376,374,382,378,387,388,389,392,394,397,399,402,396,402,401,403,407,410,415,421,423,418,418,427,427,427,426,426,429,429,432,427,429,429,430,432,434,434,433,436,437,447,448,436,442,454,446,445,452,448,448,447,456,454,456,457,458,457,459,459,460,460,463,460,460,463,466,465,458,467,463,464,464,471,466]])
        self.Z = np.array([[90,91,87,95,93,100,87,93,86,87,94,91,91,97,92,104,109,115,123,126,134,131,146,149,154,163,170,178,180,180,193,194,203,209,212,210,218,230,239,240,241,245,247,251,263,259,271,273,274,278,284,281,294,298,302,303,305,308,309,320,321,322,326,327,333,336,337,343,350,352,353,358,358,363,366,365,367,367,372,376,374,382,378,387,388,389,392,394,397,399,402,396,402,401,403,407,410,415,421,423,418,418,427,427,427,426,426,429,429,432,427,429,429,430,432,434,434,433,436,437,447,448,436,442,454,446,445,452,448,448,447,456,454,456,457,458,457,459,459,460,460,463,460,460,463,466,465,458,467,463,464,464,471,466,469]])
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