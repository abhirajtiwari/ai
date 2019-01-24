import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
echo1=18
trig1=16
echo2=22
trig2=12

GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(echo2,GPIO.IN)


while 1:
    GPIO.output(trig1, False)
    time.sleep(1)

    GPIO.output(trig1, True)
    time.sleep(0.00001)
    GPIO.output(trig1, False)
    tc1=time.time()
    while GPIO.input(echo1) == 0:
        tc2=time.time()
        if ((tc2-tc1)*17000) >400:
            print("forward left")

    t_1s = time.time()
    while GPIO.input(echo1) == 1:
        pass
    t_1e = time.time()
    t_1dur = t_1e - t_1s
    d_1 = t_1dur*(34000/2)
    print(d_1)
    GPIO.output(trig2, False)
    time.sleep(1)

    GPIO.output(trig2, True)
    time.sleep(0.00001)
    GPIO.output(trig2, False)
    tc3=time.time()
    while GPIO.input(echo2) == 0:
        tc4=tim.time()
        if ((tc4-tc3)*17000) >400:
            print("forward right")

        
    t_2s = time.time()
    while GPIO.input(echo2) == 1:
        pass
    t_2e = time.time()
    t_2dur = t_2e - t_2s
    d_2 = t_2dur*(34000/2)
    print(d_2)

    if d_1 > 25 and d_2 > 25:
        print("forward")



    elif d_1 < 25 and d_2 > 25:
        print("turn right")




    elif d_1 < 25 and d_2 < 25:
        print("backward")



    elif d_2 <25 and d_1 >25:
        print("turn left")

GPIO.cleanup()