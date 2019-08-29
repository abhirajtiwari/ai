#!/usr/bin/env python
import rospy
import signal
import os
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

rospy.init_node('obs_avoid', anonymous=True)
p = rospy.Publisher('ddrobot/cmd_vel', Twist, queue_size=10)

r_data = Range()
l_data = Range()

def right(data):
    global r_data
    r_data = data

def left(data):
    global l_data
    l_data = data

def do():
    global r_data, l_data
    command = Twist()
    if r_data.range < 3 and l_data.range > 3:
        command.angular.z = 1
    elif r_data.range > 3 and l_data.range < 3:
        command.angular.z = -1
    elif r_data.range < 3 and l_data.range < 3:
        command.linear.x = -1
    else:
        command.linear.x = 0.1
    rospy.loginfo(command)
    p.publish(command)

def subscribers():
    rospy.Subscriber('sensor/us_front_r', Range, right)
    rospy.Subscriber('sensor/us_front_l', Range, left)
    while not rospy.is_shutdown():
        do()
        rospy.sleep(0.02)

subscribers()

