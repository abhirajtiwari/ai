import time
import cv2 
import socket
# import rover_core

# UDP_IP = "192.168.43.61"
UDP_IP = '127.0.0.1'
UDP_PORT = 5005

cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#############TEMPORARY TCP ################
comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_IP = UDP_IP
TCP_PORT = 12345
comm_sock.connect((TCP_IP, TCP_PORT))
##########################################


ignore_commands = False
t1 = time.time()
while(True):
    t2 = time.time()
    time_elapsed = t2-t1
    ret, frame = cap.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    result, encimg = cv2.imencode('.jpg', frame, encode_param)
    d = encimg.flatten().tostring()
    sock.sendto(d,(UDP_IP, UDP_PORT))
    command = comm_sock.recv(1)
    if ignore_commands == True and time_elapsed < 5:
        if command == 'd':
            print 'ball detected'
            break
        print 'stopped'
        continue
    else:
        ignore_commands = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if command == 'r':
        print command
        # rover_core.right0(128)
    if command == 's':
        t1 = time.time()
        ignore_commands = True

cap.release()
cv2.destroyAllWindows()
