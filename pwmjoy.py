import pygame
import mypwm
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

lf = mypwm.mypwm(35, 256)
lb = mypwm.mypwm(36, 256)
rf = mypwm.mypwm(37, 256)
rb = mypwm.mypwm(38, 256)

try:
    x_joy = 0
    y_joy = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value*255 #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-255
        # print x_joy, y_joy
        lpwm = x_joy+y_joy
        rpwm = y_joy-x_joy
        lpwm = max(min(255, lpwm), -255)
        rpwm = max(min(255, rpwm), -255)
        print lpwm, rpwm
        if lpwm > 0:
            lf.analogWrite(abs(lpwm))
        else:
            lb.analogWrite(abs(lpwm))

        if rpwm > 0:
            rf.analogWrite(abs(rpwm))
        else:
            rb.analogWrite(abs(rpwm))

except KeyboardInterrupt:
    pass

pygame.quit()
