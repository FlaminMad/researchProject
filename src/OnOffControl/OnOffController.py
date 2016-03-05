#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   05/03/2015
Rev:    1
Lang:   Python 2.7
Deps:   yaml
Desc:   Contains On/Off controller class for import
"""

import yaml

class OnOffController:
     
     def __init__(self):
         self.params = self._importSettings()
         return
     
     def run(self,plantData):
         error = plantData.getRegister(2)-plantData.getRegister(0)
         if error < (self.params["tolerance"]*-1):
             self.u = self.params["vlvLowLimit"]
         elif error > self.params["tolerance"]:
             self.u = self.params["vlvHighLimit"]
         else:
             pass
         return self.u
     
     def _importSettings(self):
        #Reads plotPenConfiguration file to import colours and labels
        try:
            with open("OnOffParams.yaml", "r") as f:
                config = yaml.load(f)
        except IOError:
            print("Failed to read On/Off config file")
            raise SystemExit()
        return config