import time
import cv2
import socket
import RPi.GPIO as GPIO
import system
import serial
GPIO.setmode(GPIO.BCM)
ldir=5
lspeed=13
rdir=23
rspeed=18
GPIO.setup(ldir,GPIO.OUT)
GPIO.setup(lspeed,GPIO.OUT)
GPIO.setup(rdir,GPIO.OUT)
GPIO.setup(rspeed,GPIO.OUT)
UDP_IP = '192.168.43.138'
UDP_PORT = 5005
port=12344
ser=serial.Serial('/dev/serial0')
ser.baudrate=38400
cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
a=GPIO.PWM(lspeed,100)
c=GPIO.PWM(rspeed,100)
a.start(50)
c.start(50)
ack='c'
def right():
    #GPIO.output(ldir,1)	
    #GPIO.output(rdir,0)
    ser.write(chr(6))
    return

try: 
	while(True):

		s=socket.socket()
	        s.connect(('',port))
	   
		right()  
		ret, frame = cap.read()
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
		result, encimg = cv2.imencode('.jpg', frame, encode_param)
		d = encimg.flatten().tostring()		
		sock.sendto(d,(UDP_IP, UDP_PORT))
		ack=s.recv(1)
		if ack=='b':
			print "BALLL"
			s.close()
			sock.close()
			quit()
		

		
		
		s.close()
except:
	
	s.close()
	sock.close()

	
cap.release()
cv2.destroyAllWindows()
