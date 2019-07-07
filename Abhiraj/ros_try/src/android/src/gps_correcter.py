#!/usr/bin/env python

import rospy 
from sensor_msgs.msg import NavSatFix

rospy.init_node('gps_correcter.py', anonymous=True)
pub = rospy.Publisher('/phone/fix', NavSatFix, queue_size=10)

def correct(data):
    data.altitude = 400
    data.header.stamp = rospy.Time.now()
    pub.publish(data)

def main():
    rospy.Subscriber('/phone/pre_fix', NavSatFix, correct)
    rospy.spin()

if __name__=='__main__':
    main()
