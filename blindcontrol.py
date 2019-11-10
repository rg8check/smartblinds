# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:32:58 2019

@author: codyl
"""

import blinds as b

bl = b.blinds()
bl.calibrate()

while True:
    newAngle = input('New Angle: ')
    try:
        bl.setAngle(int(newAngle))
    except Exception as e:
        print('An exception has occurred: {}'.format(e))
        break