import RPi.GPIO as GPIO
import time

ledpin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledpin,GPIO.OUT)


def pwm(ledpin, value):
    pulse_width = value/255

    print(pulse_width*0.01)
    return pulse_width*0.01



def led_glow(on_time,off_time):
    GPIO.output(ledpin,True)
    time.sleep(on_time)
    GPIO.output(ledpin,False)
    time.sleep(off_time)


while (True):
    on_time = pwm(ledpin, 128)
    off_time = 0.01 - on_time
    led_glow(on_time,off_time)
