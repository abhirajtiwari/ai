#this code resolves the 13ft issue in ultrasonic


import RPi.GPIO as GPIO
import time
#setting ultrasonc pins

GPIO.setmode(GPIO.BOARD)

echo_left = 18
trigger_left = 16
echo_right = 22
trigger_right = 12
#***********************

#setting motor pins

#left_ledf = 1
#left_ledb = 2
#right_ledf = 3
#right_ledb = 4

#********************

#setting output/input
GPIO.setup(trigger_left, GPIO.OUT)
GPIO.setup(echo_left, GPIO.IN)

GPIO.setup(trigger_right, GPIO.OUT)
GPIO.setup(echo_right, GPIO.IN)

#GPIO.setup(left_ledf,GPIO.output)
#GPIO.setup(left_ledb,GPIO.output)
#GPIO.setup(right_ledf,GPIO.output)
#GPIO.setup(right_ledb,GPIO.output)


#ALGORITHM***********************
while True:
#******************sensor left

    GPIO.output(trigger_left,False)
    time.sleep(0.1)



    GPIO.output(trigger_left,True)
    time.sleep(0.00001)
    GPIO.output(trigger_left,False)


    while GPIO.input(echo_left)==0:
        pass
    lpulse_begins = time.time()



    while GPIO.input(echo_left)==1:
        lpulse_stops= time.time()
        if(lpulse_stops-lpulse_begins>0.005):
            break



    pulse_duration_left = lpulse_stops - lpulse_begins
    distance_left = pulse_duration_left * 34000/2
#*****************************************

#**************sensor right
    GPIO.output(trigger_right,False)
    time.sleep(0.1)

    GPIO.output(trigger_right,True)
    time.sleep(0.00001)
    GPIO.output(trigger_right,False)

    while GPIO.input(echo_right)==0:
        pass
    rpulse_begins = time.time()

    while GPIO.input(echo_right)==1:
        rpulse_stops= time.time()
        if(rpulse_stops-rpulse_begins>0.005):
            break

    pulse_duration_right = rpulse_stops - rpulse_begins
    distance_right = pulse_duration_right * 34000/2
#****************************************
    #print('distance_left',distance_left)
    #print('distance_right',distance_right)
    #print('pulse right', pulse_duration_right)
    #print('pulse left',pulse_duration_left)





    if(distance_left>=25 and distance_right>=25):
        print('straight')
        #straight()

    if(distance_left<=25 and distance_right>=25):
        print('right')
        #right()

    if(distance_left>=25 and distance_right<=25):
        print('left')

    if(distance_left<=15 and distance_right<=15 and distance_left <= distance_right and distance_left>10):
        print('sharp_right')
        #sharp_right()

    if(distance_left<=15 and distance_right<=15 and distance_left > distance_right and distance_left>10):
        print('sharp_left')
        #sharp_left()

    if(distance_left<=10 and distance_right<=10):
        print('back')



GPIO.cleanup()





'''
def straight():
    #GPIO.OUTPUT(left_ledf, HIGH)
    #GPIO.OUTPUT(left_ledb, LOW)
    #GPIO.OUTPUT(right_ledf, HIGH)
    #GPIO.OUTPUT(right_ledb, LOW)
    print('straight')

def right():
    #GPIO.OUTPUT(left_ledf,HIGH)
    #GPIO.OUTPUT(left_ledb,LOW)
    #GPIO.OUTPUT(right_ledf,LOW)
    #GPIO.OUTPUT(right_ledb,LOW)
    print('right')

def left():
    #GPIO.OUTPUT(left_front,LOW)
    #GPIO.OUTPUT(left_back,LOW)
    #GPIO.OUTPUT(right_front,HIGH)
    #GPIO.OUTPUT(right_back,LOW)
    print('left')

def sharp_left():
    #GPIO.OUTPUT(left_front, LOW)
    #GPIO.OUTPUT(left_back, HIGH)
    #GPIO.OUTPUT(right_front, HIGH)
    #GPIO.OUTPUT(right_back, LOW)
    print('sharp left')

def sharp_left():
    #GPIO.OUTPUT(left_front, HIGH)
    #GPIO.OUTPUT(left_back, LOW)
    #GPIO.OUTPUT(right_front, LOW)
    #GPIO.OUTPUT(right_back, HIGH)
    print('sharp right')

'''
