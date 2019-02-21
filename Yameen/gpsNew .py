from gps3 import gps3
import time
import math
import numpy as np

lat2 = 13.347626666
lon2 = 74.792168333
#lat1=0.000000
#lon1=0.000000


gpsdsock = gps3.GPSDSocket()
data = gps3.DataStream()
gpsdsock.connect()
gpsdsock.watch()

def Bearing(lat1,lon1,lat2,lon2):

    x= math.cos(lat2) * math.sin(lon2-lon1)
    y= (math.cos(lat1) * math.sin(lat2)) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1))
    print('not degree', math.atan2(y, x))
    degree = math.atan2(y, x) * 180 / math.pi
    if degree>0:
        print('degree', degree)
    else:
        print('degree', degree + 360)
    # convert to radians
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6378.1*1000
    c = 2 * math.asin(math.sqrt(a))
    print((rad * c),"M")


for newdata in gpsdsock:
    if newdata:
        data.unpack(newdata)
        lat1 = data.TPV['lat']
        lon1 = data.TPV['lon']
        if (data.TPV['lat'] == 'n/a'):
            continue
        if (data.TPV['lon'] == 'n/a'):
            continue


        Bearing(lat1, lon1, lat2, lon2)
        print(lat1,lon1)










#13.347841667    74.792141667
