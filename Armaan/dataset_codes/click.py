import numpy as np
import cv2

path1="/home/armaan/Desktop/mrm/logi_dataset/logi_noball/"
cap = cv2.VideoCapture(1)
i=89
while(True):
    # Capture frame-by-frame
    	
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
   	
    smask=str(i)+".jpg"
    k=cv2.waitKey(1) & 0xFF	
    if k==32:
	#re=cv2.resize(frame,(640,480))
	cv2.imwrite(path1+smask,frame)
	i=i+1
    if k==27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
