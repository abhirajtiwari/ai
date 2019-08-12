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
    ob1.linear.x = -0.3
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
    ob1.angular.z = 0.5
    pub.publish(ob1)


def left():
    # print("LEFT")
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0
    ob1.angular.y = 0
    ob1.angular.z = -0.5
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


def rotate():
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 1.5
    pub.publish(ob1)

lat1=0
lon1=0
count = 0
lat_gps = 49.90008734734606
lon_gps = 8.899825168243158

def callback_gps(msg):
    global init_lat, init_lon, lat2, lon2, dist, count,lat_gps,lon_gps,distance_from_gps_point
    

    if count == 0:
        init_lat = msg.latitude
        init_lon = msg.longitude
        count = count+1
    lat2 = msg.latitude
    lon2 = msg.longitude

    dist = m.sqrt((lat2-init_lat)*(lat2-init_lat)+(lon2-init_lon)*(lon2-init_lon))*100000
    distance_from_gps_point = m.sqrt((lat_gps-lat2)*(lat_gps-lat2)+(lon_gps-lon2)*(lon_gps-lon2))*100000

def callback_imu(msg):
    global count_imu,heading
    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    heading = map(yaw, 0, -3, 0, 180)
    if heading < 0:
        heading += 360



#########################49.90008734734606, 8.899825168243158#############GPS point###########distance from origin##########15.632623717678888
def ball_search_not_correct():
    global flag,init_head,init_lat,init_lon,heading,flag1,flag3,doorie,lat2,lon2,lats,longs
    if distance_from_gps_point<20:
        if flag == 0:
            init_head = heading
            init_lat = lat2
            init_lon = lon2
            flag = 1
        print(init_head,heading,distance_from_gps_point)
        if flag1==0:
            flag1=1
            while (heading>4 and heading<356):
                right()
            brutestop()
        doorie = m.sqrt((lat2-init_lat)*(lat2-init_lat)+(lon2-init_lon)*(lon2-init_lon))*100000
        print(doorie,'doorie',lat2,lon2)
        if doorie<1:
            print('dekho mujhe',lat2,lon2)
            forward()
            lats.append(lat2)
            lons.append(lon2)
        elif doorie>1:
            #brutestop()
            if flag3==0:
                init_head = heading
                flag3=1
            while abs(init_head-heading)<90:
                left()
                print abs(init_head-heading)
            brutestop()

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

def ball_search():
    global lat2,lon2,dist,heading, distance_from_gps_point, init_head, init_lat, init_lon, flag, dist, flag1, flag2
    print('inside ball search')
    print('inside 1', dist, heading, distance_from_gps_point)
    if distance_from_gps_point<1148069:
        if flag == 0:
            flag = 1
            init_lat = lat2
            init_lon = lon2
            while (heading>4 and heading<356):
                print('right')
                right()
            lats.append(lat2)
            lons.append(lon2)
            brutestop()
        dist =0
        flag=0
        Go_2m()

        while heading>270 or heading<5:
            print('1')
            left()
        lats.append(lat2)
        lons.append(lon2)
        brutestop()
        print(dist)
        dist = 0
        flag=0
        Go_2m()

        while heading>180:
            print('2')
            left()
        brutestop()        
        lats.append(lat2)
        lons.append(lon2)
        print(dist,init_lat,lat2)
        dist = 0
        flag=0
        Go_2m()

        while heading<270:
            print('3')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        print(heading)
        dist = 0
        flag=0
        Go_4m()

        while heading<357 and heading>3:
            print('4')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist = 0
        flag=0
        Go_2m()

        while heading<90 or heading>357:
            print('5')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>2 and heading<357:
            print('6')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>270 or heading<5:
            print('7')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<357 and heading>3:
            print('8')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<90 or heading>357:
            print('9')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)        
        dist=0
        flag=0
        Go_4m()

        while heading<180:
            print('10')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>90:
            print('11')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>3 and heading<358:
            print('12')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading>270 or heading<5:
            print('13')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<357 and heading>3:
            print('14')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<90 or heading>357:
            print('15')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>2 and heading<357:
            print('16')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading>270 or heading<5:
            print('17')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('18')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('19')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)        
        dist=0
        flag=0
        Go_2m()

        while heading<357 and heading>3:
            print('20')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>270 or heading<5:
            print('21')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('22')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading>90:
            print('23')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<180:
            print('24')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('25')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading<357 and heading>3:
            print('26')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<90 or heading>357:
            print('27')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>2 and heading<357:
            print('28')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading>270 or heading<5:
            print('29')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('30')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('31')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<357 and heading>3:
            print('32')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>270 or heading<5:
            print('33')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('34')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()
                                
        while heading>90:
            print('35')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<180:
            print('36')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('37')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('38')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading>90:
            print('39')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>3 and heading<358:
            print('40')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<90 or heading>357:
            print('41')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading<180:
            print('42')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('43')
            right()
        brutestop()
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('44')
            left()
        brutestop()
        dist=0
        flag=0
        Go_2m()

        while heading>90:
            print('45')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<180:
            print('46')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading<270:
            print('47')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_4m()

        while heading<357 and heading>3:
            print('48')
            right()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>270 or heading<5:
            print('49')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        while heading>180:
            print('50')
            left()
        brutestop()
        lats.append(lat2)
        lons.append(lon2)
        dist=0
        flag=0
        Go_2m()

        flag=1

        hl, = plt.plot(lats, lons)
        for i,j in zip(lats,lons):
            update_line(hl,i,j)
            
        print('ooooooo do u see MEEEEEEE')
        plt.show()





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
