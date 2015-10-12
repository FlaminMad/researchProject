#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   09/10/2015
Rev:    0.1
Lang:   Python 2.7
Deps:   scipy, collections
"""

from scipy import optimize as opt
from collections import deque as dq
import numpy


class leastSquares:
    
    #Initial guess of alpha and beta    
    x0 = numpy.array([1.0,1.0])
     
    def func(self,params,y,u,Y):
        #structure of function to be minimised
        return (Y - (params[0]*y + params[1]*u))


    def solve(self,y,u,Y):
        #run least squares algorithm - add try statement here
        ans = opt.leastsq(self.func,self.x0, args=(y,u,Y))
        #translate answers
        self.x0[0] = ans[0][0]
        self.x0[1] = ans[0][1]
        #for debugging - REMOVE LATER
        print self.x0



class dataStorage:
    
    #Amount of data points used to generate alpha and beta in least squares
    dataPoints = 20
    #Initialise list to be used as 'realtime data storage'  
    memU = dq([])
    memY = dq([])
    memY1 = dq([])
    #Initial flag to signal data removal
    startupFlag = 0    

    def memoryUpdate(self,In):
        if self.memU.__len__() == 0:
            #Value for Yt+1 is not yet know so to avoid issues, set equal to zero            
            self.memU.append(In[0])
            self.memY1.append(0)            
            self.memY.append(In[3])
            print "State 1"
            
        elif (self.memU.__len__() == 1 and self.startupFlag == 0):
            #Store new data         
            self.memU.append(In[0])
            self.memY1.append(self.memY[-1])            
            self.memY.append(In[3])
            #Remove the startup data
            self.memU.popleft()
            self.memY.popleft()
            self.memY1.popleft()
            #Ensure this procedure does not run again
            self.startupFlag = 1          
            
        elif self.memU.__len__() < self.dataPoints:
            #Filling lists up to number set by dataPoints
            self.memU.append(In[0])
            self.memY1.append(self.memY[-1])            
            self.memY.append(In[3])
            
        else:
            #store data            
            self.memU.append(In[0])
            self.memY1.append(self.memY[-1])            
            self.memY.append(In[3])
            #Keep data lists at length identified
            self.memU.popleft()
            self.memY.popleft()
            self.memY1.popleft()        