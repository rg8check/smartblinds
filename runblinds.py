# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:08:49 2019

@author: codyl
"""
import azimuth as az
import blinds as bl
import time as t
import datetime

lat = 0
long = 0
date = datetime.datetime.now()
print(date.minute, date.hour)

    
    
def runBlinds():
    lat = az.getlat()
    long = az.getlong()
    blind = bl.blinds(0, lat, long)
    input('Set your blinds to be flat. Press Enter when complete...')
    blind.calibrate()
    
    date = datetime.datetime.now()
    if 4 < date.month < 10:
        blind.setClosedDown()
        print('Blinds set to Down')
        print('Sleeping for a week...')
        
    elif not 6 < date.hour < 20:
        blind.setClosedDown()
        print('Blinds set to Down')
        print('Sleeping for an hour...')

    blind.setSunOpen()
    print('Blinds set to face the Sun at {:0.2} degrees'.format((az.getAlt(lat, long))))
    print('Sleeping for 30 min...')
    t.sleep(1800)