#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   06/02/2016
Rev:    1
Lang:   Python 2.7.11
Deps:   Some kind of brain <error 404>
Desc:   Trying to get my head around what the hell I've done and how on
        earth I should be doing what I want to
"""

import sys, time
sys.path.insert(0, '../dataLoggingTool')
sys.path.insert(0, '../systemParameterIdentification')
from RLS import RLS                         #Import Recursive Least Squares
from MVController import MVController
from osTools import osTools                 #For detecting exit keypress
if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class
else:
    from Modbus import comClient            #Import Modbus Comms Class


class minimumVarCtrl:
    def __init__(self):
        # Objects
        self.ext = osTools()            #Initialise data key press
        self.rls = RLS()                #Initialise Recursive Least Squares Object
        self.mvctrl = MVController()       #Initialise Controller
        self.initialSetup()
        if int(sys.argv[1]) == 1:
            self.r = testModel()        #Initialise simulated lab rig
        else:
            self.rw = comClient()           #Initialise Modbus comms class         
        
        # Variables
        self.ref            = 400
        self.ctrlOutput     = 1
        self.tuningParams   = [1,0] 
        self.processOutput  = self.
        return

    def initialSetup(self):
        self.ref            =  400
        self.ctrlOutput     = 1
        self.tuningParams   = [1,0] 
        self.processOutput  = 1
        return


    def model(self,plantData,sysID):
#       Drawing ID 'A'
        return (sysID[0]*plantData[0])+(sysID[1]*plantData[3])


    def process(self):
#       Drawing ID 'B'
        return self.dataPipe()


    def dataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r')

    
    def run(self):
        while(True):
            #Drawing ID 'E'
            procError = self.ref - self.processOutput
            
            #Drawing ID 'C'
            ctrlOutput = self.mvctrl.run(procError,self.tuningParams)
            
            #Drawing ID 'A' & 'B'
            processOutput = self.process(ctrlOutput, self.tuningParams)
            modelOutput = self.model(ctrlOutput, self.tuningParams)
            
            #Drawing ID 'F'
            modelError = processOutput - modelOutput
            
            #Drawing ID 'D'
            self.tuningParams = self.rls.solve(modelError)


def main():
    mvc = minimumVarCtrl()
    mvc.run()
    print "Exit"

if __name__ == '__main__':main()