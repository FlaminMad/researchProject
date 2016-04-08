#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   06/03/2016
Rev:    3
Lang:   Python 2.7
Deps:   None
Desc:   Contains Enhanced PID controller class for import
"""

import yaml
import numpy as np

class PIDControllerEnhanced:
     
     def __init__(self):
         self.settings = self._importSettings()
         self.dT = self.settings["dT"]
         self.prevSP = 0
         self.startupFlag = True        # For smooth transitioning
         self.SPC = False
         return
     
     def runCtrl(self,pv,sp,op):
         error = sp - pv                #Calculate error at current time
         self.__tools(pv,sp,op,error)   #Antiwindup, Controller Transision &
                                        #state change algorithms
         if self.settings["ctrlType"] == "P":
             u = self.settings["Kg"]*(error)
         elif self.settings["ctrlType"] == "PI":
             u = self.settings["Kg"]*(error + self.__integral())
         elif self.settings["ctrlType"]  == "PID":
             u = self.settings["Kg"]*(error + self.__integral() + self.__derivitive(pv))
         else:
             raise ValueError('Invalid Control Type - Options are P, PI & PID')
         return self.__vlvLims(u,error)
                  

     def __tools(self,pv,sp,op,error):
         
         if self.startupFlag is True:                       #To help reduce 'bump' in controller changeover
             self.deriv = pv
             self.prevErr = error
             self.__transition(pv,op,error)
             self.startupFlag = False
             
         if self.SPC is True:
             if np.sign(error)!= np.sign(self.prevErr):     #Test for sign change
                 print "Sign Change"
                 if self.settings["tuningMode"] == "N":            
                     self.spErr = (self.settings["M1"]*sp) + self.settings["C1"]
                 else:
                     print "Tuning Mode Active - Mutiplier Ignored"
                 self.SPC = False                           #Reset variable
         
         if sp - self.prevSP != 0:
             print "Set Point Change"
             self.SPC = True
         
         self.prevErr = error
         self.prevSP = sp
         return


     def __integral(self):
         ui = ((self.spErr *self.dT)/self.settings["Ki"])
         return ui
         
     def __derivitive(self,pv):
         #Note: Derivitive takes into account setpoint change spikes by using
         #      the PV instead of error.
         ud = (((self.deriv - pv) * self.settings["Kd"])/self.dT)
         self.deriv = pv
         return ud

     def __transition(self,pv,u,error):  
        # Calculate values for deriv and setErr to ensure seamless bump during
        # controller changover.        
        # PI Control - Calc sp error rounded to 0 d.p
        if self.settings["ctrlType"] == "P":
            self.spErr = 0
            
        elif self.settings["ctrlType"] == "PI" or self.settings["ctrlType"] == "PID":
            self.spErr = np.around(((self.settings["Ki"]/self.dT)*((u/self.settings["Kg"])-error)),0)
            
        else:
            raise ValueError('Invalid Control Type - Options are P, PI & PID')


     def __vlvLims(self,u,error):
         #Enforce Valve Limitations and antiwindup
         if u > self.settings["vlvHighLimit"]:
             self.spErr += (self.settings["antiWindUp"] * error)
             print "High Saturation"
             return self.settings["vlvHighLimit"]
             
         elif u < self.settings["vlvLowLimit"]:
             self.spErr += (self.settings["antiWindUp"] * error)
             print "Low Saturation"
             return self.settings["vlvLowLimit"]
             
         else:
             self.spErr += error
             return u
             
             
     def _importSettings(self):
        try:
            with open("PIDControlSettings.yaml", "r") as f:
                config = yaml.load(f)
        except IOError:
            print("Failed to read On/Off config file")
            raise SystemExit()
        return config