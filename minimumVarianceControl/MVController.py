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

class MVController:

    def __init__(self):
        print "Controller Initialised"

    def run(self,SP,sysID,yt):
        ut = (SP-(sysID[0]*yt))/sysID[1]
        print ut
        
        #Write Output
        if ut > 1000:
            ut = 1000
             
        elif ut < 0:
            ut = 0
             
        else:
            ut = ut      
        
        return ut