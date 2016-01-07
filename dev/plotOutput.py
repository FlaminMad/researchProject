#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   07/01/2016
Rev:    1
Lang:   Python 2.7
Deps:   numpy, matplotlib, warnings
"""

import numpy as np
import warnings
import matplotlib.pyplot as plt

# Example Usage:
# pag = plotActiveGraph()
# pag.dataUpdate(x,y1,y2,y3...)
# Ensure to add:
#    pag.plt.show(block=True)
# at the end of the main method to keep graph open on return


class plotActiveGraph:
    
    def __init__(self):
        self.xdata = np.array([[]])
        self.startFlag = 0
        self.fig = plt.subplots()
        plt.subplot(1,1,1)
        plt.ylim(0,1000)
        plt.ion()
        plt.xlabel("Time (s)")
        plt.show()
        warnings.warn("Ensure plt.show(block=True) is at the end of the main file to keep plot window open on program return")

    def dataUpdate(self,x,*plotData):       
        # Update x axis data array  
        self.xdata = np.append(self.xdata,x)
        
        if self.startFlag == 0:
            # Initialise array for number of pens to plot
            self.ydata = np.array([[]]).reshape(len(plotData),0)
            self.ydata = np.append(self.ydata,np.transpose(np.matrix(plotData)),1)
            self.startFlag = 1
        else:
            # Update y axis data matrix
            self.ydata = np.append(self.ydata,np.transpose(np.matrix(plotData)),1)
                        
        #Correct array size for data length
        if len(self.xdata) > 20: #Set this num up in json to allow variable length graphs
            self.xdata = np.delete(self.xdata,0)
            self.ydata = np.delete(self.ydata,0,1)
        
        # Update graph
        self.plot()
        
    def plot(self):
        #Adds data ready to write
        try:
            for i in range (0, (len(self.ydata[:,0]))):
                plt.plot(self.xdata,np.transpose(self.ydata[i,:]),'g-',label='i')
        except IndexError:
            print ("Check ALL variables passed are setup in plotPenConf")
        
        # Draws the graph to your screen
        plt.draw()
        # Workaround to avoid the freezing problem
        plt.pause(0.001)