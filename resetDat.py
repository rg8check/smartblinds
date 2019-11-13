# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:30:34 2019

@author: codyl
"""

#(self, faceDir=0, latitude=36, longitude=-79, closedUpAngle=90, closedDownAngle=-90, currentAngle=0):
f = open('/home/pi/py/blindinfo.dat', 'w+')
f.write('[0, 36, -79, 90, -90, 0]')
f.close()