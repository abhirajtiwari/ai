import pygame
import RPi.GPIO as GPIO
import time


pygame.init()
pygame.joystick.init()

joyStick = pygame.joystick.Joystick(0)
joyStick.init()

x_value = 0.00
y_value = 0.00


GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledpin,GPIO.OUT)

l_fwd = 35                      #change the pins
r_fwd = 36                      #change the pins
l_bck = 37                      #change the pins
r_bck = 38                      #change the pins


def pwm(ledpin, pwm_value):
    pulse_width = pwm_value*1.00000/255.00000

    #print(pulse_width*0.00001)
    return pulse_width*0.00001




def led_glow(on_timeL,off_timeL,on_timeR,off_timeR,pinL,pinR):
    GPIO.output(pinL,True)
    time.sleep(on_timeL)
    GPIO.output(pinL,False)
    time.sleep(off_timeL)

    GPIO.output(pinR,True)
    time.sleep(on_timeR)
    GPIO.output(pinR,False)
    time.sleep(off_timeR)


def oct1():
    led_left_fwd = x_pwm
    led_right_bck = 255 - y_pwm
    print(x_pwm)
    print(255-y_pwm)
    on_time_lf = pwm(l_fwd, 200)
    off_time_lf = 0.00001 - on_time_lf
    on_time_rb = pwm(r_bck, 40)
    off_time_rb = 0.00001 - on_time_rb
    led_glow(on_time_lf,off_time_lf,on_time_rb,off_time_rb,l_fwd,r_bck)


def oct2():
    led_left_fwd = y_pwm
    led_right_fwd = y_pwm - x_pwm
    print(y_pwm)
    print(y_pwm - x_pwm)
    on_time_lf = pwm(l_fwd, y_pwm)
    off_time_lf = 0.00001 - on_time_lf
    on_time_rf = pwm(r_fwd, y_pwm - x_pwm)
    off_time_rf = 0.00001 - on_time_rf
    led_glow(on_time_lf,off_time_lf,on_time_rf,off_time_rf,l_fwd,r_fwd)

def oct3():
    led_left_fwd = y_pwm - x_pwm
    led_right_fwd = y_pwm
    print(y_pwm - x_pwm)
    print(y_pwm)
    on_time_lf = pwm(l_fwd, y_pwm - x_pwm)
    off_time_lf = 0.00001 - on_time_lf
    on_time_rf = pwm(r_fwd, y_pwm)
    off_time_rf = 0.00001 - on_time_rf
    led_glow(on_time_lf,off_time_lf,on_time_rf,off_time_rf,l_fwd,r_fwd)

def oct4():
    led_left_bck = x_pwm - y_pwm
    led_right_fwd = x_pwm
    print(x_pwm - y_pwm)
    print(x_pwm)
    on_time_lb = pwm(l_bck, x_pwm - y_pwm)
    off_time_lb = 0.00001 - on_time_lb
    on_time_rf = pwm(r_fwd, x_pwm)
    off_time_rf = 0.00001 - on_time_rf
    led_glow(on_time_lb,off_time_lb,on_time_rf,off_time_rf,l_bck,r_fwd)

def oct5():
    led_left_fwd = x_pwm
    led_right_bck = x_pwm - y_pwm
    print(x_pwm)
    print(x_pwm - y_pwm)
    on_time_lb = pwm(l_fwd, x_pwm)
    off_time_lb = 0.00001 - on_time_lb
    on_time_rf = pwm(r_bck, x_pwm - y_pwm)
    off_time_rf = 0.00001 - on_time_rf
    led_glow(on_time_lb,off_time_lb,on_time_rf,off_time_rf,l_fwd,r_bck)

def oct6():
    led_left_bck = y_pwm
    led_right_bck = y_pwm - x_pwm
    print(y_pwm)
    print(y_pwm - x_pwm)
    on_time_lb = pwm(l_bck, y_pwm)
    off_time_lb = 0.00001 - on_time_lb
    on_time_rb = pwm(r_bck, y_pwm - x_pwm)
    off_time_rb = 0.00001 - on_time_rb
    led_glow(on_time_lb,off_time_lb,on_time_rb,off_time_rb,l_bck,r_bck)

def oct7():
    led_left_bck = y_pwm - x_pwm
    led_right_bck = y_pwm
    print(y_pwm - x_pwm)
    print(y_pwm)
    on_time_lb = pwm(l_bck, y_pwm - x_pwm)
    off_time_lb = 0.00001 - on_time_lb
    on_time_rb = pwm(r_bck, y_pwm)
    off_time_rb = 0.00001 - on_time_rb
    led_glow(on_time_lb,off_time_lb,on_time_rb,off_time_rb,l_bck,r_bck)

def oct8():
    led_left_fwd = x_pwm - y_pwm
    led_right_bck = x_pwm
    print(x_pwm - y_pwm)
    print(x_pwm)
    on_time_lf = pwm(l_fwd, x_pwm - y_pwm)
    off_time_lf = 0.00001 - on_time_lf
    on_time_rb = pwm(r_bck, x_pwm)
    off_time_rb = 0.00001 - on_time_rb
    led_glow(on_time_lf,off_time_lf,on_time_rb,off_time_rb,l_fwd,r_bck)

while True:
    for event in pygame.event.get():
        if(event.type == pygame.JOYAXISMOTION):
            if(event.axis==0):
                x_value = joyStick.get_axis(0)  #gets the position of the joystick on x axis
            elif(event.axis==1):
                y_value = -joyStick.get_axis(1)

        else:
            print('not on the axis')

        x_pwm = abs(round(x_value * 255))
        y_pwm = abs(round(y_value * 255))
        #print('x_value', x_pwm)
        #print('y_value', y_pwm)


    	if(x_value == 0 and y_value ==0):
	    print('center')




        #quad 1
        if(x_value > 0 and y_value > 0):
            if(x_value - y_value >= 0):
                print('oct 1')
                oct1()
            else:
                print('oct 2')
                oct2()
        #quad 3
        if(x_value < 0 and y_value < 0):
            if(x_value - y_value <= 0):
                print('oct 5')
                oct5()
            else:
                print('oct 6')
                oct6()
        #quad 2
        if(x_value < 0 and y_value > 0):
            if(x_value + y_value >= 0):
                print('oct 3')
                oct3()
            else:
                print('oct 4')
                oct4()
        #quad 4
        if(x_value > 0 and y_value < 0):
            if(x_value + y_value >= 0):
                print('oct 8')
                oct8()
            else:
                print('oct 7')
                oct7()

print('not on any axis')
