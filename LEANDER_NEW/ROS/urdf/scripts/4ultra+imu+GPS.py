#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
import time
from sensor_msgs.msg import NavSatFix
from math import *

def arduino_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


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
    rad = 6378.1*1000
    c = 2 * asin(sqrt(a))
    dist= rad*c
    if dist<1:
        brutestop()
        quit()


def bearing(lat1, lon1, lat2, lon2):
    global degree
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)

    degree = atan2(y, x) * 180 / pi

    if degree < 0:
        degree += 360


lat2=49.89990654904074
lon2=8.899935283587306


pitch=0.0
roll=0.0
yaw=0.0




threshold=0.45
b_threshold=0.2


ob1 = Twist()


def short_angle(x, y):
    if abs(x - y) < 180.0:
        return (abs(x - y))

    else:
        return (360.0 - abs(x - y))


def forward():
    #print("FORWARD")
    ob1.linear.x = 0.3
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    pub.publish(ob1)

def backward():
    #print("BACKWARD")
    ob1.linear.x = -0.3
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0

    pub.publish(ob1)

def right():
    #print("RIGHT")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 2.5
    pub.publish(ob1)

def left():
    #print("LEFT")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = -2.5
    pub.publish(ob1)


def brutestop():
    #print("BRUTESTOP")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    pub.publish(ob1)



def sideleftcheck():
    global distance4

    if distance4 < threshold+0.3 :
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()
        return -1
    else:
        return 1

def siderightcheck():
    global distance3

    if distance3 < threshold+0.3 :
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()
        return -1
    else:
        return 1

distance1=Range()
distance2=Range()
distance3=Range()
distance4=Range()


heading=0
degree=0
dist=0

def callback1(msg):
    global distance1
    distance1 = msg.range
    #print("DISTANCE1=",distance1)

def callback2(msg):
    global distance2
    distance2= msg.range
    #print("DISTANCE2=", distance2)

def callback3(msg):
    global distance3
    distance3= msg.range
    #print("DISTANCE3=", distance3)

def callback4(msg):
    global distance4
    distance4= msg.range
    #print("DISTANCE4=", distance4)
#
def callback_imu(msg):
    global heading

    orientation_list=[msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w]
    (roll,pitch,yaw)=euler_from_quaternion(orientation_list)

    heading=arduino_map(yaw,0,-3,0,180)

    if heading<0:
        heading+=360



def callback_gps(msg):
    global lat2,lon2,lat1,lon1


    lat1=msg.latitude
    lon1=msg.longitude

    haversine(lat1, lon1, lat2, lon2)
    bearing(lat1, lon1, lat2, lon2)


def displaydata(t, dist):
    if t < 10 and t > -10:
        print("STRAIGHT", "DISTANCE=", dist)
        forward()
        #
        #
        # return

    elif t <= -180:
        angle = 360 + t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()
        # p.ChangeDutyCycle(30)
        # q.ChangeDutyCycle(30)
        # return

    elif t < 0 and t > -180:
        angle = -t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()
        # p.ChangeDutyCycle(30)
        # q.ChangeDutyCycle(30)
        # return

    elif t >= 180:
        angle = 360 - t
        print("CLOCKWISE", angle, "DISTANCE=", dist)
        right()
        # p.ChangeDutyCycle(30)
        # q.ChangeDutyCycle(30)
        # return

    elif t > 0 and t < 180:
        angle = t
        print("ANTICLOCKWISE", angle, "DISTANCE=", dist)
        left()



def ultrasonic():

    global distance1,distance2,distance3,distance4,heading

    #print("DISTANCE1=",distance1,"DISTANCE2=", distance2)

    if distance1 < b_threshold or distance2 < b_threshold:
        backward()
        time.sleep(1)

        if distance1 < distance2:
            print("ULTRASONIC OVERRIDE: BACKWARD RIGHT")

            headA = heading
            headB = headA

            while short_angle(headA, headB) < 90:
                print("ULTRASONIC OVERRIDE: BACKWARD RIGHT")
                right()
                headB=heading

            #brutestop()

            checkB = sideleftcheck()

            while checkB == -1:
                checkB = sideleftcheck()

            return  -1

        else:
            print("ULTRASONIC OVERRIDE: BACKWARD LEFT")

            headC = heading
            headD = headC

            while short_angle(headC, headD) < 90:
                print("ULTRASONIC OVERRIDE: BACKWARD LEFT")
                left()
                headD = heading

            #brutestop()
            checkA = siderightcheck()

            while checkA == -1:
                checkA = siderightcheck()

            return -1


    elif (distance2 < threshold) and (distance2 < distance1):
        print("ULTRASONIC OVERRIDE: LEFT90")

        headA = heading
        headB = headA

        while short_angle(headA, headB) < 90:
            print("ULTRASONIC OVERRIDE: LEFT90")
            left()
            headB = heading
           

        #brutestop()
        checkA = siderightcheck()

        while checkA == -1:
            checkA = siderightcheck()

        return -1

    elif (distance1 < threshold) and (distance1 < distance2):
        headC = heading
        headD = headC

        while short_angle(headC, headD) < 90:
            print("ULTRASONIC OVERRIDE: RIGHT90")
            right()
            headD = heading

        #brutestop()
        checkB = sideleftcheck()

        while checkB == -1:
            checkB = sideleftcheck()

        return -1

    elif distance3 < threshold+0.3 :
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()

        return -1


    elif distance4 < threshold+0.3 :
        print("ULTRASONIC OVERRIDE: FORWARD---")
        forward()

        return -1

    else:
        return 1

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
       # name are launched, the previous one is kicked off. The
       # anonymous=True flag means that rospy will choose a unique
       # name for our 'listener' node so that multiple listeners can
       # run simultaneously.
    rospy.Subscriber("champ1", Range, callback1)
    rospy.Subscriber("champ2", Range, callback2)
    rospy.Subscriber("champ3", Range, callback3)
    rospy.Subscriber("champ4", Range, callback4)

    rospy.Subscriber("imu_data", Imu, callback_imu)
    rospy.Subscriber("gps_topic", NavSatFix, callback_gps)

    while not rospy.is_shutdown():

        #print("DISTANCE1=", distance1)
        #print("DISTANCE2=", distance2)
        while True:
            rospy.sleep(0.01)
            v=ultrasonic()
            if v==1:
                pass
            else:
                continue


            t= heading-degree

            displaydata(t,dist)




    # spin() simply keeps python from exiting until this node is stopped

if __name__ == '__main__':
    try:
        global ob1
        pub = rospy.Publisher('champ', Twist, queue_size=10)
        rospy.init_node('Communication', anonymous=True)
        rate = rospy.Rate(1)  # 1hz

        rospy.loginfo(ob1)

        listener()

    except rospy.ROSInterruptException:
        pass

