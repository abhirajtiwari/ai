from gps3 import gps3
import math
import numpy as np
import smbus
import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
trig1=27
echo1=17
trig2=14
echo2=15
trig3=26
echo3=19
trig4=20
echo4= 21

add=0x1e
i2c=smbus.SMBus(1)
i2c.write_byte_data(add,0x20,0b01011100)#high performance
i2c.write_byte_data(add,0x21,0b00000000)#4 gauss range
i2c.write_byte_data(add,0x22,0b00000000)
i2c.write_byte_data(add,0x23,0b00001000)
i=0
turn="straight"        
b=[[13.347801667
,74.792215],[1,2]]
#print"enter number gates"
n=2
"""for i in range(2):
	lat=raw_input()
	lon=raw_input()
	a=[lat,lon]
	b.append(a)
"""
lat2 =  13.3478
lon2 =  74.79223
lat1 = 0.0000000
lon1 = 0.0000000
tfinal=0.0
dist=0.0
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()



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

def brutestop(dl,dr):
    while(dl<5 or dr<5):
       # print("entered loop")
        #time.sleep(0.01)
        back()
        trigger(trig1)
        dl=pulsein(echo1)
        trigger(trig2)
        dr=pulsein(echo2)
        
    if(dl<dr):
        right()
        #time.sleep(0.01)
    else:
        left()
        #time.sleep(0.01)
def getdistance(lati,loni,latd,lond):
	latdiff=(latd-lati)*np.pi/180.0
	londiff=(lond-loni)*np.pi/180.0
	latif=lati*np.pi/180.0
	latdf=latd*np.pi/180.0
	a=(math.sin(latdiff/2)**2)+(math.sin(londiff/2)**2)*math.cos(latif)*math.cos(latdf)
	
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	d=6378.0*c*1000
	return d
def map(x,in_min,in_max,out_min,out_max):
	return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min
def dos(head):
	headup=0
	if(head>=0 and head<40):
	    	headup=map(head,0,40,0,90)
	elif(head>=40 and head<96):
		headup=map(head,40,96,90,180)
	elif(head>=96 and head<=140):
		headup=map(head,96,140,180,270)
	elif(head>=140 and head<360):
		headup=map(head,140,360,270,360)
	return headup
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
direc="forward"
for new_data in gps_socket:
    #ultrasonic 
    p=0	
    trigger(trig1)
    d1=pulsein(echo1)
    trigger(trig2)
    d2=pulsein(echo2)
    trigger(trig3)
    d3=pulsein(echo3)
    trigger(trig4)
    d4=pulsein(echo4)
    if (d1<5 or d2<5):
    		brutestop(d1,d2)	
    elif d1<20 :
	#go right
	direc="right"
	p=1 
    elif d2<20 :
	#go left
	direc="left"
	
    elif d3<20 or d4<20:
	#go straight
	direc="forward"
	
     
    else:  	 
    	#mag	
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
   
            
   
    	h=math.atan2(y,x)*180/np.pi
	
    	if h<0:
		h+=360
    	h=dos(h)		
    
    	#lat2=b[i][0]
    	#lon2=b[i][1]		
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
			direc=turn = "Clockwise"
			tfinal=tdiff
			if tfinal<16:
				direc=turn="straight"
				tfinal=0	
		else:
			direc=turn= "anticlockwise"
			tfinal=360-tdiff
			if tfinal<16:
				direc=turn="straight"
				tfinal=0
        
		if dist<=5:
			print "gate",i,"reached"
			print "exiting"
			quit()
		
			i+=1 
		 
	
    #print dist,tfinal,turn 
    print direc
