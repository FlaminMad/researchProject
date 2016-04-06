#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    2
Lang:   Python 2.7
Deps:   None
Desc:   Contains PID controller class for import
"""

import numpy as np

class PIDController:
     
     #Adjustable Controller Parameters
     Kg = 8.29
     Ki = 24.11
     Kd = 3.58
     dT = 5             #Time Interval
     antiWindUp = 0     #Anti-Windup (Between 0.05 & 0.25)
     
     #Experimental Params
    

     #Setup Fixed Controller Variables
     lowLimit = 0       # Valve low limit
     highLimit = 100   # Valve high limit
     startupFlag = True    # For smooth transitioning
     spErr = 0
     ctrlType = "PID"
     
     
     def runCtrl(self,pv,sp,op):
         #Calculate error at current time
         error = sp - pv
         
         #To help reduce 'bump' in controller changeover
         if self.startupFlag is True:
             self.__transition(error,pv,op)
             self.startupFlag = False
         
         #Run main PID algorithm based on selected type
         if self.ctrlType == "P":
             u = self.Kg*(error)
         elif self.ctrlType == "PI":
             u = self.Kg*(error + self.__integral(error))
         elif self.ctrlType == "PID":
             u = self.Kg*(error + self.__integral(error) + self.__derivitive(pv))
         else:
             raise ValueError('Invalid Control Type - Options are P, PI & PID')
             
         #Enforce Valve Limitations and antiwindup
         if u > self.highLimit:
             self.spErr += (self.antiWindUp * error)
             print "High Saturation"
             return 100
             
         elif u < self.lowLimit:
             self.spErr += (self.antiWindUp * error)
             print "Low Saturation"
             return 0
             
         else:
             self.spErr += error
             return u


     def __integral(self,err):
         ui = ((self.spErr *self.dT)/self.Ki)
         return ui
         
     def __derivitive(self,pv):
         #Note: Derivitive takes into account setpoint change spikes by using
         #      the PV instead of error.
         ud = (((self.deriv - pv) * self.Kd)/self.dT)
         self.deriv = pv
         return ud

     def __transition(self,err,pv,u):  
        # Calculate values for deriv and setErr to ensure seamless bump during
        # controller changover.
        self.deriv = pv
        
        #PI Control - Calc sp error rounded to 0 d.p
        if self.ctrlType == "P":
            self.spErr = 0
            
        elif self.ctrlType == "PI":
            self.spErr = np.around(((self.Ki/self.dT)*((u/self.Kg)-err)),0)
            
        elif self.ctrlType == "PID":
            self.spErr = np.around(((self.Ki/self.dT)*((u/self.Kg)-err)),0)
            
        else:
            raise ValueError('Invalid Control Type - Options are P, PI & PID')