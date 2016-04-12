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
import sys, csv
import pybrain as AI
import pybrain.datasets as datasets
from pybrain.supervised.trainers import BackpropTrainer

class neuralNetwork:
    
    def __init__(self):
        self.__FeedForward()    
        self.__dataSetImport()
        self.__trainNet()
        return
    
    def __FeedForward(self):
        # Establish Network
        self.net = AI.FeedForwardNetwork()
    
        # Define Layers    
        inLayer = AI.LinearLayer(2, name='in')
        hiddenLayer = AI.SigmoidLayer(3, name='hidden')
        outLayer= AI.LinearLayer(1, name='out')
    
        # Define Layer inputs/outputs    
        self.net.addInputModule(inLayer)    
        self.net.addModule(hiddenLayer)
        self.net.addOutputModule(outLayer)
        
        # Define Connections
        in_to_hidden = AI.FullConnection(inLayer, hiddenLayer)
        hidden_to_out = AI.FullConnection(hiddenLayer, outLayer)
        
        # Add to Network
        self.net.addConnection(in_to_hidden)
        self.net.addConnection(hidden_to_out)
        
        #Internal Initialisation        
        self.net.sortModules()    
        
    def __dataSetImport(self):
        self.ds = datasets.SupervisedDataSet(2,1)    
        with open('trainingData.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                self.ds.addSample((row[0],row[1]),(row[2]))
        return
    
    def __trainNet(self):
        trainer = BackpropTrainer(self.net,self.ds)
        print "Training, Please Wait..."
        trainer.trainUntilConvergence()
        print "Done"
        
    def activate(self,pv,sp):
        u = self.net.activate((pv,sp))
        if int(sys.argv[1]) == 1:
            lim = 100
        else:
            lim = 1000
        if u > lim:
            return lim
        elif u < 0:
            return 0
        else:
            return u