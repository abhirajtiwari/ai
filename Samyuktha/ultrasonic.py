import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
echo1=18
trig1=16
echo2=27
trig2=12

GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(echo2,GPIO.IN)

#GPIO.output(trig2,False)
while 1:
    GPIO.output(trig1, False)
    time.sleep(0.00001)
    GPIO.output(trig1, True)
    # GPIO.output(trig2,True)
    time.sleep(0.00001)
    GPIO.output(trig1, False)
    while GPIO.input(echo1) == 1:
        pass
    t_1s = time.time()
    while GPIO.input(echo1) == 0:
        pass
    t_1e = time.time()
    t_1dur = t_1e - t_1s
    d_1 = t_1dur * (0.34/2)
    print(d_1)
    GPIO.output(trig2, False)
    # GPIO.output(trig2,False)
    time.sleep(0.00001)
    GPIO.output(trig2, True)
    # GPIO.output(trig2,True)
    time.sleep(0.00001)
    GPIO.output(trig2, False)
    while GPIO.input(echo2) == 1:
        pass
    t_2s = time.time()
    while GPIO.input(echo2) == 0:
        pass
    t_2e = time.time()
    t_2dur = t_2e - t_2s
    d_2 = t_2dur * (0.34/2)
    print(d_2)
    if d_1 > 15 and d_2 > 15:
        print("forward")
        # frd()


    elif d_1 <= 15 and d_2 > 15:
        print("turn right")
        #tr()



    elif d_1 < 15 and d_2 < 15:
        print("backward")
        #bk()






    elif d_2 <= 15 and d_1 > 15:
        print("turn left")
        #tl()


'''def bk():
      GPIO.output(mlf, False)
      GPIO.output(mrf, False)
      GPIO.output(mlb, True)
      GPIO.output(mrf, True)

      print("backward")









 def frd():
  GPIO.output(mlf,True)
  GPIO.output(mrf,True)
  GPIO.output(mlb,False)
  GPIO.output(mrb,False)
  print("forward")





def tl():
    GPIO.output(mrf, False)
    GPIO.output(mrb, True)
    GPIO.output(mlf, True)
    GPIO.output(mlb, False)
    print("turn left")



def tr():
    GPIO.output(mlb, True)
    GPIO.output(mlf, False)
    GPIO.output(mrb, False)
    GPIO.output(mrf, True)
    print("turn right")'''











