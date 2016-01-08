#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   07/01/2016
Rev:    1
Lang:   Python 2.7
Deps:   numpy, matplotlib, warnings
"""

import yaml

class testYAML:
    
    def __init__(self):
        print('ready')

    def readFile(self):       
        print('loading')
        
        with open("conf.yaml", "r") as file_descriptor:
            data = yaml.load(file_descriptor)
        return data
    
    
if __name__ == "__main__":
    ty = testYAML()
    content = ty.readFile()
    print content