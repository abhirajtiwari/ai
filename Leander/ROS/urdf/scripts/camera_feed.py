#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def callback(data):
    br = CvBridge()
    rospy.loginfo('receiving image')
    cv2.imshow("camera",br.imgmsg_to_cv2(data))
    cv2.waitKey(1)


def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('rrbot/camera1/image_raw', Image, callback)

    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    listener()
