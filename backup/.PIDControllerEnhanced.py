#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   05/03/2016
Rev:    2
Lang:   Python 2.7
Deps:   None
Desc:   Contains Enhanced PID controller class for import
"""

import numpy as np

class PIDController:
     
     def __init__(self):
         self.startupFlag = True        # For smooth transitioning
         self.prevSP = 0                # For SP change detection
         pass
     
     def runCtrl(self,pv,sp,op):
         error = sp - pv                #Calculate error at current time
         self.__tools(pv,sp,op,error)   #Antiwindup, Controller Transision &
                                        #state change algorithms
         if self.ctrlType == "PI":  
             u = self.Kg*(error + self.__integral(error))
         elif self.ctrlType == "PID":
             u = self.Kg*(error + self.__integral(error) + self.__derivitive(pv))
         else:
             raise ValueError('Invalid Control Type - Options are PI & PID')
            
         return self.__vlvLims(u,error)
                  

     def __tools(self,pv,sp,op,error):
         
         if self.startupFlag is True:                       #To help reduce 'bump' in controller changeover
             self.deriv = pv
             self.prevErr = error
             self.__transition(pv,op,error)
             print " Startup Flag"
             self.startupFlag = False
             
         if sp - self.prevSP != 0:                          #Testing Methods
             print " Set Point Change"
             self.setPointChange = True
        
         if self.setPointChange is True:
             print "Waiting..."
             if np.sign(error)!= np.sign(self.prevErr):     #Test for sign change
                 print "Sign Change"                 
                 #self.__transition(pv,op,error)             #Re-calculate spErr
                 print self.spErr
                 self.setPointChange = False                #Reset variable
         
         self.prevErr = error
         self.prevSP = sp
         return


     def __integral(self,err):
         ui = ((self.spErr *self.dT)/self.Ki)
         return ui
         
     def __derivitive(self,pv):
         #Note: Derivitive takes into account setpoint change spikes by using
         #      the PV instead of error.
         ud = (((self.deriv - pv) * self.Kd)/self.dT)
         self.deriv = pv
         return ud

     def __transition(self,pv,u,error):  
        # Calculate values for deriv and setErr to ensure seamless bump during
        # controller changover.        
        # PI Control - Calc sp error rounded to 0 d.p
        if self.ctrlType == "PI":
            self.spErr = np.around(((self.Ki/self.dT)*((u/self.Kg)-error)),0)
            
        elif self.ctrlType == "PID":
            self.spErr = np.around((self.Ki/self.dT)*((u/self.Kg)-error-((self.deriv*self.Kd)/self.dT)),0)
        
        else:
            raise ValueError('Invalid Control Type - Options are PI & PID')


     def __vlvLims(self,u,error):
         #Enforce Valve Limitations and antiwindup
         if u > self.highLimit:
             self.spErr += (self.antiWindUp * error)
             print "High Alarm"
             return 100
             
         elif u < self.lowLimit:
             self.spErr += (self.antiWindUp * error)
             print "Low Alarm"
             return 0
             
         else:
             self.spErr += error
             return u     