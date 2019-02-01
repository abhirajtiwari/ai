import pygame
import RPi.GPIO as GPIO
import time


pygame.init()
pygame.joystick.init()

joyStick = pygame.joystick.Joystick(0)
joyStick.init()

x_value = 0.00
y_value = 0.00


l_fwd = 35                      #change the pins
r_fwd = 36                      #change the pins
l_bck = 37                      #change the pins
r_bck = 38                      #change the pins

GPIO.setmode(GPIO.BOARD)
GPIO.setup(l_fwd,GPIO.OUT)
GPIO.setup(l_bck,GPIO.OUT)
GPIO.setup(r_fwd,GPIO.OUT)
GPIO.setup(r_bck,GPIO.OUT)


pwmLF = GPIO.PWM(35,1000)
pwmRF = GPIO.PWM(36,1000)
pwmLB = GPIO.PWM(37,1000)
pwmRB = GPIO.PWM(38,1000)





pwmLF.start(0.00)
pwmRF.start(0.00)
pwmLB.start(0.00)
pwmRB.start(0.00)


def oct1():
    dutyLF = x_pwm*100.00000/255.00000
    dutyRB = (255-y_pwm)*100.00000/255.00000

    pwmLF.ChangeDutyCycle(dutyLF)
    pwmRB.ChangeDutyCycle(dutyRB)
    print(x_pwm)
    print(255-y_pwm)


def oct2():
    dutyLF = y_pwm*100.00000/255.00000
    dutyRF = (y_pwm - x_pwm)*100.00000/255.00000

    pwmLF.ChangeDutyCycle(dutyLF)
    pwmRF.ChangeDutyCycle(dutyRF)
    print(y_pwm)
    print(y_pwm - x_pwm)


def oct3():
    dutyLF = (y_pwm - x_pwm)*100.00000/255.00000
    dutyRF = y_pwm*100.00000/255.00000

    pwmLF.ChangeDutyCycle(dutyLF)
    pwmRF.ChangeDutyCycle(dutyRF)
    print(y_pwm - x_pwm)
    print(y_pwm)


def oct4():
    dutyLB = (x_pwm - y_pwm)*100.00000/255.00000
    dutyRF = x_pwm*100.00000/255.00000

    pwmLB.ChangeDutyCycle(dutyLB)
    pwmRF.ChangeDutyCycle(dutyRF)
    print(x_pwm - y_pwm)
    print(x_pwm)


def oct5():
    dutyLB = x_pwm*100.00000/255.00000
    dutyRF = (x_pwm - y_pwm)*100.00000/255.00000

    pwmLB.ChangeDutyCycle(dutyLB)
    pwmRF.ChangeDutyCycle(dutyRF)
    print(x_pwm)
    print(x_pwm - y_pwm)


def oct6():
    dutyLB = y_pwm*100.00000/255.00000
    dutyRB = (y_pwm - x_pwm)*100.00000/255.00000

    pwmLB.ChangeDutyCycle(dutyLB)
    pwmRB.ChangeDutyCycle(dutyRB)
    print(y_pwm)
    print(y_pwm - x_pwm)

def oct7():
    dutyLB = (y_pwm - x_pwm)*100.00000/255.00000
    dutyRB = y_pwm*100.00000/255.00000

    pwmLB.ChangeDutyCycle(dutyLB)
    pwmRB.ChangeDutyCycle(dutyRB)
    print(y_pwm - x_pwm)
    print(y_pwm)


def oct8():
    dutyLF = (x_pwm - y_pwm)*100.00000/255.00000
    dutyRB = x_pwm*100.00000/255.00000

    pwmLF.ChangeDutyCycle(dutyLF)
    pwmRB.ChangeDutyCycle(dutyRB)
    print(x_pwm - y_pwm)
    print(x_pwm)

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
        pwmLF.ChangeDutyCycle(0.00)
        pwmRF.ChangeDutyCycle(0.00)
        pwmLB.ChangeDutyCycle(0.00)
        pwmRB.ChangeDutyCycle(0.00)

    	if(x_value == 0 and y_value ==0):
            print('center')


        print('loop')

        #quad 1
        if(x_value >= 0 and y_value >= 0):
            if(x_value - y_value >= 0):
                print('oct 1')
                oct1()

            else:
                print('oct 2')
                oct2()
        #quad 3
        if(x_value <= 0 and y_value <= 0):
            if(x_value - y_value <= 0):
                print('oct 5')
                oct5()
            else:
                print('oct 6')
                oct6()
        #quad 2
        if(x_value <= 0 and y_value >= 0):
            if(x_value + y_value >= 0):
                print('oct 3')
                oct3()
            else:
                print('oct 4')
                oct4()
        #quad 4
        if(x_value >= 0 and y_value <= 0):
            if(x_value + y_value >= 0):
                print('oct 8')
                oct8()
            else:
                print('oct 7')
                oct7()

print('not on any axis')
