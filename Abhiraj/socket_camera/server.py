import cv2 as cv
import time
import numpy as np
import socket

cap = cv.VideoCapture(0)
# fps = int(cap.get(cv.CAP_PROP_FPS))
fps = 30

#socket.setdefaulttimeout(0.100)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setblocking(0)

host = socket.gethostname()

port = 1234
factor = 2

sock.bind(('', port))

sock.listen(5)

#c, addr = sock.accept()

while True:
    _, frame = cap.read()
    b, l, ch = frame.shape 
    frame = cv.resize(frame, (int(l/factor), int(b/factor)))
    if frame is not None:
        try:
            data =frame.flatten('F').tostring()
            # data = np.fromstring(data, dtype='uint8')
            # data = np.reshape(data, (480, 640, 3))
            # cv.imshow('frame', frame)
            # key = cv.waitKey(1)
            # if key == ord('q'):
            #     break
	    # print "here also"
            c, addr = sock.accept()
	    # print "here"
            # c.send(str(len(data)))
            c.sendall(data)
	    rec = c.recv(1)
	    while rec != 'd':
		continue
            # time.sleep(1./fps)
            # c.close()
            print 'wrote'

        except socket.error:
            pass
        except KeyboardInterrupt:
            break
c.close()
sock.close()
print 'Socket Closed' 
