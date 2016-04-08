# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 20:29:56 2016

@author: Alex Leech
"""

from setuptools import setup

setup(name='researchProject',
      version='0.1',
      description='Masters Research Project on Level Control',
      url='http://github.com/flaminmad/researchProject',
      author='Alexander Leech',
      author_email='alex.leech@talktalk.net',
      licence='MIT',
      packages=['researchProject'],
      install_requires=['numpy', 'matplotlib','pyserial']
      dependancy_links=['https://github.com/stephane/libmodbus'],
      zip_safe=False)