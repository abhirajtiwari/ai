import cv2 as cv
# import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import threading

#GLOBAL VARIABLES
framel = []
framer = []
retl = False
retr = False
end = False

def capl():
    cap = cv.VideoCapture(2)
    global framel
    global retl
    while True:
        retl, framel = cap.read()
        if end==True:
            break

def capr():
    cap = cv.VideoCapture(1)
    global framer
    global retr
    while True:
        retr, framer = cap.read()
        if end==True:
            break

def main():
    global retr, retl
    while retr == False or retl == False:
        pass
    while True:
        # print framel, framer
        cv.imshow('l', framel)
        cv.imshow('r', framer)
        stereo = cv.StereoBM_create(numDisparities=16, blockSize=5)
        disparity = stereo.compute(cv.cvtColor(framel, cv.COLOR_BGR2GRAY), cv.cvtColor(framer, cv.COLOR_BGR2GRAY))
        disparity = cv.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
        cv.imshow('d', disparity)
        key = cv.waitKey(1)
        if key == ord('q'):
            global end 
            end = True
            break

# def killer():
#     global end
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         end = True
#         return

tcl = threading.Thread(target=capl, args=())
tcr = threading.Thread(target=capr, args=())
tm = threading.Thread(target=main, args=())
# tk = threading.Thread(target=killer, args=())
# tk.start()
tcl.start()
tcr.start()
tm.start()
tcl.join()
tcr.join()
tm.join()
# tk.join()
