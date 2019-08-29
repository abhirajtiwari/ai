import RPi.GPIO as gpio
import time

class mypwm:
    def __init__(self, p, t):
        self.pin = p
        gpio.setup(self.pin, gpio.OUT)
        self.top = t
        self.counter = 0
        self.compare = 0
        self.state = gpio.HIGH

    def analogWrite(self, val):
        assert val<=self.top
        assert val>=0
        self.compare = val
        self.counter = self.counter + 1
        gpio.output(self.pin, self.state)
        if self.compare == self.counter:
            self.state = not self.state
        elif self.counter == self.top:
            self.counter = 0
            self.state = not self.state



        

    
