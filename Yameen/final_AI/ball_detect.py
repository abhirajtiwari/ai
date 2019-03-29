import cv2
import numpy as np
from math import sqrt
import time
import socket
import serial

ser = serial.Serial('/dev/serial0',38400)

def state(ch):
	ser.write(ch)
#import RPi.GPIO as GPIO
UDP_IP = "192.168.43.61"
UDP_PORT = 10000
TCP_PORT = 5555

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind ((UDP_IP, UDP_PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_PORT = 5555
s.bind(('',TCP_PORT))

#cap = cv2.VideoCapture(0)			##comment this

kernel = np.ones((3,3),np.float32)

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def ROI(img,y_lrange,y_urange,x_lrange,x_urange):
    RoI = img[y_lrange:y_urange,x_lrange:x_urange]
    return RoI

while True:
	data, addr = sock.recvfrom(10000000)				#comment
	frame = np.fromstring (data,dtype=np.uint8)	#comment
	frame = np.transpose(frame)				#comment	
	frame = cv2.imdecode(frame, 1)				#comment
	s=socket.socket()
	s.connect(('127.0.0.1',TCP_PORT))
	#ret, frame = cap.read()				##comment this
	frame_x, frame_y, _ = frame.shape
	#if frame_x != 0 and frame_y != 0:
	if ret == True:
		gamma = 1
		frame = adjust_gamma(frame, gamma=gamma)
		#frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		bfilter = cv2.bilateralFilter(frame, 5, 90, 90)
		hsv = cv2.cvtColor(bfilter, cv2.COLOR_BGR2HSV)

		lower_green = np.array([20, 64, 6])
		upper_green = np.array([64, 255, 255])

		lower_green1 = np.array([20, 64, 6])
		upper_green1 = np.array([64, 255, 255])

		mask = cv2.inRange(hsv, lower_green, upper_green)

		dilation = cv2.dilate(mask, kernel, iterations=3)
		dilation = cv2.erode(dilation, kernel, iterations=5)
		#mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
		#mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)),iterations=13)

        cv2.imshow('mask',dilation)
    #COUNTERS
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
        update=[]
        if len(contours) != 0:
            for counter in contours:
  
                update.append(counter)
  
                c = max(update, key=cv2.contourArea)
  

                #***********for rotated rectangle*******************
                #minAreaReact returns center(x,y) width height angle of rotation
                rect = cv2.minAreaRect(counter)
                x_rec, y_rec, w_rec, h_rec = cv2.boundingRect(counter)
                (x,y),radius = cv2.minEnclosingCircle(counter)
                center = (int(x),int(y))
                radius = int(radius)
                if rect[1][1] == 0:
                	break
                ratio = float(rect[1][0])/(rect[1][1])
                #print('rect',rect[1][0])

                if ratio<1.1 and ratio>0.9:
                    #print('center is',center)
						                
					y_min = int(y-(radius))
					x_min = int(x-(radius))
					y_max = int(y+(radius))
					x_max = int(x+(radius))
					if int(y-(radius)<0):
						break
					if int(y+(radius)<0):
						break
					if int(x-(radius)<0):
						break
					if int(x+(radius)<0):
						break
					roi = ROI(frame,y_min,y_max,x_min,x_max)    
					#print('x_max',x_max-x_min)
					if len(roi) is not 0:
						gamma1 = 1
						#roi = adjust_gamma(roi,gamma=gamma1)
						y_roi,x_roi,_ = roi.shape
						#print('s',roi.shape)
						#print('y,x',y_roi,x_roi)
						#print('ra',radius)
						side_length = radius*2
						side_length = int(side_length)
						#print('side_le',side_length)
						length = (side_length/sqrt(2) - radius)/sqrt(2)
						length = int(length)
						
						#print('le',length)
						#print('length_roi',len(roi))
						roi_in_circle_tl = roi[y_roi/2 - length: y_roi/2, x_roi/2 - length: x_roi/2]   #inside circle top left roi
						roi_in_circle_tr = roi[y_roi/2 - length: y_roi/2, x_roi/2: x_roi/2 + length]   #inside circle top right roi
						roi_in_circle_bl = roi[y_roi/2: y_roi/2 + length, x_roi/2 - length: x_roi/2]   #inside circle bottom left roi
						roi_in_circle_br = roi[y_roi/2: y_roi/2 + length, x_roi/2: x_roi/2 + length]   #inside circle bottom right roi
						roi_out_circle_tl = roi[0:length,0:length]
						roi_out_circle_tr = roi[0:length,side_length - length:side_length]
						roi_out_circle_bl = roi[side_length - length:side_length,0:length]
						roi_out_circle_br = roi[side_length - length:side_length,side_length - length:side_length]
							

							
						ar1,ar2,_ = roi.shape
						if ar1==0 or ar2==0:
							break

						ar1,ar2,_ = roi_in_circle_tl.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_in_circle_tr.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_in_circle_bl.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_in_circle_br.shape
						if ar1==0 or ar2==0:
							break

						cv2.imshow('roi',roi)
						ar1,ar2,_ = roi_out_circle_tl.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_out_circle_tr.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_out_circle_bl.shape
						if ar1==0 or ar2==0:
							break
						ar1,ar2,_ = roi_out_circle_br.shape
						if ar1==0 or ar2==0:
							break

						mask_in_tl = cv2.inRange(roi_in_circle_tl, lower_green1, upper_green1)
						mask_in_tr = cv2.inRange(roi_in_circle_tr, lower_green1, upper_green1) 
						mask_in_bl = cv2.inRange(roi_in_circle_bl, lower_green1, upper_green1)
						mask_in_br = cv2.inRange(roi_in_circle_br, lower_green1, upper_green1)
						mask_out_tl = cv2.inRange(roi_out_circle_tl, lower_green1, upper_green1)
						mask_out_tr = cv2.inRange(roi_out_circle_tr, lower_green1, upper_green1)
						mask_out_bl = cv2.inRange(roi_out_circle_bl, lower_green1, upper_green1)
						mask_out_br = cv2.inRange(roi_out_circle_br, lower_green1, upper_green1)
							
						if mask_in_tl.shape != mask_in_tr.shape:
							break
						if mask_in_bl.shape != mask_in_br.shape:
							break
						if mask_out_tl.shape != mask_out_tr.shape:
							break
						if mask_out_bl.shape != mask_out_br.shape:
							break

						inside_top_mask = cv2.bitwise_and(mask_in_tl,mask_in_tr)
						inside_bottom_mask = cv2.bitwise_and(mask_in_bl,mask_in_br)
							
						if inside_top_mask.shape != inside_bottom_mask.shape:
							break

						inside_mask = cv2.bitwise_and(inside_top_mask,inside_bottom_mask)
						outside_top_mask = cv2.bitwise_or(mask_out_tl,mask_out_tr)
						outside_bottom_mask = cv2.bitwise_or(mask_out_bl,mask_out_br)

						if outside_top_mask.shape != outside_bottom_mask.shape:
							break

						outside_mask = cv2.bitwise_or(outside_top_mask,outside_bottom_mask)
						'''
						cv2.imshow('mask_in_tl',roi_in_circle_tl)
						cv2.imshow('mask_in_tr',roi_in_circle_tr)
						cv2.imshow('mask_in_bl',roi_in_circle_bl)
						cv2.imshow('mask_in_br',roi_in_circle_br)
						cv2.imshow('mask_out_tl',roi_out_circle_tl)
						cv2.imshow('mask_out_tr',roi_out_circle_tr)
						cv2.imshow('mask_out_bl',roi_out_circle_bl)
						cv2.imshow('mask_out_br',roi_out_circle_br)
						'''
							
						cv2.imshow('mask_in_tl',mask_in_tl)
						cv2.imshow('mask_in_tr',mask_in_tr)
						cv2.imshow('mask_in_bl',mask_in_bl)
						cv2.imshow('mask_in_br',mask_in_br)
						cv2.imshow('mask_out_tl',mask_out_tl)
						cv2.imshow('mask_out_tr',mask_out_tr)
						cv2.imshow('mask_out_bl',mask_out_bl)
						cv2.imshow('mask_out_br',mask_out_br)
						
						cv2.imshow('inside_mask',inside_mask)
						cv2.imshow('outside_mask',outside_mask)
						new_mask = cv2.bitwise_xor(inside_mask,outside_mask)
							
						cv2.imshow('new_mask',new_mask)
						number = np.count_nonzero(new_mask)
							#print('number is',number)
							    #print('new_mask',new_mask)
						print('num',number)
						if number>30 and number<300:
							print(ratio)
							print('ball detected')
							cv2.circle(frame,center,2,(0,0,0),3)
							s.sendall('stop code')
								#time.sleep(100)
						else:
							print('no ball')
						roi = []

    #*************************************************************************************************

        cv2.imshow("Frame", frame)


        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()