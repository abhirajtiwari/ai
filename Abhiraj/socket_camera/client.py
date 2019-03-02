import cv2 as cv
import numpy as np
import socket

# socket.setdefaulttimeout(0.033)

port = 1234
# server = '10.42.0.15'
server = '127.0.0.1'

while True:
    try:
        sock = socket.socket()
        sock.connect((server, port))
        data1 = sock.recv(int(1e7))
        data2 = sock.recv(int(1e7))
        data3 = sock.recv(int(1e7))
        data = data1+data2+data3
        # print len(data)
        # data = sock.makefile().readline()
        frame = np.fromstring(data, dtype='uint8')
        # frame = np.hstack((frame, np.zeros(921600-len(frame)))) 
        # print frame
        if frame.shape[0] != 480*640*3:
            print 'a'
            sock.close()
            continue
        frame = np.reshape(frame, (480, 640, 3), 'F')
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        sock.close()
    except socket.timeout:
        pass

