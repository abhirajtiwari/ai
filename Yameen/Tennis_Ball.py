import cv2
import cv2.cv as cv
import numpy as np

cap = cv2.VideoCapture(0)
kernel = np.ones((3,3),np.float32)

while True:
    _, frame = cap.read()
    #blurred_frame = cv2.GaussianBlur(frame, (3, 1), 0)
    bfilter = cv2.bilateralFilter(frame, 5, 90, 90)
    hsv = cv2.cvtColor(bfilter, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([26, 89, 6])
    upper_blue = np.array([64, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    dilation = cv2.dilate(mask, kernel, iterations=3)
#    erosion = cv2.erode(dilation, kernel, iterations=1)

#HOUGH_CIRCLES


    circles = cv2.HoughCircles(dilation, cv.CV_HOUGH_GRADIENT, 1, 200, param1=255, param2=25, minRadius=0, maxRadius=0)
    #     # print circles

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")


        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
            #cv2.rectangle(frame, (x - 60, y - 60), (x + 60, y + 60), (0, 128, 255), 1)
            #print('radius',radius)
            #print('area', area)

#*********************************************************************************************************************

#COUNTERS
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #contours2, _ = cv2.findContours(contours1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    update=[]
    if len(contours) != 0:
        for counter in contours:
# ***********for selecting the maximum area************

            update.append(counter)
            c = max(update, key=cv2.contourArea)

# *******************************************************

            #***********for rotated rectangle*******************
            rect = cv2.minAreaRect(counter)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)

            x1 = box[0, 0]
            y1 = box[0, 1]
            x2 = box[1, 0]
            y2 = box[1, 1]
            x3 = box[2, 0]
            y3 = box[2, 1]
            x4 = box[3, 0]
            y4 = box[3, 1]

            area_rotated_rect = 1 / 2 * abs(x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1 - (x2 * y1 + x3 * y2 + x4 * y3 + x1 * y4))
#**************************************************************



#area = cv2.contourArea
        #hull = cv2.convexHull(counter)
            x_rec, y_rec, w_rec, h_rec = cv2.boundingRect(c)
        #ellipse = cv2.fitEllipse(counter)


#***********for simple rectangle***************
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            ratio = w_rec / h_rec

            area_rec = w_rec * h_rec

            #if ratio>=1 and ratio<=1.5
#*************************************************




            area_ratio = area_rec/(area_rotated_rect+0.0001)
            area_circle = np.pi*radius*radius
            print('___________________________________________')
            print('area_rotated_rec',area_rotated_rect)
            print('area_rec',area_rec)
            print('area_ratio',area_ratio)
            print('ratio',ratio)
            print('area_circle',area_circle)
#            print('contour_area',area)
            print('____________________________________________')
            #print('box=', box, 'box1',box[0,1])

        #print('x',x,'y',y,'x_rec', x_rec,'y_rec',y_rec,'radius',radius,'width',w_rec,'height',h_rec)

            area_diff = area_rec - area_rotated_rect
            print(area_diff)
            #if ratio < 1.2 and ratio > 0.8 and area_rec > 100 and area_rotated_rect > 100 and area_circle > 500 and area_circle < 20000 and area_ratio < 1.7: #and  area_ratio < 1.25 and area_ratio > 0.75:
            if area_diff < 800 and area_diff > 20 and ratio < 1.2 and ratio > 0.8:
                #if(area_circle<8000 and area > 5000):
        #if :#area<2500 and area>50 :
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                #cv2.drawContours(frame, counter, -1, (0, 255, 0), 3)
                #cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                cv2.rectangle(frame, (x_rec, y_rec), (x_rec + w_rec, y_rec + h_rec), (0, 255, 0), 2)
                cv2.drawContours(frame, [box], -1, (0, 255, 255), 2)


#*************************************************************************************************

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", dilation)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
