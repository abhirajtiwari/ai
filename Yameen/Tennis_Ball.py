import cv2
import numpy as np

cap = cv2.VideoCapture(0)
kernel = np.ones((3,3),np.float32)

def nothing(x):
    pass

cv2.namedWindow('HSV')

# create trackbars for color change
cv2.createTrackbar('H_min','HSV',0,255,nothing)
cv2.createTrackbar('S_min','HSV',0,255,nothing)
cv2.createTrackbar('V_min','HSV',0,255,nothing)
cv2.createTrackbar('H_max','HSV',0,255,nothing)
cv2.createTrackbar('S_max','HSV',0,255,nothing)
cv2.createTrackbar('V_max','HSV',0,255,nothing)

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

while True:
    _, frame = cap.read()
    #blurred_frame = cv2.GaussianBlur(frame, (3, 1), 0)
    gamma = 1.4
    frame = adjust_gamma(frame, gamma=gamma)

    H_min = cv2.getTrackbarPos('H_min','HSV')
    S_min = cv2.getTrackbarPos('S_min','HSV')
    V_min = cv2.getTrackbarPos('V_min','HSV')
    H_max = cv2.getTrackbarPos('H_max','HSV')
    S_max = cv2.getTrackbarPos('S_max','HSV')
    V_max = cv2.getTrackbarPos('V_max','HSV')

    bfilter = cv2.bilateralFilter(frame, 5, 90, 90)
    hsv = cv2.cvtColor(bfilter, cv2.COLOR_BGR2HSV)

    lower_green = np.array([20, 89, 6])
    upper_green = np.array([64, 255, 255])

#    lower_green = np.array([H_min,S_min,V_min])
#    upper_green = np.array([H_max,S_max,V_max])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    dilation = cv2.dilate(mask, kernel, iterations=2)
    dilation = cv2.erode(dilation, kernel, iterations=5)        #this is erosion

    cv2.imshow('dila',dilation)
#COUNTERS
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #contours2, _ = cv2.findContours(contours1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    update=[]
    if len(contours) != 0:
        for counter in contours:
# ***********for selecting the maximum area************
            #print('cont',contours)
            #cv2.imshow('contours',contours)
            update.append(counter)
            #print('up',update)
            c = max(update, key=cv2.contourArea)
            #print('c',c)
# *******************************************************

            #***********for rotated rectangle*******************
            rect = cv2.minAreaRect(counter)
            x_rec, y_rec, w_rec, h_rec = cv2.boundingRect(counter)
            (x,y),radius = cv2.minEnclosingCircle(counter)
            center = (int(x),int(y))
            radius = int(radius)
            #print('ra',radius)
            #print('rect',rect)
            #print('as',rect[1][0])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            #print('b',box)
            x1 = box[0, 0]
            y1 = box[0, 1]
            x2 = box[1, 0]
            y2 = box[1, 1]
            x3 = box[2, 0]
            y3 = box[2, 1]
            x4 = box[3, 0]
            y4 = box[3, 1]
            area_circle = np.pi*(radius+3)*(radius+3)
            if rect[1][0]>20:
                if abs(rect[1][0] - rect[1][1])<15:
                    print('center is',center)
                    #cv2.rectangle(frame,(x_rec,y_rec),(x_rec+w_rec,y_rec+h_rec),(0,255,0),2)
                    cv2.circle(frame,center,radius+6,(0,0,0),1)
                    #print('radius',radius+3)
                    #cv2.drawContours(frame, [box], -1, (255, 0, 0), 1)
                    #print('diff',abs(rect[1][0] - rect[1][1]))
                    #print('x y',x_rec,y_rec,w_rec,h_rec)
                    y_min = int(y-(radius+6))
                    x_min = int(x-(radius+6))
                    y_max = int(y+(radius+6))
                    x_max = int(x+(radius+6))
                    if int(y-(radius+6)<0):
                        y_min= 0
                    if int(y+(radius+6)<0):
                        y_max = 0
                    if int(x-(radius+6)<0):
                        x_min = 0
                    if int(x+(radius+6)<0):
                        x_max = 0
                    roi = frame[y_min:y_max,x_min:x_max]
                    if len(roi) is not 0:
                        cv2.imshow('roi',roi)
                    roi = []
                    #im = cv2.drawContours(im,[box],0,(0,0,255),2)

#*************************************************************************************************
    #frame1[:] = [H_max - H_min,S_max - S_min,V_max - V_min]
    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
