#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   09/10/2015
Rev:    0.1
Lang:   Python 2.7
Deps:   scipy
"""

from scipy import optimize as opt
import numpy



class leastSquares:
    
    data = numpy.array([[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
                         [4.043734,5.574828,7.329693,6.861458,12.177830,
                          13.609880,13.808600,18.323320,18.575510,20.152940,23.976990]])
    
    x0 = numpy.array([1.0,1.0])
    
    def func(self,params):
        #structure of function to be minimised
        return (self.data[1,:] - (params[0]*self.data[0,:] + params[1]))

    def run(self):
        ans = opt.leastsq(self.func,self.x0, args=())
        print "a = " + str(ans[0][0])
        print "b = " + str(ans[0][1])

if __name__ == '__main__':
    ls = leastSquares()
    ls.run()
    print "Done"