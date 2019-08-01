import numpy as np
import cv2
import cv2.cv as cv	

#import imutils 
def nothing(x):
    pass
cap=cv2.VideoCapture(0)
cv2.namedWindow("para")
cv2.createTrackbar("Hmin","para",0,255,nothing)
cv2.createTrackbar("Smin","para",0,255,nothing)
cv2.createTrackbar("Vmin","para",0,255,nothing)
cv2.createTrackbar("Hmax","para",0,255,nothing)
cv2.createTrackbar("Smax","para",0,255,nothing)
cv2.createTrackbar("Vmax","para",0,255,nothing)

while(1):
    a,frame=cap.read()
    """img_yuv=cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
    clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0]=clahe.apply(img_yuv[:,:,0])
    frame=cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)
    """

    rows,cols,chan=frame.shape
    black=np.zeros((rows,cols),np.uint8)
    hmin=cv2.getTrackbarPos("Hmin","para")
    smin=cv2.getTrackbarPos("Smin","para")
    vmin=cv2.getTrackbarPos("Vmin","para")
    hmax=cv2.getTrackbarPos("Hmax","para")
    smax=cv2.getTrackbarPos("Smax","para")
    vmax=cv2.getTrackbarPos("Vmax","para")
    hmin=29
    smin=86
    vmin=6
    hmax=64
    smax=255
    vmax=255
    kernel=np.ones((5,5),np.uint8)
    kernel1=np.ones((3,3),np.uint8)
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
    
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    update=[] 
    if len(contours)!=0:
       for i in contours:
           x,y,w,h = cv2.boundingRect(i)
           ratio=float(w)/h
	   print ratio
           if ratio>=0.9 and ratio<1.2:
            update.append(i)  
            
               
    roi=frame       
    if len(update)!=0:        
     c= max(update, key = cv2.contourArea)
     x,y,w,h = cv2.boundingRect(c)
     xmin=int(x/2)
     ymin=int(y/2)
     xrange=int((x+w)*1.5)
     yrange=int((y+h)*1.5)
     
     roi=mask[y:y+w,x:x+h]
     #cv2.imshow('roi',roi)
     if len(roi)!=0:
      #roi_hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
      #roi_thresh=cv2.inRange(roi_hsv,lball,hball)
      #black[x:x+w+5,y:y+h+5]=roi_thresh
      #fr=cv2.bitwise_and(frame,frame,mask=roi)
      #fr=cv2.cvtColor(frame,cv2.COLOR_BGR2BLACK)
      if (h>w): 
        m=h
      else :
          m=w

      #print(roi)  
      #roi_gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
      circles=cv2.HoughCircles(roi,cv.CV_HOUGH_GRADIENT,1,200,param1=128,param2=10,minRadius=int(w/3),maxRadius=int(w/2))
 
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      if circles is not None:
          print("ball")   
          circles=np.round(circles[0,:]).astype("int")
	  prev=0
          for(xc,yc,rc) in circles:
		curr=rc
		if curr>prev:
			maxval=curr
			xop=xc
			yop=yc
		prev=curr
		 
	   	    
          cv2.circle(frame,(xop+x,yop+y),maxval,(0,255,0),4)
          cv2.circle(frame,(xop+x,yop+y),2,(255,0,0),2)
      else:
          print("no ball")
    
    	 

    cv2.imshow('frame',frame)
    cv2.imshow('para',frame)
    cv2.imshow('res',ma)

    k=cv2.waitKey(2) & 0xFF
    if k==27:
        break
cv2.destroyAllWindows()    
