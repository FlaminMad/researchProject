# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:06:16 2015

@author: Alex Leech
"""

import numpy as np
import matplotlib.pyplot as plt

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

    def dataUpdate(self,x,*plotData):       
        # Update x axis data array        
        self.xdata = np.append(self.xdata,x)
        
        if self.startFlag == 0:
            # Initialise array for no of pens to plot
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
            for i in range (0, (len(self.ydata[:,0])-1)):
                plt.plot(self.xdata,self.ydata[i,:],'g-',label='i')
        except IndexError:
            print ("Check ALL variables passed are setup in plotPenConf")
        
        # Draws the graph to your screen
        plt.draw()
        # Workaround to avoid the freezing problem
        plt.pause(0.001)

def main():
    pag = plotActiveGraph()
    pag.dataUpdate(1,2,3,4)
    pag.dataUpdate(2,3,4,5)

if __name__ == '__main__':main()        