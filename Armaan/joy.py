import pygame
import time
from pygame import locals
pygame.init()
pygame.joystick.init()
joy=pygame.joystick.Joystick(0)
joy.init()
def map(x,in_min,in_max,out_min,out_max):
	return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min
lf=0

rf=0
lb=0
rb=0
sl=0
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
			#print(sl,sr)
			return
	elif octo==8:
			sr=abs(xq2-yq2)
			sl=xq2
			
		        #print(sl,sr)
			dirl="backward"
			dirR="forward"
			return
    
			
x=0
y=0 
def a():
	print("yo")
	
while(1):
	for events in pygame.event.get():
		if events.type==pygame.JOYAXISMOTION:
			if events.axis==0:
				x=joy.get_axis(0)				
			elif events.axis==1:
				y=joy.get_axis(1)
			


			octant=oct(x,y)
			
			speed(octant,x,y)
			print(sl,dirl,sr,dirR)
	
				
	
        		
	
