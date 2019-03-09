import RPi.GPIO as gpio
import ultrasonic
from rover_connections import *

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

def convertPWMtoDC(speed):
    return (speed/255.) * 100.

def forward(speed):
    #use send packet to set the speed and move forward
    print 'Forward'
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.HIGH)
    gpio.output(motorl, gpio.HIGH)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)
    
def backward(speed):
    print 'Backward'
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.LOW)
    gpio.output(motorl, gpio.LOW)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)

def right0(speed):
    #0 radius right turn
    print '0 radius right'
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.LOW)
    gpio.output(motorl, gpio.HIGH)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)


def left0(speed):
    #0 radius left turn
    print '0 radius left'
    speed = convertPWMtoDC(speed)
    gpio.output(motorr, gpio.HIGH)
    gpio.output(motorl, gpio.LOW)
    lpwm.ChangeDutyCycle(speed)
    rpwm.ChangeDutyCycle(speed)


def uturn(speed):
    print 'uturn'
    frontl = 0
    frontr = 0
    while frontl < front_thresh+5 or frontr < front_thresh+5:
        frontl = ultrasonic.getDistance(echolf, triggerlf)
        frontr = ultrasonic.getDistance(echorf, triggerrf)
        backward(speed)
    right0(speed)

# def sendJoystick(x, y):
    #send the joystick vals

# def sendPacket(packet):
    # send it somehow

