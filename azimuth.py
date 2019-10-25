# -*- coding: utf-8 -*-
import pysolar as pys
import datetime

#date = datetime.datetime.now(tz=datetime.timezone(-datetime.timedelta(hours=5)))
#print(pys.solar.get_altitude(42.206, -71.382, date))


#date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
#print(pys.solar.get_altitude(42.206, -71.382, date))

#%% get latitude if isn't specified
def getlat():
    while True:
        latitude = input('Input your latitude as a number in the range [-90, 90]: ')
        try:
            latitude = float(latitude)
            if -90 <= latitude <= 90:
                break
        except Exception as e:
            print(e)
        print('Latitude needs to be in the range [-90, 90]')
    return latitude

#%% get longitude if isn't specified
def getlong():
    while True:
        longitude = input('Input your longitude as a number in the range [-180, 180]: ')
        try:
            longitude = float(longitude)
            if -180 <= longitude <= 180:
                break
        except Exception as e:
            print(e)
        print('Longitude needs to be in the range [-180, 180]')
    return longitude


#%% main methods to be ran
def getAlt(latitude=None, longitude=None):
    if latitude is None:
        latitude = getlat()
    if longitude is None:
        longitude = getlong()
    
    timezone = datetime.timezone(datetime.timedelta(seconds=18000))
    date = datetime.datetime.now(tz=timezone)
    return pys.solar.get_altitude(latitude, longitude, date)

def getAz(latitude=None, longitude=None):
    if latitude is None:
        latitude = getlat()
    if longitude is None:
        longitude = getlong()
    
    timezone = datetime.timezone(datetime.timedelta(seconds=18000))
    date = datetime.datetime.now(tz=timezone)
    return pys.solar.get_azimuth(latitude, longitude, date)
