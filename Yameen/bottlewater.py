import cv2
import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
#kernel = np.ones((3,3),np.float32)

def nothing(x):
  pass
cv2.namedWindow('Colorbars')
hh='Max'
hl='Min'
wnd = 'Colorbars'
cv2.createTrackbar("Max", "Colorbars",0,255,nothing)
cv2.createTrackbar("Min", "Colorbars",0,255,nothing)

while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (3, 3), 0)
#    bfilter = cv2.bilateralFilter(frame, 5, 90, 90)
    gray = cv2.cvtColor(blurred_frame, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    hul=cv2.getTrackbarPos("Max", "Colorbars")
    huh=cv2.getTrackbarPos("Min", "Colorbars")



    lower_blue = np.array([29, 60, 20],np.uint8)      #29 60 20
    upper_blue = np.array([64, 255, 255],np.uint8)     #64 255 255
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
    #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations=13)


    mask = cv2.bitwise_and(gray,gray, mask = mask)
    canny = cv2.Canny(mask,200,200)
    sobel_horizontal = cv2.Sobel(mask,cv2.CV_64F,0,1,ksize = 5)
    #mask = cv2.bitwise_and(sobel_horizontal,sobel_horizontal, mask = mask)
    lap = cv2.Laplacian(mask,cv2.CV_64F)

#    mask1 = cv2.bitwise_and(canny,lap, mask = mask)

    thresh0 = cv2.adaptiveThreshold(canny, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
#    dilation = cv2.dilate(mask, kernel, iterations=3)
#    erosion = cv2.erode(dilation, kernel, iterations=1)


    ret,thresh1 = cv2.threshold(canny,hul,huh,cv2.THRESH_BINARY)
    #ret,thresh2 = cv2.threshold(mask,hul,huh,cv2.THRESH_BINARY_INV)
    #ret,thresh3 = cv2.threshold(canny,hul,huh,cv2.THRESH_TRUNC)
    #ret,thresh4 = cv2.threshold(mask,hul,huh,cv2.THRESH_TOZERO)
    #ret,thresh5 = cv2.threshold(canny,hul,huh,cv2.THRESH_TOZERO_INV)
#    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)
    cv2.imshow('sobel', sobel_horizontal)
    #cv2.imshow('canny', canny)
    #cv2.imshow('lap', lap)
    #cv2.imshow('mask1', mask)

    cv2.imshow("thresh1",thresh1)
    #cv2.imshow("thresh2",thresh2)
    #cv2.imshow("thresh3",thresh3)
    #cv2.imshow("thresh4",thresh4)
    #cv2.imshow("thresh5",thresh5)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
