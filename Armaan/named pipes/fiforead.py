import time 
fname="/tmp/piper"

try:
        count=0	
	f=open(fname,'r')
	while True:
		#time.sleep(1)
		
	        
		data=f.read(4)
		
		print data 
		count+=1
except KeyboardInterrupt:
	f.close()
	print "lol"
