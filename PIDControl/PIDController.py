#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
"""

import time                                                                    #Time based functions
from Modbus import comClient                                                   #Import Modbus Comms Class
from PID import PIDController as controller

        
class researchProject:
    
    def __init__():
        #Initialise Modbus comms class    
        self.rw = comClient()
        #Initialise PID Controller
        self.ctrl = controller()

    def run():
        #Main Method
        while(True):
            #For controller time loop
            startTime = time.time()
            
            #Read Controller data as r (Mock in this case)
            r = [199,0,0,356]
            
            #Send data to controller
            u = self.ctrl.runCtrl(r)
            
            #Write output to valve
            #Replace with 'self.rw.writeData(u)' when using real world comms
            print u
                    
            time.sleep(self.ctrl.dT - (time.time() - startTime))
            
            
            #Add Back In To Enable Real World Comms        
            """        
            #Read controller data        
            try:
                r = self.rw.getData()        
            except:
            print "Modbus Error: Connection Failed"
            break
            """

def main():
    rp = researchProject()
    rp.run()

if __name__ == '__main__':main()
