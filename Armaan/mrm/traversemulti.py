from gps3 import gps3
import math
import numpy as np
import smbus

add=0x1e
i2c=smbus.SMBus(1)
i2c.write_byte_data(add,0x20,0b01011100)#high performance
i2c.write_byte_data(add,0x21,0b00000000)#4 gauss range
i2c.write_byte_data(add,0x22,0b00000000)
i2c.write_byte_data(add,0x23,0b00001000)
i=0
turn="clockwise"        
b=[]
#print"enter number gates"
n=2
"""for i in range(2):
	lat=raw_input()
	lon=raw_input()
	a=[lat,lon]
	b.append(a)
"""
lat2 =  13.347801667
lon2 =  74.792215
lat1 = 0.0000000
lon1 = 0.0000000
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def getbearing(lati,loni,latd,lond):
	lati=lati*np.pi/180.0
	latd=latd*np.pi/180.0
	
	londiff=(lond-loni)*np.pi/180.0	
	y=math.sin(londiff)*math.cos(latd)
	x=math.cos(lati)*math.sin(latd)-math.sin(lati)*math.cos(latd)*math.cos(londiff)
	bear=math.atan2(y,x)*180.0/np.pi
	if bear<0:
		bear+=360
	return bear	


def getdistance(lati,loni,latd,lond):
	latdiff=(latd-lati)*np.pi/180.0
	londiff=(lond-loni)*np.pi/180.0
	latif=lati*np.pi/180.0
	latdf=latd*np.pi/180.0
	a=(math.sin(latdiff/2)**2)+(math.sin(londiff/2)**2)*math.cos(latif)*math.cos(latdf)
	
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	d=6378.0*c*1000
	return d

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()


tfinal=0.0
dist=0.0
for new_data in gps_socket:
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
    h=math.atan2(y,x)*180/np.pi
	
    if h<0:
		h+=360	
    h=(h+8.0)%360
    if new_data:
        data_stream.unpack(new_data)
        lat1=data_stream.TPV['lat']
	lon1=data_stream.TPV['lon']
	
	
	
	#lat2=b[i][0]
	#lon2=b[i][1]	
	if lat1=='n/a' or lon1=='n/a' :
		continue
	
	bear=getbearing(lat1,lon1,lat2,lon2)	
	dist=getdistance(lat1,lon1,lat2,lon2)
	t1=abs(h-bear)
	t2=360-t1

	if t2 > t1 :
		turn = "antiClockwise"
		tfinal=t1
	else:
		turn= "clockwise"
		tfinal=t2
	if tfinal<16:
		turn="straight"
		tfinal=0
        
	if dist<=5:
		print "gate",i,"reached"
		print "exiting"
		quit()
		#i+=1 
 	
	
    print dist,tfinal,turn 
    	
