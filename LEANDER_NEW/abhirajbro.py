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

GPIO.setup(ledpin,GPIO.OUT)

def pwm(pin,a):
    d_cycle=a/255
    t_on = d_cycle*0.01
    t_off =0.01-t_on
      
    t1=time.time()
    
    while(True):  
          
        t2=time.time()
        t3=t2-t1
        if(t3>t_on):
	   break	

        GPIO.output(ledpin, True)
        
    GPIO.output(ledpin, False)
     

while(True):

        x=0
	for x in range(0, 255, 5):               
   		pwm(ledpin,x)
      
GPIO.cleanup()     
