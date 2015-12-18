#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pyserial, Pymodbus
Desc:   Main file for PID Controller
"""

class MVControllerInc:

    def __init__(self,u):
        print "Controller Initialised"
        self.ut = u  # Implement Functionality

    def run(self,SP,sysID,yt):
        
        iut = (SP-(sysID[0]*yt))/sysID[1]
        
        self.ut = self.ut + iut        
        
        #Write Output
        if self.ut > 1000:
            self.ut = 1000
             
        elif self.ut < 0:
            self.ut = 0
             
        else:
            self.ut = self.ut
        
        return self.ut