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
        print "Controller Initialised"

    def run(self,SP,sysID,yt):
        ut = (SP-(sysID[0]*yt))/sysID[1]
        
        if int(sys.argv[1]) == 1:
            lim = 100
        else:
            lim = 1000
        
        #Write Output
        if ut > lim:
            ut = lim
             
        elif ut < 0:
            ut = 0
             
        else:
            ut = ut
        
        return ut