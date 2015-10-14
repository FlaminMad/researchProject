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

		
if __name__ == '__main__':
    #Initialise Modbus comms class    
    rw = comClient()
    #Initialise PID Controller
    ctrl = controller()
    
    #Main Method
    while(True):
        #For controller time loop
        startTime = time.time()
        
        #Read Controller data as r (Mock in this case)
        r = [199,0,0,356]
        
        #Send data to controller
        u = ctrl.runCtrl(r)
        
        #Write output to valve
        #Replace with 'rw.writeData(u)' when using real world comms
        print u
                
        time.sleep(ctrl.dT - (time.time() - startTime))
        
        
#Add Back In To Enable Real World Comms        
"""        
        #Read controller data        
        try:
            r = rw.getData()        
        except:
		print "Modbus Error: Connection Failed"
		break
"""