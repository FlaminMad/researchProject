# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:49:19 2016

@author: alex
"""

class subscript:
    def __init__(self):
        print("Opened")
    
    def keys(self):
        while True:
            i = raw_input("Press the C key, followed by enter to exit... ")
            if i == "C":
                print("Im Done!")
                exit() # Needs to SAFELY exit. Look into thread events.