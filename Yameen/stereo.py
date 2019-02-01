import cv2
import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt

vid1 = cv2.VideoCapture(0)
vid2 = cv2.VideoCapture(1)

while True:
    _, frame0 = vid1.read()
    frame0_new=cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    _, frame1 = vid2.read()
    frame1_new=cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Frame1", frame0)
    cv2.imshow("Frame2", frame1)

    stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=16, SADWindowSize=15)
    disparity = stereo.compute(frame0_new,frame1_new)
    cv2.imshow("Disparity", disparity)			#for disparity in live video use cv2.imshow

    key = cv2.waitKey(1)
    if key == 27:
        break

vid1.release()
vid2.release()
cv2.destroyAllWindows()
