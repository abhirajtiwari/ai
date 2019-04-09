#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

ob1 = Twist()

ob1.linear.x=2.0
ob1.linear.y=0
ob1.linear.z=0

ob1.angular.x=0
ob1.angular.y=0
ob1.angular.z=-1.8

def talker():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 1hz

    while not rospy.is_shutdown():

        rospy.loginfo(ob1)
        pub.publish(ob1)



        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
