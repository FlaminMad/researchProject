#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   12/11/2015
Rev:    1
Lang:   Python 2.7
Deps:   Pybrain
Desc:   AI network class
"""


import pybrain as AI


def FeedForward():
    # Establish Network
    n = AI.FeedForwardNetwork()

    # Define Layers    
    inLayer = AI.LinearLayer(2, name='in')
    hiddenLayer = AI.SigmoidLayer(3, name='hidden')
    outLayer= AI.LinearLayer(1, name='out')

    # Define Layer inputs/outputs    
    n.addInputModule(inLayer)    
    n.addModule(hiddenLayer)
    n.addOutputModule(outLayer)
    
    # Define Connections
    in_to_hidden = AI.FullConnection(inLayer, hiddenLayer)
    hidden_to_out = AI.FullConnection(hiddenLayer, outLayer)
    
    # Add to Network
    n.addConnection(in_to_hidden)
    n.addConnection(hidden_to_out)
    
    #Internal Initialisation        
    n.sortModules()
    
def main():
    print "Main"    
    
if __name__ == '__main__':main()