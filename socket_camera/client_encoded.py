import cv2 as cv
import numpy as np
import socket

# socket.setdefaulttimeout(0.033)

port = 1234
# server = '127.0.0.1'
# server = '10.57.0.62'
server = '192.168.43.254'

# factor = 4
# l = int(640/factor)
# b = int(480/factor)
# ch = 3
# size = l*b*ch

def getCameraFrame():
    try:
        global port
        data = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try: 
                sock.connect((server, port))
                break
            except socket.error:
                port+=1
        size = int(sock.recv(7))
        while len(data) < size:
            data += sock.recv(int(1e7))
            # print len(data)
        sock.sendall('d')
        # data = sock.makefile().readline()
        frame_encoded = np.fromstring(data, dtype='uint8')
        frame_encoded =  np.reshape(frame_encoded, (len(frame_encoded), 1))
        # frame = np.hstack((frame, np.zeros(921600-len(frame)))) 
        # print frame
        frame = cv.imdecode(frame_encoded, -1)
        # if frame.shape[0] != size:
        #     print 'a'
        #     sock.close()
        #     return
        # frame = np.reshape(frame, (b, l, ch), 'F')
        # frame = cv.resize(frame, (int(l*factor), int(b*factor)), interpolation=cv.INTER_LINEAR)
        # return frame
        # cv.imshow('frame', frame)
        # key = cv.waitKey(1)
        # if key == ord('q'):
        #     break
        sock.close()
        return frame
    except socket.timeout:
        pass


if __name__ == '__main__':
    while True:
        # try:
        #     data = ''
        #     sock = socket.socket()
        #     sock.connect((server, port))
        #     while len(data) < size:
        #         data += sock.recv(int(1e7))
        #     print len(data)
        #     # data = sock.makefile().readline()
        #     frame = np.fromstring(data, dtype='uint8')
        #     # frame = np.hstack((frame, np.zeros(921600-len(frame)))) 
        #     # print frame
        #     if frame.shape[0] != size:
        #         print 'a'
        #         sock.close()
        #         continue
        #     frame = np.reshape(frame, (b, l, ch), 'F')
        #     frame = cv.resize(frame, (int(l*factor), int(b*factor)), interpolation=cv.INTER_LINEAR)
        #     cv.imshow('frame', frame)
        #     key = cv.waitKey(1)
        #     if key == ord('q'):
        #         break
        #     sock.close()
        # except socket.timeout:
        #     pass

        factor = 1.5
        frame = getCameraFrame()
        frame = cv.resize(frame, (int(640/factor), int(480/factor)))
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break


