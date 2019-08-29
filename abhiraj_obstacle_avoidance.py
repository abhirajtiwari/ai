import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

echol = 18
trigl = 16
echor = 27 
trigr = 12

# mrf = 
# mrb = 
# mlf = 
# mlb = 

gpio.setup(echor, gpio.IN)
gpio.setup(trigr, gpio.OUT)
gpio.setup(echol, gpio.IN)
gpio.setup(trigl, gpio.OUT)
# gpio.setup(mrf, gpio.OUT)
# gpio.setup(mrb, gpio.OUT)
# gpio.setup(mlf, gpio.OUT)
# gpio.setup(mlb, gpio.OUT)

def trigger(pin):
    gpio.output(pin, gpio.LOW)
    # time.sleep(5e-6) #time to clean up for the ultrasonic sensor
    time.sleep(0.1)
    gpio.output(pin, gpio.HIGH) # TIMING????
    time.sleep(1e-5)
    gpio.output(pin, gpio.LOW)

def pulseRead(pin, level):
    while gpio.input(pin) != level:
        pass
    t1 = round(time.time() * 1e6)
    while gpio.input(pin) ==  level:
        t2 = round(time.time() * 1e6)
        if t2-t1 > 17400:
            break
    return t2-t1

def forward():
    # gpio.output(mrf, gpio.HIGH)
    # gpio.output(mlf, gpio.HIGH)
    # gpio.output(mrb, gpio.LOW)
    # gpio.output(mlb, gpio.LOW)
    print 'fwd'

def right():
    # gpio.output(mlf, gpio.HIGH)
    # gpio.output(mrb, gpio.HIGH)
    # gpio.output(mlb, gpio.LOW)
    # gpio.output(mrf, gpio.LOW)
    print 'right'

def left():
    # gpio.output(mrf, gpio.HIGH)
    # gpio.output(mlb, gpio.HIGH)
    # gpio.output(mrb, gpio.LOW)
    # gpio.output(mlf, gpio.LOW)
    print 'left'

def backward():
    # gpio.output(mrb, gpio.HIGH)
    # gpio.output(mlb, gpio.HIGH)
    # gpio.output(mrf, gpio.LOW)
    # gpio.output(mlf, gpio.LOW)
    print 'bwd'

def uturn(distl, distr, mindist=30):
    while distl < mindist or distr < mindist:
        backward()
        trigger(trigl)
        distl = pulseRead(echol, gpio.HIGH)/58
        trigger(trigr)
        distr = pulseRead(echor, gpio.HIGH)/58
    left()

try:
    while True:
        trigger(trigl)
        durationl = pulseRead(echol, gpio.HIGH)
        distancel = durationl/58

        trigger(trigr)
        durationr = pulseRead(echor, gpio.HIGH)
        distancer = durationr/58

        mindist = 30

        if mindist < distancer and distancel < mindist:
            right()
        elif distancel > mindist and distancer < mindist:
            left()
        elif distancel < mindist and distancer < mindist:
            uturn(distancel, distancer, mindist)
        else:
            forward()

except KeyboardInterrupt:
    pass

gpio.cleanup()
print 'Done' 
