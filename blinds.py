# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:16:59 2019

@author: codyl
"""
import azimuth
from gpiozero import AngularServo

class blinds:
    def __init__(self, faceDir=0, latitude=36, longitude=-79, closedUpAngle=90, closedDownAngle=-90, currentAngle=0):
        self.closedUpAngle = closedUpAngle
        self.closedDownAngle = closedDownAngle
        self.openAngle = (self.closedUpAngle + self.closedDownAngle) / 2
        self.currentAngle = currentAngle
        self.faceDir = faceDir
        self.latitude = latitude
        self.longitude = longitude
        self.s = None
        try:
            self.s = AngularServo(17, min_angle=closedDownAngle, max_angle=closedUpAngle)
        except Exception as e:
            print(e, "this computer has no GPIO pins")
        
    #%% class methods
    
    def saveBlindInfo(self):
        f = open('/home/pi/py/blindinfo.dat', 'w+')
        f.write(str([self.faceDir, self.latitude, self.longitude, self.closedUpAngle, self.closedDownAngle, self.currentAngle]))
        f.close()
        
    def setBlindFileInfo(self):
        f = open('/home/pi/py/blindinfo.dat', 'r')
        info = f.read()
        #turn list in string format to list in list format
        res = info.strip('][').split(', ')
        for k, l in enumerate(res):
            res[k] = float(l)
        #set angles
        self.closedUpAngle = res[3]
        self.closedDownAngle = res[4]
        self.openAngle = (self.closedUpAngle + self.closedDownAngle) / 2
        self.currentAngle = res[5]
        self.faceDir = res[0]
        self.latitude = res[1]
        self.longitude = res[2]
        
    #%% setter methods
        
    def setAngle(self, angle):
        self.currentAngle = angle
        try:
            self.s.angle = angle
        except Exception as e:
            print(e, "this computer has no GPIO pins")
    
    def calibrate(self):
        self.setAngle(0)
    
    def setSunOpen(self):
        rotateamount = azimuth.getAlt(self.latitude, self.longitude)
        
        if rotateamount > self.closedUpAngle: #don't over-rotate
            print('Angle > 90')
            rotateamount = self.closedUpAngle
        elif rotateamount < 0:
            print('Sun has set')
            rotateamount = self.closedDownAngle #don't rotate if sun is below horizon
        elif abs(self.faceDir - azimuth.getAz(self.latitude, self.longitude)) > 180: #don't rotate if sun isn't facing the window
            print('Sun not facing Window')
            rotateamount = self.closedUpAngle
        
        elif (abs(rotateamount - self.currentAngle)) > 5:
            print('rotating to  {} from {}'.format(rotateamount, self.currentAngle))
            self.setAngle(rotateamount)
        else:
            print('Rotation amount less than 5 degrees')
            print('Current angle is {}, rotation angle is {}'.format(self.currentAngle, rotateamount))
        
    def setClosedUp(self):
        self.setAngle(self.closedUpAngle)
        
    def setClosedDown(self):
        self.setAngle(self.closedDownAngle)
