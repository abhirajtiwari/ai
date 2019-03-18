import cv2
import numpy as np
from math import sqrt
import time

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

def ROI(img,y_lrange,y_urange,x_lrange,x_urange):
    RoI = img[y_lrange:y_urange,x_lrange:x_urange]
    return RoI

while True:
    ret, frame = cap.read()
        #blurred_frame = cv2.GaussianBlur(frame, (3, 1), 0)
    #time.sleep(0.1)
    if ret == True:
        gamma = 1
        frame = adjust_gamma(frame, gamma=gamma)

        H_min = cv2.getTrackbarPos('H_min','HSV')
        S_min = cv2.getTrackbarPos('S_min','HSV')
        V_min = cv2.getTrackbarPos('V_min','HSV')
        H_max = cv2.getTrackbarPos('H_max','HSV')
        S_max = cv2.getTrackbarPos('S_max','HSV')
        V_max = cv2.getTrackbarPos('V_max','HSV')

        bfilter = cv2.bilateralFilter(frame, 5, 90, 90)
        hsv = cv2.cvtColor(bfilter, cv2.COLOR_BGR2HSV)

        lower_green = np.array([25, 89, 6])
        upper_green = np.array([64, 255, 255])

        lower_green1 = np.array([15, 74, 6])
        upper_green1 = np.array([87, 255, 255])
    #    lower_green = np.array([H_min,S_min,V_min])
    #    upper_green = np.array([H_max,S_max,V_max])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        dilation = cv2.dilate(mask, kernel, iterations=2)
        #dilation = cv2.erode(dilation, kernel, iterations=3)        #this is erosion

        cv2.imshow('dila',dilation)
    #COUNTERS
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #contours2, _ = cv2.findContours(contours1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print('c',contours)
        update=[]
        if len(contours) != 0:
            for counter in contours:
    # ***********for selecting the maximum area************
                #print('cont',contours)
                #cv2.imshow('contours',contours)
                #cv2.imshow('co',contours)
                update.append(counter)
                #print('u',update)
                #print('up',update)
                c = max(update, key=cv2.contourArea)
                #print('c',c)
    # *******************************************************

                #***********for rotated rectangle*******************
                #minAreaReact returns center(x,y) width height angle of rotation
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
                
                #rect[1][0] is width
                #print('rect',rect[1][0])                
                #print('frame shape',frame.shape)
                if rect[1][0]>5 and rect[1][1]>5:
                    if abs(rect[1][0] - rect[1][1])<5:
                        print('center is',center)
                        #cv2.rectangle(frame,(x_rec,y_rec),(x_rec+w_rec,y_rec+h_rec),(0,255,0),2)
                        #cv2.circle(frame,center,radius,(0,0,0),1)
                        #print('radius',radius+3)
                        #cv2.drawContours(frame, [box], -1, (255, 0, 0), 1)
                        #print('diff',abs(rect[1][0] - rect[1][1]))
                        #print('x y',x_rec,y_rec,w_rec,h_rec)
                                            
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
                            #cv2.circle(roi,((x_max-x_min)/2,(y_max-y_min)/2),radius,(255,0,0),1)
                            #roi = adjust_gamma(roi,gamma=gamma1)
                            y_roi,x_roi,_ = roi.shape
                            print('s',roi.shape)
                            print('y,x',y_roi,x_roi)
                            
                            print('ra',radius)
                            side_length = radius*2
                            side_length = int(side_length)
                            print('side_le',side_length)
                            length = (side_length/sqrt(2) - radius)/sqrt(2)
                            length = int(length)
                            print('le',length)
                            print('length_roi',len(roi))
                            roi_in_circle_tl = roi[y_roi/2 - length: y_roi/2, x_roi/2 - length: x_roi/2]   #inside circle top left roi
                            roi_in_circle_tr = roi[y_roi/2 - length: y_roi/2, x_roi/2: x_roi/2 + length]   #inside circle top right roi
                            roi_in_circle_bl = roi[y_roi/2: y_roi/2 + length, x_roi/2 - length: x_roi/2]   #inside circle bottom left roi
                            roi_in_circle_br = roi[y_roi/2: y_roi/2 + length, x_roi/2: x_roi/2 + length]   #inside circle bottom right roi
                            roi_out_circle_tl = roi[0:length,0:length]
                            roi_out_circle_tr = roi[0:length,side_length - length:side_length]
                            roi_out_circle_bl = roi[side_length - length:side_length,0:length]
                            roi_out_circle_br = roi[side_length - length:side_length,side_length - length:side_length]
                            
                            print('sad',len(roi_in_circle_tl))

                            if len(roi_in_circle_tl) == 0:
                                break
                            if len(roi_in_circle_tr) == 0:
                                break
                            if len(roi_in_circle_bl) == 0:
                                break
                            if len(roi_in_circle_br) == 0:
                                break
                            if len(roi_out_circle_tl) == 0:
                                break
                            if len(roi_out_circle_tr) == 0:
                                break
                            if len(roi_out_circle_bl) == 0:
                                break
                            if len(roi_out_circle_br) == 0:
                                break
                            
                            cv2.imshow('roi',roi)
                            print('dsa',roi_out_circle_tr.shape)
                            print(len(roi_out_circle_tr))
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

                            inside_top_mask = cv2.bitwise_or(mask_in_tl,mask_in_tr)
                            inside_bottom_mask = cv2.bitwise_or(mask_in_bl,mask_in_br)
                            
                            if inside_top_mask.shape != inside_bottom_mask.shape:
                                break

                            inside_mask = cv2.bitwise_or(inside_top_mask,inside_bottom_mask)
                            outside_top_mask = cv2.bitwise_and(mask_out_tl,mask_out_tr)
                            outside_bottom_mask = cv2.bitwise_and(mask_out_bl,mask_out_br)
                            
                            if outside_top_mask.shape != outside_bottom_mask.shape:
                                break

                            outside_mask = cv2.bitwise_and(outside_top_mask,outside_bottom_mask)
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
                            print('number is',number)
                                #print('new_mask',new_mask)
                            if number>15 and number<300:
                                print('ball detected')
                            else:
                                print('no ball')
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
