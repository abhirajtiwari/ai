import smbus
import time
import math as m
from gps3 import gps3
import numpy as np

add=0x1e

lat2 = 13.347906667
lon2 = 74.792238333
#lat1=0.000000
#lon1=0.000000
#distance = 0.000000
degree = 0.000000

gpsdsock = gps3.GPSDSocket()
data = gps3.DataStream()
gpsdsock.connect()
gpsdsock.watch()


i2c=smbus.SMBus(1)
i2c.write_byte_data(add,0x20,0b01011100)#high performance
i2c.write_byte_data(add,0x21,0b00000000)#4 gauss range
i2c.write_byte_data(add,0x22,0b00000000)
i2c.write_byte_data(add,0x23,0b00001000)



def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


def Bearing(lat1,lon1,lat2,lon2):


    # convert to radians
    dLat = (lat2 - lat1) * m.pi / 180.0
    dLon = (lon2 - lon1) * m.pi / 180.0

    # convert to radians
    lat1 = (lat1) * m.pi / 180.0
    lat2 = (lat2) * m.pi / 180.0

    y = m.cos(lat2) * m.sin(dLon)
    x = (m.cos(lat1) * m.sin(lat2)) - (m.sin(lat1) * m.cos(lat2) * m.cos(dLon))
#    print('not degree', m.atan2(y, x))
    degree = m.atan2(y, x) * 180 / m.pi

    if degree < 0:
        degree += 360
    print('degree',degree)

    # apply formulae
    a = (pow(m.sin(dLat / 2), 2) + pow(m.sin(dLon / 2), 2) * m.cos(lat1) * m.cos(lat2))
    rad = 6378.1*1000
    c = 2 * m.asin(m.sqrt(a))
    #print((rad * c),"M")
    #print('rad',rad)
    #print('c',c)
    distance = rad * c
    return distance

for new_data in gpsdsock:
    #time.sleep(1)

    msbx=i2c.read_byte_data(add,0x29)
    lsbx=i2c.read_byte_data(add,0x28)
    x=(msbx<<8|lsbx)
    x=twos_comp(x,16)*0.00014
    msby=i2c.read_byte_data(add,0x2b)
    lsby=i2c.read_byte_data(add,0x2a)
    y=(msby<<8|lsby)
    y=twos_comp(y,16)*0.00014
    msbz=i2c.read_byte_data(add,0x2d)
    lsbz=i2c.read_byte_data(add,0x2c)
    z=(msbz<<8|lsbz)
    x=x-0.06
    y=y-0.35
    heading=m.atan2(y,x)*180/np.pi
    heading = heading - 73.00
    if heading<0:
        heading += 360



    if new_data:
        data.unpack(new_data)
        lat1 = data.TPV['lat']
        lon1 = data.TPV['lon']
        print('inside if')

    if (lat1 == 'n/a'):
        continue
    if (lon1 == 'n/a'):
        continue



    dist = Bearing(lat1, lon1, lat2, lon2)
    print('heading',heading)

###########degree is angle of the given gps coordinate from the north
###########heading is the orientation of the imu from north
    turn = heading - degree
    '''
    if abs(degree - heading)>20 and abs(heading - degree)>180:
        print('clockwise turn',heading - degree)
        print('distance', dist)
    elif abs(degree - heading)>20 and abs(heading - degree)<180:
        print('anticlockwise turn',heading - degree)
        print('distance', dist)
    else:
        print('straight')
        #print(360 - abs(degree - heading))
        print('distance', dist)
    '''

    print('distance', dist)
    if(turn<8 and turn>-8):
        print('straight')
        print(turn)
    elif((turn)<0 and (turn)<=-180):
        print('anti-clock1', 360 + turn)
        print(turn)
    elif ((turn)<0 and (turn)>-180):
        print('clock1', -turn)
        print(turn)
    elif ((turn)>0 and (turn)>=180):
        print('clock2', 360 - turn)
        print(turn)
    elif ((turn)>0 and (turn)<180):
        print('anti-clock2', turn)
        print(turn)

    if dist<4:
        print('destination reached')
        quit()

###############if heading is not 0 when facing north

#(now not) assuming when mag facing north is 0.00000
####################################################
####################################################


###########GPS########################



#######################GPS angle and distance





####################################
