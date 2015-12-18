# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:06:16 2015

@author: Toshiba
"""
import time
import numpy as np
import matplotlib.pyplot as plt

class plotActiveGraph:
    
    def __init__(self):
        self.xdata = np.array([])
        self.ydata = np.array([])
        self.fig = plt.subplots()
        plt.subplot(1,1,1)
        plt.ylim(0,1000)
        plt.xlim(-20,20)
        plt.ion()
        plt.xlabel("Time (s)")
        plt.show()

    def dataUpdate(self,x,y):
        self.xdata = np.append(self.xdata,x)
        self.ydata = np.append(self.ydata,y)
        self.plot()
        
    def plot(self):
        plt.plot(self.xdata,self.ydata,'g-') # Adds data to your graph
        plt.draw() # Draws the graph to your screen
        
        
def func(x):
    y = (np.square(x)+(2*x)+12)
    return y

def main():
    pA = plotActiveGraph()
    
    for x in range(-20, 20):
        pA.dataUpdate(x,func(x))
        
    plt.show(block=True)
    
if __name__ == '__main__': main()