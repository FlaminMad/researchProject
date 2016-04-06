#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   02/11/2015
Rev:    1
Lang:   Python 2.7
Deps:   None
Desc:   Contains Recursive least squares solver algorithms
"""

import numpy as np
from numpy import linalg as ma

class RLS:
    
    def __init__(self):
        #Initialise independant variables here
        self.I = np.eye(2)
        self.ff = 0.95

    def setup(self,xT,y): 
        #Initialise dependant variables here
        x = np.matrix.transpose(xT)
        self.P = ma.matrix_power(np.dot(xT[:,:2],x[:2,:]),-1)
        self.sysID = np.dot(np.dot(self.P,xT[:,:2]),y[:2,0])
    
    def solve(self,x,y):
        #RLS Solving Algorithm where sysID contains identified parameters
        xT = np.matrix.transpose(x)
        
        D = self.ff + np.dot(np.dot(xT,self.P),x)
        
        K = np.dot(np.dot(self.P,x),(np.power(D,-1)))
        
        self.P = 1/self.ff * np.dot((self.I-np.dot(K,xT)),self.P)
        
        self.sysID = self.sysID + K*(y - np.dot(xT,self.sysID))
        