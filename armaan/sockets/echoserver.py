import socket                
import cv2  
import sys
socket.setdefaulttimeout(0.0333)
# next create a socket object 
s = socket.socket()          
print "Socket successfully created"
cap=cv2.VideoCapture(0)  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345          

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print "socket binded to %s" %(port) 
  
# put the socket into listening mode 
s.listen(5)      
print "socket is listening"            
  
# a forever loop until we interrupt it or  
# an error occurs

																																																																																																																																																																																											

while True:
	try: 
	 
		   a,frame=cap.read()
		   if frame is not None:
			
		   	cv2.imshow('frame',frame) 
   # Establish connection with client. 
		   	key=cv2.waitKey(1)
			if key==ord('q'):
				break
			print "frame",frame
			print "flat",  
		   	c, addr = s.accept()
			
			send=frame.flatten().tostring()      
		   	print 'Got connection from', addr 
		   	print 'stop'	
		   # send a thank you message to the client.  
		   	c.sendall(send) 
	  
   # Close the connection with the client 
	except socket.timeout:
		pass
		   
	except KeyboardInterrupt:
		cv2.destroyAllWindows()
		c.close() 
		s.close()
		sys.exit()
	except: 
		s.close()
			
s.close()
