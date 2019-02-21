import smbus
import time
import m as m
from gps3 import gps3
import numpy as np


sb = smbus.SMBus(1)   #1 start byte

sb.write_byte_data(0x1E, 0x20, 0b11111100)      #0x1E is the address of magnetometer
sb.write_byte_data(0x1E, 0x21, 0b00000000)      #0x20 is the register
sb.write_byte_data(0x1E, 0x22, 0b00000000)      #0b11111100 is the data to write on those registers
sb.write_byte_data(0x1E, 0x23, 0b00001100)

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def mapp(x, in_min, in_max, out_min, out_max):
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min

def ans():
    if (x_mag>0):
        print('1 x>0')
        pos = 4*m.atan2(y_mag,x_mag)/3
        if pos>0:
            print('12')
            return pos
#	elif(pos>200):
#	    print('23')
#	    return pos + 60
        else:
            print('34')
            mapped = mapp(pos + m.pi*2, 270 , 360, 315, 360)
            return (pos + m.pi*2)


    elif (x_mag==0 and y_mag>0):
        print('2 x=0 y>0')
        return m.pi/2

    elif (x_mag==0 and y_mag<0):
        print('3 x=0 y<0')
        return -m.pi/2

    #elif (x_mag<0 and y_mag>=0):
    elif (x_mag<0):
        print('4 x<0 y>=0')
        if ((m.atan2(y_mag,x_mag) + m.pi/2)>0):
            print('41')
            return (m.atan2(y_mag,x_mag) + m.pi/2)*6/7
        else:
            print('42')
            if (m.atan2(y_mag,x_mag)+ m.pi*5/2 - 40*m.pi/180)*m.pi/180>270:
                print('42 inside')
                return 270
            elif (m.atan2(y_mag,x_mag)+ m.pi*5/2 - 40*m.pi/180)<270:
                print('42 outside')
                return (m.atan2(y_mag,x_mag) + m.pi*5/2 - 40*m.pi/180)

        if (x_mag<0 and y_mag<0):
            print('5 x<0 y<0')
            return m.atan2(y_mag,x_mag) - m.pi
    #heading_new = trasnslate(heading, 0)

while True:
    time.sleep(0.1)
    x_l = sb.read_byte_data(0x1E, 0x28)
    x_h = sb.read_byte_data(0x1E, 0x29)
    x_mag = twos_comp(x_h << 8 | x_l, 16)
    y_l = sb.read_byte_data(0x1E, 0x2A)
    y_h = sb.read_byte_data(0x1E, 0x2B)
    y_mag = twos_comp(y_h << 8 | y_l, 16)
    z_l = sb.read_byte_data(0x1E, 0x2C)
    z_h = sb.read_byte_data(0x1E, 0x2D)
    z_mag = twos_comp(z_h << 8 | z_l, 16)
    print('x_value',x_mag)
    print('y_value',y_mag)
    #print('z_value',z_mag)

    heading = ans()*180/m.pi
    print(heading)


'''
def translate(heading, 0, 359, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
'''


#valueScaled = float(value - leftMin) / float(leftSpan)




lat2 = 13.347906667
lon2 = 74.792238333
lat1=0.000000
lon1=0.000000


gpsdsock = gps3.GPSDSocket()
data = gps3.DataStream()
gpsdsock.connect()
gpsdsock.watch()

def Bearing(lat1,lon1,lat2,lon2):

    y = m.cos(lat2) * m.sin(lon2-lon1)
    x = (m.cos(lat1) * m.sin(lat2)) - (m.sin(lat1) * m.cos(lat2) * m.cos(lon2-lon1))
#    print('not degree', m.atan2(y, x))
    degree = m.atan2(y, x) * 180 / m.pi

    if degree < 0:
        degree += 360
    print('degree',degree)

    # convert to radians
    dLat = (lat2 - lat1) * m.pi / 180.0
    dLon = (lon2 - lon1) * m.pi / 180.0

    # convert to radians
    lat1 = (lat1) * m.pi / 180.0
    lat2 = (lat2) * m.pi / 180.0

    # apply formulae
    a = (pow(m.sin(dLat / 2), 2) + pow(m.sin(dLon / 2), 2) * m.cos(lat1) * m.cos(lat2))
    rad = 6378.1*1000
    c = 2 * m.asin(m.sqrt(a))
#    print((rad * c),"M")


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
