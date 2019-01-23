import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
trig1=16
echo1=18
trig2=12
echo2=22
GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(echo2,GPIO.IN)

"""lf
lb
rf
rb"""
def left():
    """GPIO.output(lf,1)
    GPIO.output(lb,0)
    GPIO.output(rf,0)
    GPIO.output(rb,1)
"""
    print("left")
    return   
 
def right():
    """GPIO.output(lf,0)
    GPIO.output(lb,1)
    GPIO.output(rf,1)
    GPIO.output(rb,0)
"""    
    print("right")    
    return
def front():
    """GPIO.output(lf,1)
    GPIO.output(lb,0)
    GPIO.output(rf,1)
    GPIO.output(rb,0)
"""    
    print("front")    
    return
def back():
    """GPIO.output(lf,0)
    GPIO.output(lb,1)
    GPIO.output(rf,0)
    GPIO.output(rb,1)
"""    
    print("back")
    return
def brutestop():
    while(d1<5 or d2<5):
        time.sleep(0.01)
        back()
        trigger(trig1)
        d1=pulsein(echo1)
        trigger(trig2)
        d2=pulsein(echo2)
        
    if(d1<d2):
        right()
        time.sleep(1)
    else:
        left()
        time.sleep(1)

def trigger(trig):
     GPIO.output(trig1,GPIO.LOW)
     time.sleep(0.1)
     GPIO.output(trig1,GPIO.HIGH)
     time.sleep(0.00001)
     GPIO.output(trig1,GPIO.LOW)
     return 

def pulsein(echo):
 while(GPIO.input(echo)==0):
     pass
 t1=time.time()
 while(GPIO.input(echo)==1):
     pass
 t2=time.time()
 d=(t2-t1)*17150
 d=round(d,2)
 
 return d

 









while(1):
 trigger(trig1)
 d1=pulsein(echo1)
 print("got d1")
 
 trigger(trig2)
 d2=pulsein(echo2)
 print("got d2")
 
 if(d1<5 or d2<5):
    print("back")
 if(d1<d2):
     if(d1<20):
        
        right()
        
 elif(d2<20):
         
     left()
             
 elif(d1>20 and d2>20):
     front()
 time.sleep(0.01)
GPIO.cleanup()
     
             
     
  
    
 

 
   
 
   
 

 
   
 
