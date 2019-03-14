import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
trig1=17
echo1=27
GPIO.setup(trig1,GPIO.OUT)
GPIO.setup(echo1,GPIO.IN)
def trigger(trig):
     GPIO.output(trig,GPIO.LOW)
     time.sleep(0.01)
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
	while True:
		trigger(trig1)
		d1=pulsein(echo1)
except KeyboardInterrupt:
	GPIO.cleanup()
