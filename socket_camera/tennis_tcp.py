import cv2
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time
import client_encoded

# cap = cv2.VideoCapture(0)
count = 19 #photo count for testing
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
    # _, frame = cap.read()
    frame = client_encoded.getCameraFrame() ###get frame from tcp
    # time.sleep(3)
    # count += 1
    # frame = cv2.imread('/home/abhiraj/Mars Rover Manipal/dataset/day2/ball/{}.jpg'.format(count))
    frame = cv2.GaussianBlur(frame, (5,5), 0)

    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([29, 60, 70])
    upper_green = np.array([64, 255, 255])
    
    mask = cv2.inRange(frame_HSV, lower_green, upper_green)
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)))
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations=13)

    _, conts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.array(conts)
    if len(conts) > 0:
        for i, contour in enumerate(conts):
            (x,y), rad = cv2.minEnclosingCircle(contour)
            frame = cv2.circle(frame, (int(x), int(y)), 0, (0,0,255), 4)
            x1, y1, w, h = cv2.boundingRect(contour)
            moments = cv2.moments(contour)
            cx = int(moments['m10']/moments['m00'])
            cy = int(moments['m01']/moments['m00'])
            p = (w/100 + h/100)/2
            x1 = int(x1 - p)
            y1 = int(y1 - p)
            x2 = int(x1+w+p)
            y2 = int(y1+h+p)
            x1 = 0 if x1<0 else x1
            y1 = 0 if y1<0 else y1
            # frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            r = frame[y1:y2, x1:x2] #r is roi
            # cv2.imshow('sample', cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)//64 * 64)
            # np.savetxt('r.txt', cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)//64 * 64, delimiter=', ', newline=', ', header='{}, {}, '.format(r.shape[0], r.shape[1]),fmt='%d') 
            r = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
            r = cv2.GaussianBlur(r, (5, 5), 0)
            hist = cv2.calcHist(r, [0], None, [256], [0,256]) 
            if np.mean(hist[200:,0]) > np.mean(hist[:199,0]):
                r = cv2.bitwise_not(r)
                print 'inv'
            print 'not'
            r = cv2.equalizeHist(r) 
            # r = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0) ##ADDED NOW
            # r = cv2.Canny(r, 18, 200)
            # cv2.imshow('fin', r)
            # plt.plot(hist)
            # plt.pause(0.5)
            # cv2.imshow('r', r)
            circles = cv2.HoughCircles(r , cv2.HOUGH_GRADIENT, 1, int(w), param1=128, param2=15, minRadius=int(w/6), maxRadius=int(w/2)) 
            if circles is not None:
                for circle in circles:
                    if ((cx-int(x1+circle[0][0]))**2 + (cy-int(y1+circle[0][1]))**2 - circle[0][2]) > 0:
                        continue
                    frame = cv2.circle(frame, (int(x1+circle[0][0]), int(y1+circle[0][1])), circle[0][2], (255,0,0), 3) 
    cv2.imshow('mask', mask)
    cv2.imshow('result',frame)

cv2.destroyAllWindows()
