# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:49:03 2016

@author: alex
"""

from subscript import subscript
import thread
import time

def main():
    x = 0
    key = subscript()
    thread.start_new_thread(key.keys())
    
    while True:
        print(x)
        x += 1
        time.sleep(1)
    
if __name__ == '__main__':main()