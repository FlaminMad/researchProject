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

import sys

class MVController:

    def __init__(self):
        #Set vlv limits based upon system thats running
        if int(sys.argv[1]) == 1:
            self.vlvLim = 100
        else:
            self.vlvLim = 1000

    def run(self,yt,sp,sysID):
        #Controller Algorithm
        ut = (sp-(sysID[0]*yt))/sysID[1]
        
        #Enforce Valve Limits & Write Output
        if ut > self.vlvLim:
            return self.vlvLim
        elif ut < 0:
            return 0
        else:
            return ut