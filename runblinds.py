# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:08:49 2019

@author: codyl
"""
import blinds as bl
import datetime
from dateutil import tz

timezone = tz.gettz()
date = datetime.datetime.now(tz=timezone)
print(date.hour, date.minute)
    
def runBlinds():
    blind = bl.blinds()
    blind.setBlindFileInfo()
    
    date = datetime.datetime.now()
    if 4 < date.month < 10:
        blind.setClosedDown()
        print('Blinds set to Down')
        
    elif not 6 < date.hour < 20:
        blind.setClosedDown()
        print('Blinds set to Down')

    blind.setSunOpen()
    print('Sleeping for 30 min...')
    blind.saveBlindInfo()
    
runBlinds()