import RPi.GPIO as gpio
import time
import ultrasonic
from rover_connections import *
import justimu

# motorl = 9 
# motorlp = 11
# motorr = 23
# motorrp = 24
#
# gpio.setup(motorl, gpio.OUT)
# gpio.setup(motorlp, gpio.OUT)
# gpio.setup(motorr, gpio.OUT)
# gpio.setup(motorrp, gpio.OUT)
#
# lpwm = gpio.PWM(motorlp, 50)
# rpwm = gpio.PWM(motorrp, 50)
#
# lpwm.start(0)
# rpwm.start(0)
#
# triggerrf = 14
# echorf = 15
# triggerlf = 27
# echolf = 17
# triggerrs = 20
# echors = 21
# triggerls = 26
# echols = 19

forward_sleep = 5

def convertPWMtoDC(speed):
    return (speed/255.) * 100.

def forward(speed):
    #use send packet to set the speed and move forward
    print 'Forward'
    atser.write(chr(1))
    '''
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.HIGH)
    gpio.output(motorl, gpio.HIGH)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)
    '''

def backward(speed):
    print 'Backward'
    atser.write(chr(2))
    '''
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.LOW)
    gpio.output(motorl, gpio.LOW)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)
    '''

def right0(speed):
    #0 radius right turn
    print '0 radius right'
    atser.write(chr(3))
    '''
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.LOW)
    gpio.output(motorl, gpio.HIGH)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)
    '''


def left0(speed):
    #0 radius left turn
    print '0 radius left'
    atser.write(chr(4))
    '''
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.HIGH)
    gpio.output(motorl, gpio.LOW)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)
    '''

def right90(speed):
    curr_head = justimu.getHead()
    final_head = (curr_head + 90)%360
    while abs(final_head - curr_head) >= 10:
        right0(speed)
        curr_head = justimu.getHead()
    forward(speed)
    time.sleep(forward_sleep)

def left90(speed):
    curr_head = justimu.getHead()
    final_head = (curr_head + 270)%360
    while abs(final_head - curr_head) >= 10:
        left0(speed)
        curr_head = justimu.getHead()
    forward(speed)
    time.sleep(forward_sleep)

def uturn(speed):
    print 'uturn'
    frontl = 0
    frontr = 0
    while frontl < front_thresh+5 or frontr < front_thresh+5:
        frontl = ultrasonic.getDistance(echolf, triggerlf)
        frontr = ultrasonic.getDistance(echorf, triggerrf)
        backward(speed)
    right0(speed)

def stop():
    print 'stop'
    atser.write(chr(5))
    '''
    lpwm.ChangeDutyCycle(0)
    rpwm.ChangeDutyCycle(0)
    '''

def clean():
    gpio.cleanup()
# def sendJoystick(x, y):
    #send the joystick vals

# def sendPacket(packet):
    # send it somehow

