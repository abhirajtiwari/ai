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

    if t_on>0:
        GPIO.output(ledpin, True)
        time.sleep(t_on)

    else:
        GPIO.output(ledpin, False)
        time.sleep(t_off)

while(True):

        x=0
	for x in range(0,255,20):               
   		pwm(ledpin,x)
      
GPIO.cleanup()     
