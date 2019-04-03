#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
rospy.init_node('lmaaaao', anonymous=True)
def handler(data):
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    # rospy.loginfo(data.msg)
    pub.publish(data)

sub = rospy.Subscriber('/turtle1/cmd_vel', Twist, handler)
rospy.spin()


