#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Main file for data logging
"""

import time                                                                    #Time based functions
from Modbus import comClient                                                   #Import Modbus Comms Class
from xlsLogging import xlsLogging

        
class dataLoggingTool:
    
    def __init__(self):
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise excel data logging
        self.xls = xlsLogging()
        #For Time Interval
        self.Interval = 5      
        #For 'heart beat' counter
        self.count = 0

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

            print self.count
            self.count += 1
             
            time.sleep(self.Interval - (time.time() - startTime))


def main():
    rp = dataLoggingTool()
    rp.run()

if __name__ == '__main__':main()
