import numpy as np
import cv2
import socket
import time
import RPi.GPIO as GPIO
import serial

ser = serial.Serial('/dev/serial0',38400)

def state(ch):
	ser.write(ch)


#put IP of rec
UDP_IP = "192.168.43.61"
UDP_PORT = 10000

cap = cv2.VideoCapture(0)
#********UDP********
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ack='n'


while(True):
	try:
		#right
		state(chr(6))
		
		s=socket.socket()			#TCP
		s.connect(('',TCP_PORT))	#TCP

		ret, frame = cap.read()
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
		result, encimg = cv2.imencode('.jpg', frame, encode_param)
		d = encimg.flatten().tostring()
		sock.sendto(d,(UDP_IP, UDP_PORT))
		ack=s.recv(9)
		
		if ack=='stop code':
			s.close()
			sock.close()
			GPIO.cleanup()
			quit()

	except KeyboardInterrupt:
		GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()