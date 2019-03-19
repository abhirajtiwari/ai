import socket
import numpy
import time
import cv2

# UDP_IP = "192.168.43.130"
UDP_IP = '127.0.0.1'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))

def getCameraFrame():
    data, addr = sock.recvfrom(10000000)
    print('inside')
    frame = numpy.fromstring (data,dtype=numpy.uint8)
    #print('frame shape',frame.shape)
    #print('frame is',len(frame))
    frame = numpy.transpose(frame)
    frame = cv2.imdecode(frame, 1)
    return frame

if __name__ == '__main__':
    while True:
        cv2.imshow('frame', getCameraFrame())
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
