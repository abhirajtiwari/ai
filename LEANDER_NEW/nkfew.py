import cv
import numpy as np
import serial
import base64
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)



cap = cv.VideoCapture(0)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5, 5))
kernel1= cv.getStructuringElement(cv.MORPH_ELLIPSE,(3, 3))





while(1):

    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv=cv.GaussianBlur(hsv,(5,5),0)

      # define range of yellow color in HSV
    lower_yellow = np.array([29,86,6])
    upper_yellow = np.array([64,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel1)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel1)


    mask = cv.erode(mask,kernel,iterations=2)
    mask = cv.dilate(mask,kernel1, iterations=13)

       # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame,  mask = mask)

# BOUNDING RECTANGLE .............................................................................................

    _, conts, hei = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE )
    conts = np.array(conts)

    if len(conts) > 0:

        for i, contour in enumerate(conts):
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            aratio = (rect[1][0] / rect[1][1])
            if (aratio > 0.9) and (aratio < 1.1):
                cv.drawContours(frame, [box], 0, (0, 0, 255), 2)



            print("Aspect Ratio",aratio)



#HOUGH CIRCLES........................................................................................................



    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)

    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 200, param1=255, param2=20, minRadius=0, maxRadius=0)
    #     # print circles

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle

            if (aratio > 0.9) and (aratio < 1.1):
                cv.circle(res, (x, y), r, (0, 255, 0), 4)
                roi=cv.rectangle(res, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 0)
                #cv2.putText(frame,"BALL DETECTED",(x,y),cv2.FONT_HERSHEY_SIMPLEX,2,255)
                image = roi
                image_read = image.read()
                image_64_encode = base64.encodestring(image_read)
                print(image_64_encode)
                ser.write(image_64_encode)
                print(len(image_64_encode))
                time.time(1)
                quit()

    #DISPLAY................................................................................................................



    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    cv.imshow('roi',roi)

#.....................................................................................................................
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
