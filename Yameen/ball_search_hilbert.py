#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from pynput import keyboard
from pynput.keyboard import Key
from tf.transformations import euler_from_quaternion
from math import *
import time
import matplotlib.pyplot as plt
import numpy

ob1 = Twist()



def cartesian_distance(lat1,lon1,lat2,lon2):
    return sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def forward():
    global  ob1
    #print("FORWARD")
    ob1.linear.x = 0.5
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    pub.publish(ob1)

def backward():
    # print("BACKWARD")
    global ob1
    ob1.linear.x = -0.5
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0

    pub.publish(ob1)


def right():
    # print("RIGHT")
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0.1
    pub.publish(ob1)


def left():
    # print("LEFT")
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.y = 0
    ob1.angular.z = -0.1
    pub.publish(ob1)


def brutestop():
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    #print("stop",ob1)
    pub.publish(ob1)




count = 0


def callback_gps(msg):
    global init_lat, init_lon, lat2, lon2, dist, count,lat_gps,lon_gps
    

    if count == 0:
        init_lat = round(msg.latitude,7)
        init_lon = round(msg.longitude,7)
        count = 1
    lat2 = round(msg.latitude,8)
    lon2 = round(msg.longitude,8)

    dist = haversine(lat2,lon2,init_lat,init_lon)
    #print('lat lon',lat2,lon2)


def callback_imu(msg):
    global heading
    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    heading = map(yaw, 0, -3, 0, 180)
    if heading < 0:
        heading += 360

def update_line(hl, new_data_lat, new_data_lon):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data_lat))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data_lon))
    plt.draw()



def rotate():
    global distance_points, X, Y, X_temp, Y_temp, deg, heading, degree
    a = 0
    b = 0
    c = 0
    d = 0
    if deg==90 :
        if a == 0:
            while (heading<deg or heading>350):
                right()
                #print('heading',heading,degree)
                a = 1
                print('1')
            brutestop()
        if a == 0:
            while (heading>deg):
                left()
                #print('heading',heading,degree)
                a=1
                print('2')
            brutestop()
        print('12')
        travel()

    elif deg==180 :
        if c == 0:
            while (heading<deg):
                right()
                #print('heading',heading,degree)
                c = 1
                print('3')
            brutestop()
        if c == 0:
            while (heading>deg):
                left()
                #print('heading',heading,degree)
                c = 1
                print('4')
            brutestop()
        print('34')
        travel()

    elif deg==270 :
        if d == 0:
            while (heading<deg):
                right()
                #print('heading',heading,degree)
                d = 1
                print('5')
            brutestop()
        if d == 0:
            while (heading>deg or heading<10):
                left()
                #print('heading',heading,degree)
                d = 1
                print('6')
            brutestop()
        print('56')
        travel()
        
    elif deg == 0:
        if b == 0:
            while heading<360 and heading>300:
                right()
                #print('heading',heading,degree)
                b = 1
                print('7')
            brutestop()
        if b == 0:
            while heading>0 and heading<60:
                left()
                #print('heading',heading,degree)
                b = 1
                print('8')
            brutestop()

        
        print('66')
        travel()
    flag1 = 1

def travel():
    global distance_points,lat2,lon2,X_temp,Y_temp, X, Y, heading, counter1, prev_dist, counter2, prev_prev_dist, iteration
    distance_points = haversine(lat2,lon2,X,Y)
    
    while distance_points>0.9:
        distance_points = haversine(lat2,lon2,X,Y)
        if counter1%20 == 0:
            prev_dist = distance_points

        if counter2%600 == 0:
            prev_prev_dist = distance_points
        

        counter1 = counter1 + 1
        counter2 = counter2 + 1
        print('dist points',distance_points,'pichla ',prev_dist,'pichla pichla ',prev_prev_dist, iteration)
        forward()
    brutestop()
    flag1 = 0


def haversine(lat1, lon1, lat2, lon2):
    # distance between latitudes
    # and longitudes

    
    dLat = (lat2 - lat1) * pi / 180.0
    dLon = (lon2 - lon1) * pi / 180.0

    # convert to radians
    lat1 = (lat1) * pi / 180.0
    lat2 = (lat2) * pi / 180.0

    # apply formulae
    a = (pow(sin(dLat / 2), 2) +
         pow(sin(dLon / 2), 2) *
         cos(lat1) * cos(lat2))
    rad = 6378.1 * 1000
    c = 2 * asin(sqrt(a))
    haver_dist = rad * c
    return haver_dist

def bearing(lat1, lon1, lat2, lon2):
    global degree
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)

    degree = atan2(y, x) * 180 / pi

    if degree < 0:
        degree += 360




