import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #STREAM is TCP, for UDP use DGRAM
sock.bind(('0.0.0.0',10000))                                #0.0.0.0 [every device on the same network with server will be connected to it]
sock.listen(1)
connections = []
while True:
	c, a = sock.accept()
	connections.append(c)
	print(connections)	
