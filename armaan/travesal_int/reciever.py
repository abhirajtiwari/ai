import socket
import numpy as np
import cv2.cv as cv
import time
import cv2
#server 
#put ip of reciever
UDP_IP = ''
UDP_PORT = 5005
port=12345
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
port=12344
s.bind(('',port))
s.listen(5)
hmin=29
smin=86
vmin=6
hmax=64
smax=255
vmax=255


try:
	while True:
	    conn,addr=s.accept()
	    
	    data, addr = sock.recvfrom(10000000)
	    #print('inside')
	    frame = np.fromstring (data,dtype=np.uint8)
	    #print('frame shape',frame.shape)
	    #print('frame is',len(frame))
	    frame = np.transpose(frame)
	    frame = cv2.imdecode(frame, 1)
	    blur=cv2.GaussianBlur(frame,(5,5),0)
	    
	    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
	    
	    lball=np.array([hmin,smin,vmin])
	    hball=np.array([hmax,smax,vmax])
	    mask1=cv2.inRange(hsv,lball,hball)

	    mask=cv2.inRange(hsv,lball,hball)
	    ma=mask
	    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)),iterations=1)
	    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations=13)	
	   
	    """mask=cv2.erode(mask,kernel,iterations=2)
	    #mask=cv2.dilate(mask,kernel1,iterations=1)
	    
	    mask=cv2.dilate(mask,kernel,iterations=1)
	    mask=cv2.erode(mask,kernel,iterations=1)
	    
	    
	    	mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    	mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel1)
	    	mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    """
	    prev=0
	    curr=0
	    	
	    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	    update=[] 
	    if len(contours)!=0:
	       		for i in contours:
		   		rect = cv2.minAreaRect(i)
			
		   		ratio=float(rect[1][0])/rect[1][1]
		   		#print ratio
		   	if ratio>0.9 and ratio<2:
		   		 update.append(i)  
		    
		       
	    #roi=frame       
	    if len(update)!=0:
			for i in update:        
	     			#c= max(update, key = cv2.contourArea)
		     		x,y,w,h = cv2.boundingRect(i)
		     		moments=cv2.moments(i)
		     		cx = int(moments['m10']/moments['m00'])
		     		cy = int(moments['m01']/moments['m00'])
		     
				xmin=int(x/2)
				ymin=int(y/2)
				xrange1=int((w)*1.2)
			     	yrange=int((h)*1.2)
				     
			     	roi_mask=mask[y:y+yrange,x:x+xrange1]
		     		xr=x-(xrange1/2)
		     		if xr<0:
					xr=0
		     		roi_left=mask[y:y+yrange,xr:x+(xrange1)/2]
		     		roi_right=mask[y:y+yrange,x+(xrange1)/2:x+(xrange1)/2+xrange1]
		     		hist_main = cv2.calcHist([roi_mask],[0],None,[256],[0,256])
		     		hist_left = cv2.calcHist([roi_left],[0],None,[256],[0,256])
		     		hist_right = cv2.calcHist([roi_right],[0],None,[256],[0,256])
		     		#print roi_left
		     		if hist_right[255]>hist_main[255]/1.65 and hist_left[255]>hist_main[255]/1.65:
					continue
		     	 
		     
		     		roi=blur[y:y+yrange,x:x+xrange1]
		     	
		     		#cv2.imshow('maskasas',roi_left)
		     		roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
		     		#cv2.imshow('roi',roi)
		     		if len(roi)!=0:
		      			if (h>w): 
						m=h
		      			else :
			  			m=w

				      #print(roi)  
				      #roi_gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
					circles=cv2.HoughCircles(roi,cv.CV_HOUGH_GRADIENT,1,200,param1=200,param2=13 ,minRadius=int(w/3),maxRadius=int(w/2))
					cv2.rectangle(frame,(x,y),(x+xrange1,y+yrange),(0,255,0),2)  
					cv2.rectangle(frame,(x+(xrange1)/2,y),(x+(xrange1)/2-xrange1,y+yrange),(0,255,0),2)
					cv2.rectangle(frame,(x+(xrange1)/2,y),(x+(xrange1)/2+xrange1,y+yrange),(0,255,0),2)
			     
		      			if circles is not None:
			     
			  			circles=np.round(circles[0,:]).astype("int")
			  			prev=0
			  			for(xc,yc,rc) in circles:
							curr=rc
							if curr>prev:
								maxval=curr
								xop=xc
								yop=yc
							prev=curr
					 
		 	  			if abs(cx-(x+xop))>8 or abs(cx-(x+xop))>8:
							continue
						print "ball"
			  			conn.sendall('b')
						
			
			  			cv2.circle(frame,(xop+x,yop+y),maxval,(0,255,0),4)
			  			cv2.circle(frame,(xop+x,yop+y),2,(255,0,0),2)
		      			else:
			  			print "no ball"
	    
	    	 

	    
	    print('frame shape new',frame.shape)
	    cv2.imshow('frame1',frame)
	    cv2.imshow('mask',mask)
	    if cv2.waitKey(1) & 0xFF == ord ('q'):
			break
	    conn.close()
except:
	conn.close()
	s.close()
	sock.close()
