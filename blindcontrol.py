# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:32:58 2019

@author: codyl
"""
# this allows for manual control to test the angle rotating part of the code. Otherwise, the blinds turn every 30 minutes
import blinds as b # blinds.py is a module written by codyl

bl = b.blinds() #creates a new blind object
bl.calibrate() # sets the initial angle to zero.

while True:
    newAngle = input('New Angle: ') # inputs come from the blindinfo.dat file
    try:
        bl.setAngle(int(newAngle)) # rotates the stepper motor to that angle
    except Exception as e:
        print('An exception has occurred: {}'.format(e))
        break