#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   18/01/2016
@rev:    1
@lang:   Python 2.7
@deps:   Numpy, YAML
@desc:   Simulated system for usage in offline tests
         Make sure that the object is initiliased as 'r' so as to avoid code
         changes elsewhere
"""

import time
import yaml
import numpy as np

class testModel:
    
    def __init__(self):
        self.mdlConf = self.__importSettings("../../tests/testSysParams.yaml")
        self.sp = self.__importSettings("../../tests/sp.yaml")['sp']
        self.Av = (np.pi*np.square(self.mdlConf['outDiam']))/4
        self.h = self.mdlConf['hInitial']
        self.__updateFlow(self.mdlConf['uInitial'])
        self.refTime = time.time()
        self.__modelSys()
        print "Simulation Running"
        return

    def __importSettings(self, filename):
        try:
            with open(filename, 'rb') as f:
                settings = yaml.load(f)
                return settings
        except IOError:
            print("Failed to read config file")
            raise SystemExit()
      
    
    def __modelSys(self):
        #Note: contains time critical equation
        timeNow = time.time()
        self.h += (timeNow-self.refTime)*(self.qin - self.Av*np.sqrt(19.62*self.h))/self.mdlConf['tankArea']   
        self.refTime = timeNow
        return
    
    def __updateFlow(self,u):
        self.u = u
        ux = float(u/100.0)
        self.qin = (0.2693*(ux*ux*ux))-(0.0279*(ux*ux))+(0.0046*ux)
        if self.qin > 0.01731:
            self.qin = 0.01731
        return
    
    def readModel(self):
        self.__modelSys()
        self.sp = self.__importSettings("../../tests/sp.yaml")['sp']
        return

    def writeModel(self,u):
        self.__modelSys()
        self.__updateFlow(u)
        return

    def getRegister(self,i):
        # Method to maintain compatibility with the modbus returned data type
        return [self.h, 0, self.sp, self.u][i]