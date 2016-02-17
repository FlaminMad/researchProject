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
import numpy as np
from MVController import MVController
from osTools import osTools                 #For detecting exit keypress
from plotActiveGraph import plotActiveGraph #Import Graph Tools Class

if int(sys.argv[1]) == 1:
    sys.path.insert(0, '../../tests')    
    from testModel import testModel         #Import Simulation Class
else:
    from Modbus import comClient            #Import Modbus Comms Class


class minimumVarCtrl:
    def __init__(self):
        # Objects
        self.ext = osTools()                        # Initialise data key press
        self.rls = RLS()                            # Initialise Recursive Least Squares Object
        self.mvctrl = MVController()                # Initialise Controller
        self.pg = plotActiveGraph()                 #For graphical plot (PV,SP,OP)
        if int(sys.argv[1]) == 1:
            self.r = testModel("../../tests/")       # Initialise simulated lab rig
        else:
            self.rw = comClient()                   # Initialise Modbus comms class         
        
        # Variables
        self.ref           = 40                    # Setpoint <TEMPORARY>
        self.count         = 0                     # For 'heart beat' counter
        self.sampleTime    = 40                    # Controller loop time
        return


    def model(self,plantData,sysID):
        return (sysID[0]*plantData.getRegister(0))+\
               (sysID[1]*plantData.getRegister(3))


    def process(self,operation,*ctrlOutput):
        if operation =='r':
            return self.dataPipe()   
        elif operation == 'w':
            if int(sys.argv[1]) == 1:
                self.r.writeModel(ctrlOutput[0])            #Write to model
            else:
                self.rw.dataHandler('w',ctrlOutput[0])      #Write to MODBUS system
        else:
            raise SystemExit("Invalid Operation Detected - Use r or w")


    def dataPipe(self):
        if int(sys.argv[1]) == 1:
            self.r.readModel()
            return self.r
        else:
            return self.rw.dataHandler('r')


    def initialSetup(self):
        self.X = np.array([[0,0,0,0],[0,0,0,0]])
        self.Y = np.array([[0,0,0,0]])
        
        for i in range(0,4):
            r = self.dataPipe()
            self.X[0,i]   = r.getRegister(0)
            self.X[1,i]   = r.getRegister(3)
            if i > 0:
                self.Y[:,i-1] = self.X[0,i]
            time.sleep(self.sampleTime)
            
        r = self.dataPipe()
        self.Y[:,3] = r.getRegister(0)
        print self.X
        print self.Y
        self.rls.setup(self.X,np.matrix.transpose(self.Y))
        print "Setup Complete"
    
    def run(self):
        startTime = time.time()
        processOutput = self.process('r')                                   #Read process values
        self.modelOutput = self.model(processOutput, self.rls.sysID)
        
        while(True):
            loopTime = time.time()
            processOutput = self.process('r')                               #Read process values
            self.pg.dataUpdate((time.time() - startTime),\
                                processOutput.getRegister(0),\
                                processOutput.getRegister(2),\
                                processOutput.getRegister(3),\
                                self.rls.sysID[0],\
                                self.rls.sysID[1])            

            modelError = processOutput.getRegister(0) - self.modelOutput    #Drawing ID 'F'
            print modelError            
            #Drawing ID 'D'
            self.rls.solve(np.array([processOutput.getRegister(0),\
                                     processOutput.getRegister(3)]), modelError)
                                     
            ctrlOutput = self.mvctrl.run(processOutput.getRegister(2),\
                                         self.rls.sysID,\
                                         processOutput.getRegister(0))      #Drawing ID 'C'
            
            self.process('w',ctrlOutput)                                    #Drawing ID 'A' & 'B' - Write
            self.modelOutput = self.model(processOutput, self.rls.sysID)    #Read model estimate of process output
            time.sleep(self.sampleTime - (time.time() - loopTime))          #Loop Sleepy Time
            
            if self.ext.kbdExit():              #Detect exit condition
                break

        
def main():
    mvc = minimumVarCtrl()
    mvc.initialSetup()
    mvc.run()
    mvc.pg.end()

if __name__ == '__main__':main()