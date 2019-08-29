import cv2 as cv
import numpy as np
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
arr = []

data1 = ord(ser.read()) 
data2 = ord(ser.read())
count = 0
print data1, data2
while count < data1*data2:
    data = ser.read()
    arr.append(ord(data))
    count += 1
arr = np.array(arr, dtype=np.uint8)
arr = np.reshape(arr, (data1, data2))
cv.imshow('recieved', arr)
cv.waitKey(0)
cv.destroyAllWindows()
