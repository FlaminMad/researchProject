#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   
Desc:   Contains main PID controller classes for import
"""

class PIDController:
     
     #Adjustable Controller Parameters
     Kp = 1
     Ki = 1
     Kd = 1
     dT = 5             #Time Interval
     sp = 200           #Tank Setpoint

     #Setup Fixed Controller Variables
     spErr = 0.0        # Accumulated setpoint error
     deriv = 0.0        # Pervious setpoint error
     lowLimit = 0       # Cannot drive the valve lower than this
     highLimit = 100    # Cannot drive the valve higher than this
     
     def runCtrl(self,r):
         #Replace 'r[0]' with 'r.getRegister(0)' when using real world comms
         error = r[0] - self.sp
         u = self.proportional(error) + self.integral(error) + self.derivitive(error)
         return u
     
     def proportional(self,err):
         return (self.Kp * err)

     def integral(self,err):
         ui = ((self.spErr *self.dT)/self.Ki)
         self.spErr += err
         return ui
         
     def derivitive(self,err):
         ud = (((err - self.deriv) * self.Kd)/self.dT)
         self.deriv = err
         return ud
         
         
         