import RPi.GPIO as gpio
import time
from rover_connections import *

# gpio.setmode(gpio.BCM)

def trigger(pin):
    gpio.output(pin, gpio.LOW)
    # time.sleep(5e-6) #time to clean up for the ultrasonic sensor
    time.sleep(0.022)
    gpio.output(pin, gpio.HIGH) # TIMING????
    time.sleep(1e-5)
    gpio.output(pin, gpio.LOW)

def pulseRead(pin, level):
    t1 = 0
    t2 = 0

    t1 = round(time.time() * 1e6)
    while gpio.input(pin) != level:
        t2 = round(time.time() * 1e6)
        if t2-t1 > 17400:
            # print 'broke here'
            return 300
        pass

    #t1 = t2 = 0
    t1 = round(time.time() * 1e6)
    while gpio.input(pin) ==  level:
        t2 = round(time.time() * 1e6)
        if t2-t1 > 17400:
            # print 'broke'
            break
    return t2-t1

def getDistance(pinEcho, pinTrigger):
    trigger(pinTrigger)
    return pulseRead(pinEcho, gpio.HIGH)/58

if __name__ == '__main__':
    gpio.setmode(gpio.BCM)
    trig = triggerrs
    echo = echors

    gpio.setup(echo, gpio.IN)
    gpio.setup(trig, gpio.OUT)


    try:
        while True:
            distance = getDistance(echo, trig)
            print distance

    except KeyboardInterrupt:
        pass

    gpio.cleanup()
    print 'Done'

    

