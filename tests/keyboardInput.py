# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:08:02 2015

@author: Toshiba
"""

import msvcrt

num = 0
done = False
while not done:
    print num
    num += 1

    if msvcrt.kbhit():
        print "you pressed",msvcrt.getch(),"so now i will quit"
        done = True