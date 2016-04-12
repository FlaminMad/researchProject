#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   18/01/2016
@rev:    1
@lang:   Python 2.7
@deps:   Numpy, YAML
@desc:   Simulated system for usage in offline tests
         Make sure that the object is initiliased as 'r' so as to avoid code
         changes elsewhere
"""

import time
from testModel import testModel   #Import Graph Plotting Class
import sys; sys.path.insert(0, '../src/dataLoggingTool')
from plotActiveGraph import plotActiveGraph   #Import Graph Plotting Class
from osTools import osTools


def main():
    mdl = testModel("./")
    graph = plotActiveGraph()
    ext = osTools()
    startTime = time.time()
    Interval = 0.5
    
    while(True):
        mdl.readModel()
        graph.dataUpdate((time.time() - startTime),\
                         mdl.getRegister(0),\
                         mdl.getRegister(2),\
                         mdl.getRegister(3))
        if ext.kbdExit():
            break
        time.sleep(Interval)   #Loop Interval

if __name__ == '__main__':main() 