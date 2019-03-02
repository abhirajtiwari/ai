import cv2 as cv
import time
import numpy as np
import socket

cap = cv.VideoCapture(0)
fps = int(cap.get(cv.CAP_PROP_FPS))

socket.setdefaulttimeout(0.100)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setblocking(0)

host = socket.gethostname()

port = 1234

sock.bind(('', port))

sock.listen(5)


while True:
    _, frame = cap.read()
    if frame is not None:
        try:
            frame[frame==255] = 254
            frame[0,0,0] = 255
            # print frame.flatten()
            data =frame.flatten('F').tostring()
            # data = np.fromstring(data, dtype='uint8')
            # data = np.reshape(data, (480, 640, 3))
            # cv.imshow('frame', frame)
            # key = cv.waitKey(1)
            # if key == ord('q'):
            #     break
            c, addr = sock.accept()
            # c.send(str(len(data)))
            c.sendall(data)
            time.sleep(1./fps)
            c.close()
            print 'wrote'

        except socket.error:
            pass
        except KeyboardInterrupt:
            break
sock.close()
print 'Socket Closed'
