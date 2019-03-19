import numpy as np
import cv2
import cv2.cv as cv	

#import imutils 
def nothing(x):
    pass
def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)
def corrected(x,y,w,h):
	roi_frame=frame[y:y+w,x:x+h]
	roi_lab=cv2.cvtColor(roi_frame,cv2.COLOR_BGR2LAB)
    	roi_gamma=adjust_gamma(roi_frame,0.3) #gamma corrected
    	roi_lab_g=cv2.cvtColor(roi_gamma,cv2.COLOR_BGR2LAB) #lab colorspace
    	hist_g=cv2.calcHist([roi_lab_g],[0],None,[256],[0,256])
	pos,b=np.where(hist_g==np.amax(hist_g))
	val=1.0000
	arr=np.zeros(256,dtype=np.uint8)
	"""while pos[0]<108 or pos[0]>148:
		if pos[0]>128:
			val-=0.05
		else:
			val+=0.05
		#print val
		roi_gamma=adjust_gamma(roi_frame,val)
		roi_lab_g=cv2.cvtColor(roi_gamma,cv2.COLOR_BGR2LAB)	 
		hist_g=cv2.calcHist([roi_lab_g],[0],None,[256],[0,256])
		pos,b=np.where(hist_g==np.amax(hist_g))
		arr[pos[0]]+=1
		if arr[pos[0]]>7:
			break"""
	print "POSITION",pos
	roi_hsv=cv2.cvtColor(roi_gamma,cv2.COLOR_BGR2HSV)
	mask_roi=cv2.inRange(roi_hsv,lball,hball)

    	mask_roi = cv2.erode(mask_roi, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)),iterations=1)
    	mask_roi = cv2.dilate(mask_roi, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations=13)	
	return mask_roi



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
    """kernel=np.ones((5,5),np.uint8)
    kernel1=np.ones((3,3),np.uint8)"""

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
           x,y,w,h = cv2.boundingRect(i)
           ratio=float(w)/h
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

	     cv2.imshow('maskasas',roi_left)
	     roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
	     #cv2.imshow('roi',roi)
	     if len(roi)!=0:
	      if (h>w): 
		m=h
	      else :
		  m=w

	      #print(roi)  
	      #roi_gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
	      circles=cv2.HoughCircles(roi,cv.CV_HOUGH_GRADIENT,1,200,param1=200,param2=15,minRadius=int(w/3),maxRadius=int(w/2))
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

	 	  if abs(cx-(x+xop))>20 or abs(cx-(x+xop))>20:
			continue
		  print("ball")
		  cv2.circle(frame,(xop+x,yop+y),maxval,(0,255,0),4)
		  cv2.circle(frame,(xop+x,yop+y),2,(255,0,0),2)
	      else:
		  print("no ball")



    cv2.imshow('frame',frame)
    cv2.imshow('para',frame)
    cv2.imshow('res',mask)

    k=cv2.waitKey(2) & 0xFF
    if k==27:
        break
cv2.destroyAllWindows()
