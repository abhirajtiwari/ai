import pygame.display
import os
import sys
import pygame
from pygame import locals
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#frequency=100Hz

ledpin=35

t_on=0.00
t_off=0.00
f=0
GPIO.setup(ledpin,GPIO.OUT)

def pwm(pin,a):
    d_cycle=a/255
    t_on = d_cycle*0.01
    t_off =0.01-t_on
      
    t1=time.time()
    
    while(True):  
        
         
        t2=time.time()
        t3=t2-t1
        if(t3<t_on):
	 	GPIO.output(ledpin, True)
        elif:
		break

    t4=time.time()

    while(True):
	t5=time.time()
        t6=t5-t4
	if(t6<t_off):
		GPIO.output(ledpin, False)
        elif:
		break


while(True):

                x=255       
   		pwm(ledpin,x)
      
GPIO.cleanup()     
