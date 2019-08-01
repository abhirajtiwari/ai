import pygame
import time
import RPi.GPIO as gpio
from pygame import locals
gpio.setmode(gpio.BOARD)
pygame.init()
pygame.joystick.init()
joy=pygame.joystick.Joystick(0)
joy.init()

lfp=35
#lbp
rfp=36
#rbp
lf=0
sr=0
rf=0
lb=0
rb=0
sl=0
l=37
r=38
gpio.setup(lfp,gpio.OUT)
#gpio.setup(lbp,gpio.OUT)
gpio.setup(l,gpio.OUT)
gpio.setup(rfp,gpio.OUT)
gpio.setup(r,gpio.OUT)
a=gpio.PWM(l,100)
b=gpio.PWM(r,100)
a.start(0)
b.start(0)
top=255
def map(x,in_min,in_max,out_min,out_max):
	return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min

def pwm(val,pin):
	count=0
        while count<=val:
		gpio.output(pin,1)	 
		count+=1
	#x=(val/255)*0.01
	
	#time.sleep(x)
	while count<=top:
		gpio.output(pin,0)
		count+=1

dirl="0"
dirR="0"

sr=0


def oct(x1,y1):
	
	y1=-1*y1
	if((x1>=0 and x1<=0) and (y1>=0 and y1<=0)):
  		return 0;
  	if((x1>=0 and x1<=1)and(y1>=0 and y1<=1)):
  		 if(y1<x1):
    			return 1
   		 else:
  			return 2
	if((x1<=0 and x1>=-1)and(y1>=0 and y1<=1)):
		 if(y1>-x1):
  			return 3
  		 else:
 			return 4

	if((x1<=0 and x1>=-1)and(y1<=0 and y1>=-1)):
		 if(y1>x1):
  			return 8
  		 else: 
  			return 7

	if((x1>=0 and x1<=1)and(y1<=0 and y1>=-1)):

  		if(y1<-x1):
  			return 6
  		else: 
  			return 5
def speed(octo,x,y):
	y=-1*y;
	xq1=map(x,0,1,0,255)
	yq1=map(y,0,1,0,255)
	xq2=map(x,0,-1,0,255)
	yq2=map(y,0,-1,0,255)
	
	global sl
	global sr
	global dirl
	global dirR
	global lf
	global rf
        if octo==0:
  			lf=0
			rf=0
			lb=0
			rb=0
			sl=0
			sr=0
			dirl="0"
			dirR="0"
			#print(sl,sr)
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
  			return
	elif octo==1:
			lf=1
			lb=0
			rf=0
			rb=1
			sl=xq1
			sr=abs(xq1-yq1)
			#print(sl,sr)
			dirl="forward"
			dirR="backward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
	elif octo==2:
			lf=1
			lb=0
			rf=1
			rb=0
			sl=yq1
			sr=abs(yq1-xq1)
			#print(sl,sr)
			dirl="forward"
			dirR="forward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
	elif octo==3:
			lf=1
			lb=0
			rf=1
			rb=0
			sl=abs(yq1-xq2)
			sr=yq1
			#print(sl,sr)
			dirl="forward"
			dirR="forward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
  	elif octo==4:
			lf=0
			lb=1
			rf=1
			rb=0
			sl=abs(xq2-yq1)
			sr=xq2
			#print(sl,sr)
			dirl="backward"
			dirR="forward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
	elif octo==5:
			lf=1
			lb=0
			rf=0
			rb=1
			sr=xq1
			sl=abs(xq1-yq2)
		        #print(sl,sr)
			dirl="forward"
			dirR="backward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
			
	elif octo==6:
			lf=0
			lb=1
			rf=0
			rb=1
			sr=yq2
			sl=abs(yq2-xq1)
			#print(sl,sr)
			dirl="backward"
			dirR="backward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
	elif octo==7:
			lf=0
			lb=1
			rf=0
			rb=1
			sr=abs(yq2-xq2)
			sl=yq2
			
			dirl="backward"
			dirR="backward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			#print(sl,sr)
			return
	elif octo==8:
			sr=abs(xq2-yq2)
			sl=xq2
			
		        #print(sl,sr)
			dirl="backward"
			dirR="forward"
			gpio.output(lfp,lf)
			gpio.output(rfp,rf)
			return
    
			
x=0
y=0 
pwml=0
pwmr=0

try:	
 while(1):
	for events in pygame.event.get():
		if events.type==pygame.JOYAXISMOTION:
			if events.axis==0:
				x=joy.get_axis(0)				
			elif events.axis==1:
				y=joy.get_axis(1)
			


			octant=oct(x,y)
			
			speed(octant,x,y)
			pwml=float(sl)*100/(255)
			pwmr=float(sr)*100/(255)
			print(sl,lf,sr,rf)
			
		
			a.ChangeDutyCycle(pwml)
			b.ChangeDutyCycle(pwmr)
			
			
			#pwm(sr,r)
			
			#gpio.output(lbp,lb)
			#gpio.output(rbp,rb)

	
except KeyboardInterrupt:
				
	a.stop()
	b.stop()	
	gpio.cleanup()        		
	
