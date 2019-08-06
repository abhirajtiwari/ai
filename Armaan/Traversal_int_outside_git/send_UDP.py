import time
import cv2
import socket
#import RPi.GPIO as GPIO
import serial
#put IP of reciever 

UDP_IP = ''
UDP_PORT = 5005
port=12344
#ser=serial.Serial('/dev/serial0')
#ser.baudrate=38400
cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

ack='c'
def right():
    #GPIO.output(ldir,1)	
    #GPIO.output(rdir,0)
    ser.write(chr(3))
    return
s=socket.socket()
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

except KeyboardInterrupt:
	sock.close()
	s.close()
sock.close()
s.close()	
cap.release()
cv2.destroyAllWindows()

