# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:16:59 2019

@author: codyl
"""
import azimuth
from gpiozero import AngularServo
from time import sleep

# creates a new instance of blinds with a latitude and longitude set 
# to North Carolina's, angle values restricted to +-90 degrees, and 
# an initial angle of 0 degrees. 
class blinds: 
    def __init__(self, faceDir=0, latitude=36, longitude=-79, closedUpAngle=90, closedDownAngle=-90, currentAngle=0): 
        self.closedUpAngle = closedUpAngle
        self.closedDownAngle = closedDownAngle
        self.openAngle = (self.closedUpAngle + self.closedDownAngle) / 2 # openAngle is the average of closedUpAngle and closedDownAngle - in this case, 0 degrees
        self.currentAngle = currentAngle
        self.faceDir = faceDir 
        self.latitude = latitude
        self.longitude = longitude
        self.s = None 
        try:
            self.s = AngularServo(17, min_angle=closedDownAngle, max_angle=closedUpAngle) # creates a new stepper motor object. Restricts it to a 180 degree range
        except Exception as e:
            print(e, "this computer has no GPIO pins") # This pretty much just checks if you're using a raspberry pi. If you get an exception, you aren't.
        
    #%% class methods
    
# saves current blind info. This is a pretty good idea for when the raspberry pi gets turned off, if that occurs. 
    def saveBlindInfo(self):
        f = open('/home/pi/py/blindinfo.dat', 'w+') 
        f.write(str([self.faceDir, self.latitude, self.longitude, self.closedUpAngle, self.closedDownAngle, self.currentAngle])) 
        f.close()
# uploads blind info from earlier. I'd argue this is a setter method.
    def setBlindFileInfo(self):
        f = open('/home/pi/py/blindinfo.dat', 'r')
        info = f.read()
        #turn list in string format to list in list format
        res = info.strip('][').split(', ')
        for k, l in enumerate(res):
            res[k] = float(l)
        #set blind parameters 
        self.closedUpAngle = res[3]
        self.closedDownAngle = res[4]
        self.openAngle = (self.closedUpAngle + self.closedDownAngle) / 2
        self.currentAngle = res[5]
        self.s.angle = res[5]
        self.faceDir = res[0]
        self.latitude = res[1]
        self.longitude = res[2]
        
    #%% setter methods
        
# changes the value of current angle and rotates the stepper motor to angle
    def setAngle(self, angle):
        self.currentAngle = angle
        try:
            self.s.angle = angle # rotates the servo motor to angle. 
            time.sleep(5) # sleeps for 5 seconds
        except Exception as e:
            print(e, "this computer has no GPIO pins") 
    
    def calibrate(self):
        self.setAngle(0) # calibrate sets the angle to zero. For our calibrate function, we'll want to set the minimum angle, the maximum angle, and the open angle.
    # defines the amount the angle is supposed to change by setting it equal to the sun's azimuth, which is subject to change
    def setSunOpen(self):
        self.calibrate() 
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
        # closesUp the angle
    def setClosedUp(self):
        self.calibrate()
        self.setAngle(self.closedUpAngle)
        #closesDown the angle
    def setClosedDown(self):
        self.calibrate()
        self.setAngle(self.closedDownAngle)
