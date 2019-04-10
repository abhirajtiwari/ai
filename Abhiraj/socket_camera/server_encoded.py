import cv2 as cv
import time
import numpy as np
import socket

cap = cv.VideoCapture(0)
# fps = int(cap.get(cv.CAP_PROP_FPS))

#socket.setdefaulttimeout(0.100)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setblocking(0)

host = socket.gethostname()

port = 1234
factor = 2

while True:
    try:
        sock.bind(('', port))
        print 'Port at ', port
        break
    except socket.error:
        port += 1

sock.listen(5)

#c, addr = sock.accept()

while True:
    _, frame = cap.read()
    b, l, ch = frame.shape 
    frame = cv.resize(frame, (int(l/factor), int(b/factor)))
    _, encoded = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 30])
    length = len(encoded)
    string_encoded = encoded.tostring()
    if frame is not None:
        try:
            # data =frame.flatten('F').tostring()
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
            # c.sendall(data)
            c.sendall(format(length, '07')+string_encoded)
            rec = c.recv(1)
            while rec != 'd':
                continue
            # time.sleep(1./fps)
            c.close()
            print 'wrote', length

        except socket.error:
            pass
        except KeyboardInterrupt:
            break
# c.close()
sock.close()
print 'Socket Closed' 
