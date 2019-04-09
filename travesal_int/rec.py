import socket
import cv2
import numpy as np
UDP_IP = ''
UDP_PORT = 5005
port=12344
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))
s.bind(('',port))
s.listen(5)
while True:
	data, addr = sock.recvfrom(10000000)
	conn,addr=s.accept()
	
	frame = np.fromstring (data,dtype=np.uint8)
	#print('frame shape',frame.shape)
	#print('frame is',len(frame))
	frame = np.transpose(frame)
	frame = cv2.imdecode(frame, 1)
	print frame.shape
	conn.sendall('a')
	cv2.imshow('frame',frame)
	k=cv2.waitKey(1) & 0xFF
	if k==ord('q'):
		break
cv2.destroyAllWindows()

