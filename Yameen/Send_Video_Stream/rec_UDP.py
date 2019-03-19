import socket
import numpy
import time
import cv2
#put ip of reciever
UDP_IP = "192.168.43.61"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))


while True:

    data, addr = sock.recvfrom(10000000)
    print('inside')
    frame = numpy.fromstring (data,dtype=numpy.uint8)
    #print('frame shape',frame.shape)
    #print('frame is',len(frame))
    frame = numpy.transpose(frame)
    frame = cv2.imdecode(frame, 1)
    print('frame shape new',frame.shape)
    cv2.imshow('frame1',frame)

    if cv2.waitKey(1) & 0xFF == ord ('q'):
break