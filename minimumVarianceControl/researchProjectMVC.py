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
            for i in range(3, 30):
                x = self.X[:,i]
                y = self.Z[:,i]
                
                self.rls.solve(x,y)
            print "Done, SysID is:"
            print self.rls.sysID
            break
            
    def testData(self):
        U = np.array([[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40]])
        Y = np.array([[50,65.0,78.5,90.7,101.6,111.4,120.3,128.3,135.4,141.9,147.7,152.9,157.6,161.9,165.7,169.1,172.2,175.0,177.5,179.7,181.8,183.6,185.2,186.7,188.0,189.2,190.3,191.3,192.1,192.9,193.6]])
        self.Z = np.array([[65.0,78.5,90.7,101.6,111.4,120.3,128.3,135.4,141.9,147.7,152.9,157.6,161.9,165.7,169.1,172.2,175.0,177.5,179.7,181.8,183.6,185.2,186.7,188.0,189.2,190.3,191.3,192.1,192.9,193.6,194.3]])
        self.X = np.concatenate((U,Y), axis=0)        
        
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