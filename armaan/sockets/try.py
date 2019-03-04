import socket
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
port=12344
s.bind(('',port))
s.listen(5)
ack='n'
try:
 while True:
	a,frame=cap.read()
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
	result, encimg = cv2.imencode('.jpg', frame, encode_param)
	data=encimg.flatten().tostring()
	length=len(data)
	sn=str(length).zfill(7)	
	print int(sn)
		
	c,addr=s.accept()
	c.sendall(sn)
	c.sendall(data)	
		
	key=cv2.waitKey(1)
	if key==ord('q'):
		break
	while ack!='a':
		ack=c.recv(1)
	c.close()
except KeyboardInterrupt:
	s.close()
s.close()
