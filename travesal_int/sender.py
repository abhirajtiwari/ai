import socket
import cv2
import numpy as np
UDP_IP = ''
UDP_PORT = 5005
port=12344
cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
		ret, frame = cap.read()
		s=socket.socket()
		s.connect(('',port))
		var=s.recv(1)	
		#print recer
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
		result, encimg = cv2.imencode('.jpg', frame, encode_param)
		d = encimg.flatten().tostring()		
		sock.sendto(d,(UDP_IP, UDP_PORT))
		
		print var
cv2.destroyAllWindows()

