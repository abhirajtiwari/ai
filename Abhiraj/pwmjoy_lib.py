import pygame
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

gpio.setup([35,36,37,38], gpio.OUT)


lf = gpio.PWM(35, 50)
lb = gpio.PWM(36, 50)
rf = gpio.PWM(37, 50)
rb = gpio.PWM(38, 50)
lf.start(0)
lb.start(0)
rf.start(0)
rb.start(0)

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
        if lpwm >= 0:
            lf.ChangeDutyCycle((abs(lpwm)/255) * 100)
            lb.ChangeDutyCycle(0)
        else:
            lb.ChangeDutyCycle((abs(lpwm)/255) * 100)
            lf.ChangeDutyCycle(0)

        if rpwm >= 0:
            rf.ChangeDutyCycle(abs(rpwm)/255 * 100)
            rb.ChangeDutyCycle(0)
        else:
            rb.ChangeDutyCycle(abs(rpwm)/255 * 100)
            rf.ChangeDutyCycle(0)

except KeyboardInterrupt:
    pass
gpio.cleanup()
pygame.quit()
