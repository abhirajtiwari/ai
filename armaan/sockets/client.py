import socket                
import cv2  
import numpy as np
# Create a socket object 

# Define the port on which you want to connect 
port = 12344          
  
# connect to the server on local computer 
 
  
# receive data from the server
try:
	while True:
	 
		s = socket.socket()          
		s.connect(('127.0.0.1', port))  
		data=s.recv(10000000)
		while len(data)<640*480*3:
			data+=s.recv(10000000)
		s.sendall('a')	
		print len(data)
		if len(data)==640*480*3:		
		 data=np.fromstring(data,dtype=np.uint8)
		 frame=np.reshape(data,(480,640,3))
		 cv2.imshow('res',frame)
				
		key=cv2.waitKey(1)		
		if key==ord('q'):
			break
		s.close()  		
	
		
except KeyboardInterrupt:
	cv2.destroyAllWindows()
	
# close the connection 
       
