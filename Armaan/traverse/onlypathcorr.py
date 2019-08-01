import smbus
import time
import math
from gps3 import gps3
import numpy as np
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
trig1=27
echo1=17
trig2=14
echo2=15
trig3=26
echo3=19
trig4=20
echo4= 21
ldir=9
lspeed=11
rdir=23
rspeed=24
GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(trig3,GPIO.OUT)
GPIO.setup(trig4,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(echo2,GPIO.IN)
GPIO.setup(echo3,GPIO.IN)
GPIO.setup(echo4,GPIO.IN)
GPIO.setup(ldir,GPIO.OUT)
GPIO.setup(lspeed,GPIO.OUT)
GPIO.setup(rdir,GPIO.OUT)
GPIO.setup(rspeed,GPIO.OUT)
a=GPIO.PWM(lspeed,100)
c=GPIO.PWM(rspeed,100)
a.start(50)
c.start(50)

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
dist=0
turn="front"
tfinal=0

min_x=0
max_x=0
min_y=0
max_y=0
min_z=0
max_z=0

l=360-179
x_manual=1.6575
y_manual=2.424

lat2 =  13.3478
lon2 =  74.79223
lat1 = 0.0000000
lon1 = 0.0000000
bus = smbus.SMBus(1)
def left():
    GPIO.output(ldir,0)	
    GPIO.output(rdir,1)
    return
def right():
    GPIO.output(ldir,1)	
    GPIO.output(rdir,0)
    return
def front():
    GPIO.output(ldir,1)	
    GPIO.output(rdir,1)
    return
def back():
    GPIO.output(ldir,0)	
    GPIO.output(rdir,0)	
    
    return 
def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val
def getdistance(lati,loni,latd,lond):
	latdiff=(latd-lati)*np.pi/180.0
	londiff=(lond-loni)*np.pi/180.0
	latif=lati*np.pi/180.0
	latdf=latd*np.pi/180.0
	a=(math.sin(latdiff/2)**2)+(math.sin(londiff/2)**2)*math.cos(latif)*math.cos(latdf)
	
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	d=6378.0*c*1000
	return d
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
def trigger(trig):
     GPIO.output(trig,GPIO.LOW)
     time.sleep(0.001)
     GPIO.output(trig,GPIO.HIGH)
     time.sleep(0.00001)
     GPIO.output(trig,GPIO.LOW)
     return 



def pulsein(echo):
# flag=0
 while(GPIO.input(echo)==0):
     #print("in zero")
     pass
 t1=time.time()
 while(GPIO.input(echo)==1):
     #print("in 1")
     t2=time.time()
     if ((t2-t1>0.0233)):
           break
  
     
 #t2=time.time()
 d=(t2-t1)*17150
 d=round(d,2)
 
 return d
def getheading():
	out_x_m_l = bus.read_byte_data(0x1E, 0x28)
	out_x_m_h = bus.read_byte_data(0x1E, 0x29)
	x = twos_complement((out_x_m_h << 8) | out_x_m_l, 16) / 1e3
	#print("X=", x, "gauss")



	out_y_m_l = bus.read_byte_data(0x1E, 0x2A)
	out_y_m_h = bus.read_byte_data(0x1E, 0x2B)
	y= twos_complement((out_y_m_h << 8) | out_y_m_l, 16) / 1e3
	#print("Y=", y, "gauss")


	out_z_m_l = bus.read_byte_data(0x1E, 0x2C)
	out_z_m_h = bus.read_byte_data(0x1E, 0x2D)
	z = twos_complement((out_z_m_h << 8) | out_z_m_l, 16) / 1e3
	#print("Z=",z, "gauss")
	x=x-1.6575
        y=y-2.424
	

	h=math.atan2(y,x)*180/math.pi
	if h<0:
		h+=360
	h=(h+360-179)%360
	return h
		
bus.write_byte_data(0x1E, 0x20, 0b01111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)
#infinite loop
try:
 for new_data in gps_socket:
 
	#path correction
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
			tdiff=bear-h
			if tdiff<0:
				tdiff+=360


			if tdiff<180 :#t2 is greater
				turn = "right"
				tfinal=tdiff
				if tfinal<16:
					turn="front"
					tfinal=0
			else:
				turn= "left"
				tfinal=360-tdiff
				if tfinal<16:
					turn="front"
					tfinal=0
		
			if dist<=5:
				print "gate",i,"reached"
				print "exiting"
				quit()
		
				i+=1 
		 
	if turn=="front":
		front()
	elif turn=="right":
		right()
	elif turn=="left":
		left()			
        print dist,tfinal,turn 
except KeyboardInterrupt:
	GPIO.cleanup()    	
