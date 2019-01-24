import numpy as np
import cv2
import imutils 
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
    rows,cols,chan=frame.shape
    black=np.zeros((rows,cols),np.uint8)
    hmin=cv2.getTrackbarPos("Hmin","para")
    smin=cv2.getTrackbarPos("Smin","para")
    vmin=cv2.getTrackbarPos("Vmin","para")
    hmax=cv2.getTrackbarPos("Hmax","para")
    smax=cv2.getTrackbarPos("Smax","para")
    vmax=cv2.getTrackbarPos("Vmax","para")
    hmin=20
    smin=117
    vmin=38
    hmax=100
    smax=255
    vmax=255
    kernel=np.ones((5,5),np.uint8)
    kernel1=np.ones((3,3),np.uint8)
    blur=cv2.GaussianBlur(frame,(11,11),0)
    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    
    lball=np.array([hmin,smin,vmin])
    hball=np.array([hmax,smax,vmax])
    mask1=cv2.inRange(hsv,lball,hball)
    
    mask=cv2.inRange(hsv,lball,hball)
    """mask=cv2.erode(mask,kernel,iterations=2)
    #mask=cv2.dilate(mask,kernel1,iterations=1)
    """
    mask=cv2.dilate(mask,kernel,iterations=1)
    mask=cv2.erode(mask,kernel,iterations=1)
    
    
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    
    prev=0
    curr=0
    
    r,contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    update=[] 
    if len(contours)!=0:
       for i in contours:
           x,y,w,h = cv2.boundingRect(i)
           ratio=float(w)/h
           if ratio>=1 and ratio<2:
            update.append(i)  
            
               
    roi=frame       
    if len(update)!=0:        
     c= max(update, key = cv2.contourArea)
     x,y,w,h = cv2.boundingRect(c)
     xmin=int(x/2)
     ymin=int(y/2)
     xrange=int((x+w)*1.5)
     yrange=int((y+h)*1.5)
     
     roi=frame[x:x+w,y:y+h]
     #cv2.imshow('roi',roi)
     if len(roi)!=0:
      roi_hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
      #roi_thresh=cv2.inRange(roi_hsv,lball,hball)
      #black[x:x+w+5,y:y+h+5]=roi_thresh
      #fr=cv2.bitwise_and(frame,frame,mask=roi)
      #fr=cv2.cvtColor(frame,cv2.COLOR_BGR2BLACK)
      if (h>w): 
        m=h
      else :
          m=w

      #print(roi)  
      roi_gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
      circles=cv2.HoughCircles(roi_gray,cv2.HOUGH_GRADIENT,1,200,param1=255,param2=13,minRadius=0,maxRadius=m)
 
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      if circles is not None:
          print("ball")   
          circles=np.round(circles[0,:]).astype("int")
          for(xc,yc,rc) in circles:
              cv2.circle(frame,(xc+x,yc+y),rc,(0,255,0),3)
              cv2.circle(frame,(xc+x,yc+y),2,(255,0,0),2)
      else:
          print("no ball")
    
    roi=cv2.inRange(hsv,lball,hball)
    blend=cv2.bitwise_and(frame,frame,mask=roi)

    cv2.imshow('frame',frame)
    cv2.imshow('para',frame)
    cv2.imshow('res',mask)

    k=cv2.waitKey(2) & 0xFF
    if k==27:
        break
cv2.destroyAllWindows()    



