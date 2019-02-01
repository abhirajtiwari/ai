import RPi.GPIO as GPIO
import pygame # controller
import math
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

left_fwd=18
left_bkwd=16
right_fwd=22
right_bkwd=12
GPIO.setup(left_fwd,GPIO.OUT)
GPIO.setup(left_bkwd, GPIO.OUT)
GPIO.setup(right_fwd, GPIO.OUT)
GPIO.setup(right_bkwd, GPIO.OUT)
a=GPIO.PWM(left_fwd,100)
b=GPIO.PWM(left_bkwd,100)
c=GPIO.PWM(right_fwd,100)
d=GPIO.PWM(right_bkwd,100)
a.start(0)
b.start(0)
c.start(0)
d.start(0)







# Initialize pygame

# get joystick readings
#def joysticks():




# control speed
pygame.init()
pygame.display.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
try:
    j = pygame.joystick.Joystick(0)  # create a joystick instance
    j.init()  # init instance
    print("Enabled joystick:")
except pygame.error:
    print("no joystick found.")







def robospeed():
    global xAxis, yAxis

    pygame.event.get()

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        xAxis = joystick.get_axis(0)
        if xAxis>1:
            xAxis=1
        if xAxis<-1:
            xAxis=-1
        yAxis = joystick.get_axis(1)
        if yAxis<-1:
            yAxis=-1
        if yAxis>1:
            yAxis=1

    global motorSpeedA, motorSpeedB, x1, x2, y1, y2
    x1 = math.floor(xAxis * 255)
    x2 = math.floor(xAxis * -255)
    y1 = math.floor(yAxis * -255)
    y2 = math.floor(yAxis * 255)
    #print(xAxis,yAxis)
    #print(yAxis)

    if yAxis == 0 and xAxis == 0:
        motorSpeedA = 0
        motorSpeedB = 0
        a.ChangeDutyCycle(0)
        b.ChangeDutyCycle(0)
        c.ChangeDutyCycle(0)
        d.ChangeDutyCycle(0)
        print(motorSpeedA)
        print(motorSpeedB)


    elif yAxis < 0:
        #y2=-y2
        if yAxis < xAxis and xAxis < 0:
            motorSpeedA =abs(y2)
            motorSpeedB = abs(x2 - y2)
            if motorSpeedB>255:
                motorSpeedB=255

            print('oct6')
            oct6()


            #leftBackward()
            #rightBackward()







        elif yAxis <  - xAxis and xAxis > 0:

            motorSpeedA = abs(x1 - y2)
            if motorSpeedA>255:
                motorSpeedA=255
            motorSpeedB = abs(y2)
            print('oct7')
            oct7()


            #leftBackward()
            #rightBackward()






        elif yAxis > xAxis and xAxis < 0:

            motorSpeedA = abs(x2 - y2)
            motorSpeedB = abs(x2 + y2)
            if motorSpeedB>255:
                motorSpeedB=255
            if motorSpeedA>255:
                motorSpeedA=255
            print('oct5')
            oct5()

            #leftBackward()
            #rightForward()




        elif yAxis >  - xAxis and xAxis > 0:

            motorSpeedA = abs(x1 + y2)
            if motorSpeedA>255:
                motorSpeedA=255
            motorSpeedB = abs(x1 - y2)
            if motorSpeedB>255:
                motorSpeedB=255
            print('oct8')
            oct8()

            #leftForward()
            #rightBackward()






    elif yAxis > 0:
        if yAxis > xAxis and xAxis > 0:
            motorSpeedA = abs(y1)
            motorSpeedB = abs(x1 - y1)
            if motorSpeedB>255:
                motorSpeedB=255
            print('oct2')
            oct2()

            #leftForward()
            #rightForward()




        elif yAxis < xAxis and xAxis > 0:
            motorSpeedA = abs(x1 + y1)
            if motorSpeedA>255:
                motorSpeedA=255
            motorSpeedB = abs(x1 - y1)
            if motorSpeedB>255:
                motorSpeedB=255
            print('oct1')
            oct1()

            '''leftForward()
            rightBackward()'''









        elif yAxis >  - xAxis and xAxis < 0:
            motorSpeedA = abs(x2 - y1)
            if motorSpeedA>255:
                motorSpeedA=255

            motorSpeedB = abs(y1)
            print('oct3')
            oct3()

            #leftForward()

            #rightForward()









        elif yAxis <  - xAxis and xAxis < 0:

            motorSpeedA =abs(x2 - y1)
            if motorSpeedA>255:
                motorSpeedA=255
            motorSpeedB = abs(x2 + y1)
            if motorSpeedB>255:
                motorSpeedB=255

            print('oct4')
            oct4()

            #leftBackward()
            #rightForward()




        #while True:




def oct1():
    a.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    b.ChangeDutyCycle(0)
    c.ChangeDutyCycle(0)
    d.ChangeDutyCycle((motorSpeedB/255)*100)
    print('rightbackward')

    print('leftforward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct2():
    a.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    b.ChangeDutyCycle(0)
    c.ChangeDutyCycle((motorSpeedB/255)*100)
    d.ChangeDutyCycle(0)
    print('rightforward')

    print('leftforward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct3():
    a.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    b.ChangeDutyCycle(0)
    c.ChangeDutyCycle((motorSpeedB/255)*100)
    d.ChangeDutyCycle(0)
    print('rightforward')

    print('leftforward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct4():
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    c.ChangeDutyCycle((motorSpeedB/255)*100)
    d.ChangeDutyCycle(0)
    print('rightForward')

    print('leftBackward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct5():
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    c.ChangeDutyCycle((motorSpeedB/255)*100)
    d.ChangeDutyCycle(0)
    print('rightForward')

    print('leftBackward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct6():
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    c.ChangeDutyCycle(0)
    d.ChangeDutyCycle((motorSpeedB/255)*100)
    print('rightbackward')

    print('leftbackward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct7():
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    c.ChangeDutyCycle(0)
    d.ChangeDutyCycle((motorSpeedB/255)*100)
    print('rightBackward')

    print('leftbackward')
    print(motorSpeedA)
    print(motorSpeedB)
def oct8():
    a.ChangeDutyCycle((motorSpeedA/255.0)*100.0)
    b.ChangeDutyCycle(0)
    c.ChangeDutyCycle(0)
    d.ChangeDutyCycle((motorSpeedB/255)*100)
    print('rightbackward')

    print('leftforward')
    print(motorSpeedA)
    print(motorSpeedB)




















# -------------------Main Program--------------------------
while True:
    time.sleep(0.1)
    robospeed()


    #print (motorSpeedA, motorSpeedB)
