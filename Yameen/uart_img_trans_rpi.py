#this program does not account for data loss during transferring
import cv2
import serial
import numpy as np
import time
im = cv2.imread(r'/home/pi/result.png',0)
#print type(im)
#print(im)
#a = np.array(im)
#a = a.flatten()
#print(a[90],a[91],a[96],a[97])
#a = [37, 42, 165, 167, 165, 162, 161, 162, 163, 164, 166, 169, 170, 167, 165, 165, 166, 167, 167, 167, 166, 162, 160, 162, 168, 172, 173, 173, 171, 171, 174, 177, 177, 1$
a = [43,25,32,122,41,122,121,124,14,9,56,54,23,12,41,1,43,114,116,65,5,53,26,214]
ser = serial.Serial('/dev/serial0', 9600)
#while i<100:
 #   print(a[i])
#print(a.shape)
#if a[0][0]/10 <100:
 #   ser.write('0')
  #  ser.write(str(a[0]))
#print(a[20])
#i = 0
for i in a:
    #print(i)
    if i<10:
        ser.write(("00"+str(i)).encode())
        #print(i)
        #ser.write(str(b))
    elif i<100:
        ser.write(('0'+str(i)).encode())
        #print(i)
        #ser.write(str(b))
    else:
        ser.write(str(i).encode())
        #print(i)
        #ser.write(str(b))
    #i += 1
    #time.sleep(0.1)
    #ser.write(str(i))
    #i += 1
    #time.sleep(0.1)
