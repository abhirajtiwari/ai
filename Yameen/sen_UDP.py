import time

UDP_IP = "192.168.43.61"
UDP_PORT = 5005

cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while(True):
	ret, frame = cap.read()
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
	result, encimg = cv2.imencode('.jpg', frame, encode_param)
	d = encimg.flatten().tostring()
	sock.sendto(d,(UDP_IP, UDP_PORT))
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
