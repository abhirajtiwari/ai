#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

thresh = 2

move_command = Twist()
pub = rospy.Publisher('/obs/cmd_vel', Twist, queue_size=10)
rospy.init_node('laser_reader')


def avoidObstacles(data):
    data = np.array(data.ranges)
    if np.amin(data[144:360]) < thresh:
        move_command.linear.x = 0
        move_command.angular.z = -1
        pub.publish(move_command)
    elif np.amin(data[360:567]) < thresh:
        move_command.linear.x = 0
        move_command.angular.z = 1
        pub.publish(move_command)
    else:
        move_command.angular.z = 0
        move_command.linear.x = 0.5
        pub.publish(move_command)

if __name__ == '__main__':
    rospy.Subscriber('/scan', LaserScan, avoidObstacles)
    while not rospy.is_shutdown():
        rospy.sleep(0.01)
