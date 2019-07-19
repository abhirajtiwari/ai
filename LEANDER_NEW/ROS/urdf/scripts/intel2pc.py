#!/usr/bin/env python
from roslib import message
import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2
from math import sqrt




def point_callback(data) :


    for point in pc2.read_points(data, field_names=("x", "y", "z"), skip_nans=False, uvs=[[64, 240],[128,240],[192,240],[256,240],[320,240],[384,240],[448,240],[512,240],[576,240],[639,240]]):
        pt_x = point[0]
        pt_y = point[1]
        pt_z = point[2]
        #print(pt_x,pt_y,pt_z)
        print("DISTANCE:=",sqrt(pt_x**2+pt_y**2+pt_z**2))


#listener
def listener():
    rospy.Subscriber('r200/camera/depth_registered/points', PointCloud2, point_callback)

    while not rospy.is_shutdown():
        #talker()
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:
        rospy.init_node('listener', anonymous=True)

        rate = rospy.Rate(50)  # 1hz

        listener()

    except rospy.ROSInterruptException:
        pass
