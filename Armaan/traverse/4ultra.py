import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
trig1=27
echo1=17
trig2=14
echo2=15
trig3=26
echo3=19
trig4=20
echo4= 21
GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(trig2,GPIO.OUT)
GPIO.setup(trig3,GPIO.OUT)
GPIO.setup(trig4,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
GPIO.setup(echo2,GPIO.IN)
GPIO.setup(echo3,GPIO.IN)
GPIO.setup(echo4,GPIO.IN)

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
def brutestop(dl,dr):
    while(dl<5 or dr<5):
       # print("entered loop")
        #time.sleep(0.01)
        back()
        trigger(trig1)
        dl=pulsein(echo1)
        trigger(trig2)
        dr=pulsein(echo2)
        
    if(dl<dr):
        right()
        #time.sleep(0.01)
    else:
        left()
        #time.sleep(0.01)

def trigger(trig):
     GPIO.output(trig,GPIO.LOW)
     time.sleep(0.001)
     GPIO.output(trig,GPIO.HIGH)
     time.sleep(0.00001)
     GPIO.output(trig,GPIO.LOW)
     return 

def pulsein(echo):
# flag=0
 
 while(GPIO.input(echo)==0):
     #print("in zero")
     pass
 t1=time.time()
 while(GPIO.input(echo)==1):
     #print("in 1")
     t2=time.time()
     if ((t2-t1>0.0233)):
           break
  
     
 #t2=time.time()
 d=(t2-t1)*17150
 d=round(d,2)
 
 return d

 








try:
 while(1):
	 trigger(trig1)
	 d1=pulsein(echo1)
	 trigger(trig2)
	 d2=pulsein(echo2)
	 trigger(trig3)
	 d3=pulsein(echo3)
	 trigger(trig4)
	 d4=pulsein(echo4)
 	 #print("got d2")
	 print d1,d2,d3,d4
 	 #print d4
 	 if(d1<5 or d2<5):
    		brutestop(d1,d2)
    #print("back")
 	 
     	 elif(d1<20):
        
        		right()
        
 	 elif(d2<20):
         
     		left()
 	 elif(d3<20 or d4<20):
		print "front alt"
             
 	 elif(d1>20 and d2>20 ):
     		front()
# time.sleep(0.001)

except KeyboardInterrupt:
	GPIO.cleanup()
     
             
     
  
    
 

 
   
 
   
 

 
   
 
