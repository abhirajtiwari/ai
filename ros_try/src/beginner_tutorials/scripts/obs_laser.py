#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

thresh = 2
thresh_side = 3

move_command = Twist()
pub = rospy.Publisher('/obs/cmd_vel', Twist, queue_size=10)
rospy.init_node('laser_reader')


def avoidObstacles(data):
    data = np.array(data.ranges)
    if np.amin(data[144:360]) < thresh and np.amin(data[660:720]) > thresh_side:
        move_command.linear.x = 0
        move_command.angular.z = -0.5
    elif np.amin(data[361:567]) < thresh and np.amin(data[0:60]) > thresh_side:
        move_command.linear.x = 0
        move_command.angular.z = 0.5
    else:
        move_command.angular.z = 0
        move_command.linear.x = 0.5

    if np.amin(data[0:60]) < thresh_side or np.amin(data[660:720]) < thresh_side:
        move_command.angular.x = 0.00001
    else:
        move_command.angular.x = 0

    pub.publish(move_command)

if __name__ == '__main__':
    rospy.Subscriber('/scan', LaserScan, avoidObstacles)
    while not rospy.is_shutdown():
         rospy.sleep(0.01)
