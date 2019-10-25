# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:08:49 2019

@author: codyl
"""
import azimuth as az
import blinds as bl
import datetime
import time

timezone = datetime.timezone(datetime.timedelta(seconds=time.timezone))
date = datetime.datetime.now(tz=timezone)
print(date.hour, date.minute)
    
def runBlinds():
    blind = bl.blinds()
    blind.setBlindFileInfo()
    blind.calibrate()
    
    date = datetime.datetime.now()
    if 4 < date.month < 10:
        blind.setClosedDown()
        print('Blinds set to Down')
        
    elif not 6 < date.hour < 20:
        blind.setClosedDown()
        print('Blinds set to Down')

    blind.setSunOpen()
    print('Blinds set to face the Sun at {:0.2} degrees'.format((az.getAlt(blind.latitude, blind.longitude))))
    print('Sleeping for 30 min...')
    
runBlinds()