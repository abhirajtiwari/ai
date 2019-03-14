from gps3 import gps3
import math
import numpy as np
import smbus
import RPi.GPIO as GPIO
import time
import RTIMU 
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
def left():
    GPIO.output(ldir,1)
    GPIO.output(lspeed,1)	
    GPIO.output(rdir,0)
    GPIO.output(rspeed,1)
    return
def right():
    GPIO.output(ldir,0)
    GPIO.output(lspeed,1)	
    GPIO.output(rdir,1)
    GPIO.output(rspeed,1)
    return
def front():
    GPIO.output(ldir,1)
    GPIO.output(lspeed,1)	
    GPIO.output(rdir,1)
    GPIO.output(rspeed,1)
    return
def back():
    GPIO.output(ldir,0)
    GPIO.output(lspeed,1)	
    GPIO.output(rdir,0)
    GPIO.output(rspeed,1)
    return 
   	
add=0x1e

i=0
s=RTIMU.Settings('RTIMULib')
imu=RTIMU.RTIMU(s)
imu.IMUInit()
imu.setSlerpPower(0.02)
imu.setCompassEnable(True)

pause=imu.IMUGetPollInterval()
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
	print "back"
        
    if(dl<dr):
        right()
	print "right"
        #time.sleep(0.01)
    else:
        left()
	print "left"
        #time.sleep(0.01)
    return
def getdistance(lati,loni,latd,lond):
	latdiff=(latd-lati)*np.pi/180.0
	londiff=(lond-loni)*np.pi/180.0
	latif=lati*np.pi/180.0
	latdf=latd*np.pi/180.0
	a=(math.sin(latprdiff/2)**2)+(math.sin(londiff/2)**2)*math.cos(latif)*math.cos(latdf)
	
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	d=6378.0*c*1000
	return d
def map(x,in_min,in_max,out_min,out_max):
	return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min



def getHeading():
    if imu.IMURead():
        data = imu.getCompass()
        heading = math.atan2(data[1], data[0]) * 180./np.pi
        if heading < 0:
            heading += 360
        return heading
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
try:
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
		continue
    			
    elif d1<20  :
	#go right
	direc="right"
	
	p=1 
    elif d2<20 :
	#go left
	direc="left"
	
    elif d3<20 or d4<20:
	#go straight
	direc="front"
	
     
    else:  	 
    	#mag	
    	if imu.IMURead():
		data=imu.getCompass()
		h=math.atan2(data[1],data[0])*180/np.pi
		if h<0:
			h+=360
		h=360-h
		time.sleep(pause/1000) 
            
   
    		
    
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
			direc=turn = "right"
			tfinal=tdiff
			if tfinal<16:
				direc=turn="front"
				tfinal=0	
		else:
			direc=turn= "left"
			tfinal=360-tdiff
			if tfinal<16:
				direc=turn="front"
				tfinal=0
        
		if dist<=5:
			print "gate",i,"reached"
			print "exiting"
			quit()
		
			i+=1 
		 
	
    #print dist,tfinal,turn
    if direc=="right":
		right()
    elif direc=="left":

		left()
    elif direc=="front":
		front()
	  
    print direc
except KeyboardInterrupt:
 gpio.cleanup()
