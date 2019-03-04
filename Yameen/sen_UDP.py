import numpy as np
import cv2
import socket

UDP_IP = "10.57.0.78"
UDP_PORT = 5005

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)


    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    d = frame.flatten ()
    print(len(d))
    s = d.tostring ()
    #print(s[46080:(2)*46080])


    for i in xrange(20):
    	#print(s[i*46080:(i+1)*46080])
        sock.sendto (s[i*46080:(i+1)*46080],(UDP_IP, UDP_PORT))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
