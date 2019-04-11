#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

move_gps = Twist()
move_laser = Twist()

rospy.init_node('muxer')
pub = rospy.Publisher('/ib/cmd_vel', Twist, queue_size=10)

def cmd_from_gps(data):
    global move_gps
    move_gps = data

def cmd_from_laser(data):
    global move_laser
    move_laser = data

def do():
    global move_laser, move_gps
    if move_laser.angular.z != 0 or move_laser.angular.x == 0.00001:
        pub.publish(move_laser)
        rospy.loginfo('Obstacle')
    else:
        pub.publish(move_gps)
        rospy.loginfo('Navigating')
    if move_gps.linear.x == 0:
        rospy.loginfo('Reached')

rospy.Subscriber('/gpsmag/cmd_vel', Twist, cmd_from_gps)
rospy.Subscriber('/obs/cmd_vel', Twist, cmd_from_laser)
while not rospy.is_shutdown():
    do()
    rospy.sleep(0.02)
