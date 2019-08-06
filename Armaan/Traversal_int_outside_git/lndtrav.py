import smbus
import time
import math
from gps3 import gps3
import numpy as np
import RPi.GPIO as GPIO 
import os
import serial
GPIO.setmode(GPIO.BCM)
trig1=9
echo1=11
trig2=8
echo2=25
trig3=19
echo3=26
trig4=20
echo4= 16
GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(trig3,GPIO.OUT)
GPIO.setup(trig4,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(echo2,GPIO.IN)
GPIO.setup(echo3,GPIO.IN)
GPIO.setup(echo4,GPIO.IN)
"""GPIO.setup(ldir,GPIO.OUT)
GPIO.setup(lspeed,GPIO.OUT)
GPIO.setup(rdir,GPIO.OUT)
GPIO.setup(rspeed,GPIO.OUT)
a=GPIO.PWM(lspeed,100)
c=GPIO.PWM(rspeed,100)
a.start(50)
c.start(50)
"""
ser=serial.Serial('/dev/serial0')
ser.baudrate=38400

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

l=360-180
x_manual=2.686
y_manual=0.255

lat2 =  13.3478
lon2 =  74.79223
lat1 = 0.0000000
lon1 = 0.0000000
bus = smbus.SMBus(1)
def left():
    """GPIO.output(ldir,0)	
    GPIO.output(rdir,1)"""
    ser.write(chr(4))
    return
def right():
    """GPIO.output(ldir,1)	
    GPIO.output(rdir,0)"""
    ser.write(chr(3))
    return
def front():
    """GPIO.output(ldir,1)	
    GPIO.output(rdir,1)
    a.ChangeDutyCycle(50)	
    c.ChangeDutyCycle(50)"""
    ser.write(chr(1))
    return
def back():
    """GPIO.output(ldir,0)	
    GPIO.output(rdir,0)	
    """
    ser.write(chr(2))
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
	x=x-x_manual
        y=y-y_manual
	

	h=math.atan2(y,x)*180/math.pi
	if h<0:
		h+=360
	h=(h+l)%360
	return h
		
bus.write_byte_data(0x1E, 0x20, 0b01111100)
bus.write_byte_data(0x1E, 0x21, 0b00000000)
bus.write_byte_data(0x1E, 0x22, 0b00000000)
bus.write_byte_data(0x1E, 0x23, 0b00001100)
#infinite loop
gate_no=input("enter number of gates ") 
latarr=[]
lonarr=[]
for coun in range(gate_no):
	latarr.append(float(input("Enter latitude ")))
	lonarr.append(float(input("Enter longitude ")))
cood=0
for new_data in gps_socket:
	adiff=0
	finalhead=0
	h=getheading()
	trigger(trig1)
	d1=pulsein(echo1)
	trigger(trig2)
	d2=pulsein(echo2)
	trigger(trig3)
	d3=pulsein(echo3)
	trigger(trig4)
	d4=pulsein(echo4)
	print d1,d2,d3,d4
	
	if d1<30 and d1<d2:
		#90 degree right
		print"right overide"
		while adiff<91:
				
			
			
			
			
					
			right()
			"""a.ChangeDutyCycle(50)	
    			c.ChangeDutyCycle(50)	
    			"""
			finalhead=getheading()
			adiff=abs(finalhead-h)
			if adiff>180:
				adiff=360-adiff
	elif d2<30:
		#90 degree left 
		print"left overide"
		while adiff<91:
			
			
					
			left()
			"""a.ChangeDutyCycle(50)	
    			c.ChangeDutyCycle(50)"""
			finalhead=getheading()
			adiff=abs(finalhead-h)
			
			if adiff>180:
				adiff=360-adiff
				
	elif d3<40 or d4<40:
		print "sides overide"
		front()
		
	else:		
		print"correct path"

	#path correction
		if new_data:
			data_stream.unpack(new_data)
			lat1=data_stream.TPV['lat']
			lon1=data_stream.TPV['lon']
	
	
	
			#lat2=b[i][0]
			#lon2=b[i][1]	
			if lat1=='n/a' or lon1=='n/a' :
				continue
	
			bear=getbearing(lat1,lon1,latarr[cood],lonarr[cood])	
			dist=getdistance(lat1,lon1,latarr[cood],lonarr[cood])
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
		
			if dist<=2:
				print "gate",cood+1,"reached"
				#execute ball detection
				os.system("python send_UDP.py")
				cood+=1
				
				if cood==gate_no:
					ser.write(chr(5))
					quit()
				#i+=1 
		 
		if turn=="front":
			front()
			"""a.ChangeDutyCycle(50)	
    			c.ChangeDutyCycle(50)"""
		elif turn=="right":
			right()
			""""
			a.ChangeDutyCycle(50)	
    			c.ChangeDutyCycle(50)"""
		elif turn=="left":
			"""
			a.ChangeDutyCycle(50)	
    			c.ChangeDutyCycle(50)"""
			left()			
        print dist,tfinal,turn 
