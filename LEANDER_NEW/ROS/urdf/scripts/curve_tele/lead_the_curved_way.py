#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import NavSatFix
from math import *

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def short_angle(x, y):
    if abs(x - y) < 180.0:
        return (abs(x - y))

    else:
        return (360.0 - abs(x - y))

def haversine(lat1, lon1, lat2, lon2):
    # distance between latitudes
    # and longitudes

    global dist
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
    dist = rad * c



def bearing(lat1, lon1, lat2, lon2):
    global degree
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)

    degree = atan2(y, x) * 180 / pi

    if degree < 0:
        degree += 360

pitch = 0.0
roll = 0.0
yaw = 0.0

threshold = 0.45
b_threshold = 0.2

ob1 = Twist()

b = open("lat+lon_curve_fit_only.txt","r")




def forward():
    # print("FORWARD")
    ob1.linear.x = 0.5
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    pub.publish(ob1)


def backward():
    # print("BACKWARD")
    ob1.linear.x = -0.3
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0

    pub.publish(ob1)


def right():
    # print("RIGHT")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 1.0
    pub.publish(ob1)


def left():
    # print("LEFT")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = -1.0
    pub.publish(ob1)


def brutestop():
    # print("BRUTESTOP")
    ob1 = Twist()
    pub.publish(ob1)


heading = 0
degree = 0
dist = 10
lat1=0
lon1=0


def callback_imu(msg):
    global heading

    orientation_list = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

    heading = arduino_map(yaw, 0, -3, 0, 180)

    if heading < 0:
        heading += 360


def callback_gps(msg):
    global lat1, lon1

    lat1 = msg.latitude
    lon1 = msg.longitude


def waypoint_replay(lat2,lon2):
    global lat1, lon1

    haversine(lat1, lon1, lat2, lon2)
    bearing(lat1, lon1, lat2, lon2)


def displaydata(t, dist):
    if t < 10 and t > -10:
        print("STRAIGHT", "DISTANCE=", dist)
        forward()

    elif t <= -180:
        angle = 360 + t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()


    elif t < 0 and t > -180:
        angle = -t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()


    elif t >= 180:
        angle = 360 - t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()

    elif t > 0 and t < 180:
        angle = t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()



def listener():
    global dist
    rospy.Subscriber("imu_data", Imu, callback_imu)
    rospy.Subscriber("gps_topic", NavSatFix, callback_gps)

    while not rospy.is_shutdown():


        rospy.sleep(0.01)

        for line in b:
            lat2, lon2 = line.split(",")
            lat2 = float(lat2)
            lon2 = float(lon2)

            while (dist>0.3):

                waypoint_replay(lat2,lon2)
                t = heading - degree
                displaydata(t, dist)

            print("WAYPOINT REACHED")
            dist =10
            continue

        print("GOAL REACHED")
        brutestop()
        break

if __name__ == '__main__':
    try:
        global ob1
        pub = rospy.Publisher('champ', Twist, queue_size=10)
        rospy.init_node('Communication', anonymous=True)
        rate = rospy.Rate(50)  # 1hz


        listener()

    except rospy.ROSInterruptException:
        b.close()

