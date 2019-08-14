#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from pynput import keyboard
from pynput.keyboard import Key
from tf.transformations import euler_from_quaternion
import math as m
import time
import matplotlib.pyplot as plt
import numpy

ob1 = Twist()

lats = []
lons = []

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
    ob1.angular.z = 0.3
    pub.publish(ob1)


def left():
    # print("LEFT")
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.y = 0
    ob1.angular.z = -0.3
    pub.publish(ob1)


def brutestop():
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    print("stop",ob1)
    pub.publish(ob1)



lat1=0
lon1=0
count = 0
lat_gps = 49.90008734734606
lon_gps = 8.899825168243158

def callback_gps(msg):
    global init_lat, init_lon, lat2, lon2, dist, count,lat_gps,lon_gps
    

    if count == 0:
        init_lat = msg.latitude
        init_lon = msg.longitude
        count = count+1
    lat2 = msg.latitude
    lon2 = msg.longitude

    dist = m.sqrt((lat2-init_lat)*(lat2-init_lat)+(lon2-init_lon)*(lon2-init_lon))*100000


def callback_imu(msg):
    global count_imu,heading
    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    heading = map(yaw, 0, -3, 0, 180)
    if heading < 0:
        heading += 360



def gogogo():
    global flag, init_lat,lat2,init_lon,lon2,heading,dist
    if flag == 0:
        flag = 1
        init_lat = lat2
        init_lon = lon2
    print('heading and lati and dist ',heading,lat2, dist)

def update_line(hl, new_data_lat, new_data_lon):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data_lat))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data_lon))
    plt.draw()


def Go_2m():
    global dist
    while (dist<2):
        gogogo()
        forward()
    brutestop()

def Go_4m():
    global dist
    while (dist<4):
        gogogo()
        forward()
    brutestop()

def rotate():
    global distance_points, X, Y, X_temp, Y_temp, degree, heading
    f = 0
    if degree!=0 :
        if f == 0:
            while (heading<degree):
                right()
                print('heading',heading,degree)
                f = 1
                print('1')
            brutestop()
        if f == 0:
            while (heading>degree):
                left()
                print('heading',heading,degree)
                f=1
                print('2')
            brutestop()
    print('55')
    travel()

    b = 0
    if degree == 0:
        if heading>300:
            while heading<360 and heading>300:
                right()
                print('heading',heading,degree)
                b = 1
                print('3')
            brutestop()
        if heading<60:
            while heading>0 and heading<60:
                left()
                print('heading',heading,degree)
                b = 1
                print('4')
            brutestop()

        flag1 = 1
    print('66')

    travel()

def travel():
    global distance_points,lat2,lon2,X_temp,Y_temp

    while distance_points>0.02828262:
        distance_points = m.sqrt((lat2-X_temp)*(lat2-X_temp)+(lon2-Y_temp)*(lon2-Y_temp))/100
        print('disdisdis',distance_points)
        forward()
    brutestop()

def hilbert(x0, y0, xi, xj, yi, yj, n):
    global lat2,lon2,heading, flag, distance, X, Y, X_temp, Y_temp, flag2, flag1, flag3, distance_points, degree
    if n <= 0:

        X = x0 + (xi + yi)/2
        Y = y0 + (xj + yj)/2
        if flag3 == 0:                          ###########this should run once
            dLat = (X - lat2) * m.pi / 180.0
            dLon = (Y - lon2) * m.pi / 180.0

            lat2 = (lat2) * m.pi / 180.0
            X_lat = (X) * m.pi / 180.0

            y = m.cos(X_lat) * m.sin(dLon)
            x = (m.cos(lat2) * m.sin(X_lat)) - (m.sin(lat2) * m.cos(X_lat) * m.cos(dLon))
            degree = m.atan2(y, x) * 180 / m.pi
            flag3 = 1
            #76.7920516, 74.79213001327778, 15.3476016, 13.347667362137521
            if degree < 0:
                degree += 360
        
        if flag2 == 1:
            dLat = (X - X_temp) * m.pi / 180.0
            dLon = (Y - Y_temp) * m.pi / 180.0

            X_temp_lat = (X_temp) * m.pi / 180.0
            X_lat = (X) * m.pi / 180.0

            y = m.cos(X_lat) * m.sin(dLon)
            x = (m.cos(X_temp_lat) * m.sin(X_lat)) - (m.sin(X_temp_lat) * m.cos(X_lat) * m.cos(dLon))
            degree = m.atan2(y, x) * 180 / m.pi            
            print('tempp',X_temp,X,Y_temp,Y,degree)
            distance_points = m.sqrt((lat2-X_temp)*(lat2-X_temp)+(lon2-Y_temp)*(lon2-Y_temp))/100
            if degree < 0:
                degree += 360

            if degree>75 and degree<105:
                degree = 90

            elif degree>165 and degree<195:
                degree = 180

            elif degree>255 and degree<285:
                degree = 270

            else:
                degree = 0

            print('sfrgvbtbtbtbt',degree,heading)

        if flag == 0:                       ###########this should run once
            while abs(heading-degree)>2:
                print(heading,degree,'abs',abs(heading-degree))
                right()
            brutestop()
            print('deg ',degree, Y, lon2, X, lat2, flag)
            distance = m.sqrt((X-lat2)*(X-lat2)+(Y-lon2)*(Y-lon2))
            print('distaance', distance)
            while distance>0.35362:
                distance = m.sqrt((X-lat2)*(X-lat2)+(Y-lon2)*(Y-lon2))
                print('dis',distance,  Y, lon2, X, lat2)
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
    global lat2,lon2,dist,heading, init_head, init_lat, init_lon, flag, dist, flag1, flag2
    print('inside ball search')
    print('inside 1', dist, heading, lat2, lon2, init_lat, init_lon)
##'inside 1', 6.673292331661946, 54.306002108193724, 13.347669526053634, 74.79207737914214, 13.347612982162849, 74.79204193804355
    if dist>7:
        hilbert(13.3476016, 74.7920516, 4.0, 0.0, 0.0, 4.0, 3)
        print('ooooooo do u see MEEEEEEE',lat2,lon2,dist)



####15.3476016 76.7920516


def talk_listen():
    
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
    print("see this")
    rospy.Subscriber("imu_data", Imu, callback_imu)
    #rospy.Subscriber("gps_topic", NavSatFix, callback_search)


    while not rospy.is_shutdown():

        with keyboard.Listener(on_press=call_key) as listener1:  # setting code for listening key-press
            listener1.join()

        with keyboard.Listener(on_release=call_stop) as listener2:  # setting code for listening key-release
            listener2.join()
        ball_search()
        rate.sleep()

if __name__ == '__main__':
    try:
        count_imu = 0
        flag = 0
        flag1=0
        flag2=0
        flag3=0
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
