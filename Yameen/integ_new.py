import smbus
import time
import math as m
from gps3 import gps3
import numpy as np
import RPi.GPIO as GPIO

add=0x1e

lat2 = 13.3475583
lon2 = 74.792135
lat1=0.000000
lon1=0.000000
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

GPIO.setmode(GPIO.BCM)

echo_left = 17
trigger_left = 27
echo_right = 15
trigger_right = 14
echo_side_l = 19
trigger_side_l = 26
echo_side_r = 21
trigger_side_r = 20


GPIO.setup(trigger_left, GPIO.OUT)
GPIO.setup(echo_left, GPIO.IN)

GPIO.setup(trigger_right, GPIO.OUT)
GPIO.setup(echo_right, GPIO.IN)

GPIO.setup(trigger_side_l, GPIO.OUT)
GPIO.setup(echo_side_l, GPIO.IN)

GPIO.setup(trigger_side_r, GPIO.OUT)
GPIO.setup(echo_side_r, GPIO.IN)

def Ultrasonic(pin,pin2):
	GPIO.output(pin2,False)
	time.sleep(0.1)

	GPIO.output(pin2,True)
	time.sleep(0.00001)
	GPIO.output(pin2,False)

	while GPIO.input(pin)==0:
		pass
	pulse_begins = time.time()
	
	while GPIO.input(pin)==1:
		pulse_stops = time.time()
		if (pulse_stops-pulse_begins>0.004):
			pulse_duration = pulse_stops-pulse_begins
			distance = pulse_duration*34000/2
			return distance,'not alert'
			break
	
	pulse_duration = pulse_stops-pulse_begins
	distance = pulse_duration*34000/2
	return distance,'alert'


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
    return distance, degree

for new_data in gpsdsock:
    time.sleep(0.1)

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
    heading = heading - 293.00
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

    dist, deg = Bearing(lat1, lon1, lat2, lon2)
    print('heading',heading)

###########degree is angle of the given gps coordinate from the north
###########heading is the orientation of the imu from north
    turn = heading - deg
    
    dist_lf,alert_lf = Ultrasonic(echo_left,trigger_left)
    dist_rf,alert_rf = Ultrasonic(echo_right,trigger_right)
    dist_sl, alert_l = Ultrasonic(echo_side_l,trigger_side_l)
    dist_sr, alert_r = Ultrasonic(echo_side_r,trigger_side_r)
    
    if (alert_lf == 'alert' and alert_rf == 'not alert'):
        print('Turn Right')
        continue
    elif (alert_rf == 'alert' and alert_lf == 'not alert'):
        print('Turn Left')
        continue
    else:
        print('back')
    
    if (alert_r == 'alert' and alert_l == 'not alert'):
        if((turn)<0 and (turn)<=-180):
            print('anti-clock1', 360 + turn)
        elif((turn)>0 and (turn)<180):
            print('anti-clock2', turn)
        else:
            print('go straight')
    elif (alert_l == 'alert' and alert_r == 'not alert'):
        if((turn)<0 and (turn)>-180):
            print('clock1', -turn)
        elif((turn)>0 and (turn)>=180):
            print('clock2', 360 - turn)
        else:
            print('go straight')    
    
    print('distance', dist)


    if dist<7:
        print('destination reached')
        quit()

###############if heading is not 0 when facing north

#(now not) assuming when mag facing north is 0.00000
####################################################
####################################################


###########GPS########################



#######################GPS angle and distance





####################################
