from gps3 import gps3
import time

gpsdsock = gps3.GPSDSocket()
data = gps3.DataStream()
gpsdsock.connect()
gpsdsock.watch()

for newdata in gpsdsock:
    if newdata:
        data.unpack(newdata)
        print data.TPV['lat'], data.TPV['lon']