def hilbert(x0, y0, xi, xj, yi, yj, n):
    global lat2,lon2,heading, flag, distance, X, Y, X_temp, Y_temp, flag2, flag1, flag3, distance_points, degree, deg, iteration, prev_prev_dist, prev_dist, counter5, counter6
    if n <= 0:

        X = x0 + (xi + yi)/2
        Y = y0 + (xj + yj)/2
        if flag3 == 0:                          ###########this should run once
            
            bearing(lat2, lon2, X, Y)
            flag3 = 1

            '''
            dLat = (X - lat2) * pi / 180.0
            dLon = (Y - lon2) * pi / 180.0

            lat2 = (lat2) * pi / 180.0
            X_lat = (X) * pi / 180.0

            y = cos(X_lat) * sin(dLon)
            x = (cos(lat2) * sin(X_lat)) - (sin(lat2) * cos(X_lat) * cos(dLon))
            degree = atan2(y, x) * 180 / pi
            
            #76.7920516, 74.79213001327778, 15.3476016, 13.347667362137521
            if degree < 0:
                degree += 360
            '''

        if flag2 == 1:
            bearing(lat2, lon2, X, Y)

            
            
            distance_points = haversine(lat2,lon2,X,Y)
            if degree < 0:
                deg += 360

            if degree>45 and degree<135:
                deg = 90

            elif degree>=135 and degree<225:
                deg = 180

            elif degree>=225 and degree<315:
                deg = 270

            else:
                deg = 0

            print('degree',degree,'deg',deg,'head',heading)

        if flag == 0:                       ###########this should run once
            while abs(heading-degree)>0.2:
                print(heading,degree,'abs',abs(heading-degree))
                right()
            brutestop()
            distance = haversine(lat2,lon2,X,Y)
            while distance>0.9:
                distance = haversine(lat2,lon2,X,Y)
                if counter5%2 == 0:
                    prev_dist = distance

                if counter6%100000 < 100:
                    prev_prev_dist = distance


                counter5 = counter5 + 1
                counter6 = counter6 + 1

                print('dis',distance, 'head', heading,prev_dist,prev_prev_dist)
                forward()
            brutestop()
            flag = 1
            #travel()
        if flag2 == 1:
            rotate()



        if flag1 == 0:
            X_temp = X
            Y_temp = Y
            flag1 = 1
            flag2 = 1

        iteration += 1
        brutestop()
        ##########0.632444427681901
        # Output the coordinates of the cv
#        print '%s %s 0' % (X, Y)
    else:
        hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1)
        hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1)
        hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1)


def ball_search():
    global lat2,lon2,dist,heading, init_head, init_lat, init_lon, flag, dist, flag1, flag2,counter4
    print('inside ball search')
    print('dist and head', dist, heading)
    
##'inside 1', 6.673292331661946, 54.306002108193724, 13.347669526053634, 74.79207737914214, 13.347612982162849, 74.79204193804355
    if dist>3:
        counter4=1
        hilbert(lat2, lon2, 0.00035, 0.0, 0.0, 0.00035, 3)
        print('ooooooo do u see MEEEEEEE',lat2,lon2,dist)



####15.3476016 76.7920516


def talk_listen():
    global counter4
    def call_stop(key):  # what to do on key-release
        print "look at me"
        brutestop()
        return False  # stop detecting more key-releases

    def call_key(key):  # what to do on key-press
        print "do you see me"
        global flag_for_stop_key, flag

        if key == Key.up:
            forward()
        elif key == Key.down:
            backward()

        elif key == Key.right:
           right()

        elif key == Key.left:
            left()
        print(key)
        return False

    rospy.Subscriber("gps_topic", NavSatFix, callback_gps)
    rospy.Subscriber("imu_data", Imu, callback_imu)


    while not rospy.is_shutdown():

        with keyboard.Listener(on_press=call_key) as listener1:  # setting code for listening key-press
            listener1.join()

        with keyboard.Listener(on_release=call_stop) as listener2:  # setting code for listening key-release
            listener2.join()
        
        if counter4==0:
            ball_search()
        
        rate.sleep()

if __name__ == '__main__':
    try:
        count_imu = 0
        flag = 0
        flag1=0
        flag2=0
        flag3=0
        counter = 0
        counter1 = 0
        counter2 = 0
        prev_dist = 0
        prev_prev_dist = 0
        iteration = 0
        counter4 = 0
        counter5 = 0
        counter6 = 0 
        pub = rospy.Publisher('arrow_control', Twist, queue_size=10)
        print(pub)
        print "1111"
        rospy.init_node('talker', anonymous=True)
        print "2222"
        rate = rospy.Rate(50)
        print "3333"
        talk_listen()
        print "4444"
    except rospy.ROSInterruptException:
        pass
