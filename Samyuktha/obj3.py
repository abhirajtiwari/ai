import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

cap = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)
while (1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of yellow color in HSV
    lower_yellow = np.array([29, 86, 6])
    upper_yellow = np.array([64, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # ....................................................................................................................

    res = cv2.GaussianBlur(res, (5, 5), 0)
    #  kernel = np.ones((5, 5), np.uint8)
    #  erosion = cv2.erode(res, kernel, iterations=1)
    gimg = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    gimg = cv2.erode(gimg, kernel, iterations=1)
    gimg = cv2.dilate(gimg, kernel, iterations=1)

    cnts = cv2.findContours(gimg, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print(cX)
        print(cY)
    # cimg = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(gimg, cv2.HOUGH_GRADIENT, 1, 200,
                               param1=255, param2=10, minRadius=0, maxRadius=0)
    if circles is not None:
        circles = np.round(circles[0, :]).astype('int')

        for (x, y, r) in circles:
            if  abs(cX - x) < 5 and abs(cY - y) < 5:
                cv2.circle(res, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(res, (x - (r + 20), y + (r + 20)), (x + r + 20, y - r - 20), (0, 128, 255), 3)
    '''if circles is not None:
        x1 = circles[0]
        y1 = circles[1]'''

    '''circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(res, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(res, (i[0], i[1]), 2, (0, 0, 255), 3)'''

    cv2.imshow('detected circles', res)
    cv2.imshow('gray image', gimg)
    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)
    # cv2.imshow('adjusted',adjusted)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
