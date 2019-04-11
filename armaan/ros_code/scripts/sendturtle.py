#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
import pygame  
from sensor_msgs.msg import LaserScan 
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from tf.transformations import euler_from_quaternion
pygame.init()
pygame.joystick.init()
joy=pygame.joystick.Joystick(0)
joy.init()
dist=[]
def map(x,in_min,in_max,out_min,out_max):
        return ((x-in_min)*(out_max-out_min)/(in_max-in_min))+out_min


def callback(data):
    global dist
    dist= data.ranges
head=0
def callback1(data):
    q=[]
    global head 
    q.append(data.orientation.x)
    q.append(data.orientation.y)
    q.append(data.orientation.z)
    q.append(data.orientation.w)
    rpy=euler_from_quaternion(q)
    head=map(rpy[2],0,-3,0,180)
    if head<0:
        head+=360
def callback3(data):
    print data.latitude,data.longitude
     
x=0
y=0

def talker():
    
    pub = rospy.Publisher('/ib/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    rate = rospy.Rate(10) # 10hz
    x=y=0
    while not rospy.is_shutdown():
        
         
        """for events in pygame.event.get():
                if events.type==pygame.JOYAXISMOTION:
                        if events.axis==0:
                                x=joy.get_axis(0)                      
                        elif events.axis==1:
                                y=joy.get_axis(1)"""
        rospy.Subscriber("/scan", LaserScan, callback)
        rospy.Subscriber('/imu', Imu, callback1)
        rospy.Subscriber('/gps_data', NavSatFix, callback3)

        y=0
        x=0
        
        for i in dist[0:360]:
            if i<20:
                x=-1
                y=0
                break 
        for i in dist[360:720]:
            if i<20:
                x=1
                y=0
                break 
        sendinfo= Twist()
        sendinfo.linear.x=-y
        sendinfo.linear.y=0
        sendinfo.linear.z=0
        sendinfo.angular.x=0
        sendinfo.angular.y=0
        sendinfo.angular.z=x
	print "Sent"

        hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(sendinfo)
        pub.publish(sendinfo)
        rate.sleep()

        
if __name__ == '__main__':
    try:
        talker()
    	
    except rospy.ROSInterruptException:
        pass

