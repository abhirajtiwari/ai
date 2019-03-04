import socket
import cv2
import numpy as np
port=12344
try:
 while True:
	s=socket.socket()
	s.connect(('127.0.0.1',port))
	size=s.recv(7)	
	data=s.recv(10000000)
	while len(data)<int(size):
		data+=s.recv(10000000)
	s.sendall('a')
	
	print len(data)
	data=np.fromstring(data,dtype=np.uint8)
	data=np.transpose(data)
	frame= cv2.imdecode(data, 1)
	cv2.imshow('res',frame)
	key=cv2.waitKey(1)
	if key==ord('q'):
		break
	
	s.close()

except KeyboardInterrupt:
	cv2.destroyAllWindows()
	s.close()
cv2.destroyAllWindows()
