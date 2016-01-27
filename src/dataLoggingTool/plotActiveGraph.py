

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
import yaml
import matplotlib.pyplot as plt

# Example Usage:
# pag = plotActiveGraph()
# pag.dataUpdate(x,y1,y2,y3...)
# Ensure to add:
#    pag.plt.show(block=True)
# at the end of the main method to keep graph open on return


class plotActiveGraph:
    
    def __init__(self):
        self.config= self._importSettings()
        self.xdata = np.array([[]])
        self.startFlag = 0
        self.fig = plt.subplots()
        
        if self.config["no_of_plots"] == 1:
            self.ax1 = plt.subplot(1,1,1)
        elif self.config["no_of_plots"] == 2:
            self.ax1 = plt.subplot(2,1,1)
            self.ax2 = plt.subplot(2,1,2)
            self.ax2.set_xlabel('Time (s)')
        else:
            raise SystemExit("Invalid number of plots")
        
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylim(self.config['y_axis_min'],self.config['y_axis_max'])
        
        plt.ion()
        plt.show()
        #"Ensure end fuction is the last method called to keep plot window open on program return"


    def dataUpdate(self,x,*plotData):
        # Update x axis data array  
        self.xdata = np.append(self.xdata,x)
        
        if self.startFlag == 0:
            # Initialise array for number of pens to plot
            self.ydata = np.array([[]]).reshape(len(plotData),0)
            self.ydata = np.append(self.ydata,np.transpose(np.matrix(plotData)),1)
        else:
            # Update y axis data matrix
            self.ydata = np.append(self.ydata,np.transpose(np.matrix(plotData)),1)
                        
        #Correct array size for data length
        if len(self.xdata) > 20: #Set this num up in json to allow variable length graphs
            self.xdata = np.delete(self.xdata,0)
            self.ydata = np.delete(self.ydata,0,1)
        
        # Update graph
        self._plot()
        
        
    def _plot(self):
        #Adds data ready to write
        try:
            if self.config["no_of_plots"] == 1:
                for i in range (0, (len(self.ydata[:,0]))):
                    self.ax1.plot(self.xdata,np.transpose(self.ydata[i,:]),self.config["pen_" + str(i+1) + "_colour"],label=self.config["pen_" + str(i+1) + "_name"])
            else:            
                for i in range (0, 3):
                    self.ax1.plot(self.xdata,np.transpose(self.ydata[i,:]),self.config["pen_" + str(i+1) + "_colour"],label=self.config["pen_" + str(i+1) + "_name"])
                for i in range (3, (len(self.ydata[:,0]))):
                    self.ax2.plot(self.xdata,np.transpose(self.ydata[i,:]),self.config["pen_" + str(i+1) + "_colour"],label=self.config["pen_" + str(i+1) + "_name"])
                    
        except IndexError:
            print ("Check ALL variables passed are setup in plotPenConf")
        
        # Sets up the legend
        if self.startFlag == 0:
            plt.legend()
            self.startFlag = 1        
        # Draws the graph to your screen
        plt.draw()
        # Workaround to avoid the freezing problem
        plt.pause(0.001)
    
    
    def _importSettings(self):
        #Reads plotPenConfiguration file to import colours and labels
        try:        
            with open("plotPenConfiguration.yaml", "r") as f:
                config = yaml.load(f)
        except IOError:
            print("Failed to read config file")
            raise SystemExit()   
        return config
        
    def end(self):
        plt.show(block=True)