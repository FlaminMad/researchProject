#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   None
Desc:   Contains PID controller class for import
"""

class PIDController:
     
     #Adjustable Controller Parameters
     Kp = 1
     Ki = 102.618
     Kd = 1
     dT = 5             #Time Interval
     antiWindUp = 0.2   #Anti-Windup (Between 0.05 & 0.25)

     #Setup Fixed Controller Variables
     lowLimit = 0       # Valve low limit
     highLimit = 1000   # Valve high limit
     startupFlag = True    # For smooth transitioning
     
     
     def runCtrl(self,pv,sp):
         #Calculate error at current time
         error = sp - pv
         
         #To help reduce 'bump' in controller changeover
         if self.startupFlag is True:
             self.__transition(error)
             self.startupFlag = False
             print self.startupFlag
         
         #Run main PID algorithm - Comment out P, I, D methods as necessary
         u = self.__proportional(error) \
           + self.__integral(error)     \
#           + self.__derivitive(pv)
             
         #Enforce Valve Limitations and antiwindup
         if u > self.highLimit:
             self.spErr += (self.antiWindUp * error)
             return 1000
         elif u < self.lowLimit:
             self.spErr += (self.antiWindUp * error)
             return 0
         else:
             self.spErr += error
             print self.spErr
             return u
     
     
     def __proportional(self,err):
         return (self.Kp * err)

     def __integral(self,err):
         ui = ((self.spErr *self.dT)/self.Ki)
         return ui
         
     def __derivitive(self,pv):
         #Note: Derivitive takes into account setpoint change spikes by using
         #      the PV instead of error.
         ud = (((self.deriv - pv) * self.Kd)/self.dT)
         self.deriv = pv
         return ud

     def __transition(self,err):
        self.spErr = err        # Accumulated setpoint error
        self.deriv = err        # Pervious setpoint error
