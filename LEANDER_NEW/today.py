#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion

def arduino_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min




pitch=0.0
roll=0.0
yaw=0.0

def callback(msg):
    global pitch,roll,yaw

    orientation_list=[msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w]
    (roll,pitch,yaw)=euler_from_quaternion(orientation_list)

    heading=arduino_map(yaw,0,-3,0,180)

    if heading<0:
        heading+=360

    print (heading)



def listener():

    rospy.init_node('listening', anonymous=True)

    rospy.Subscriber("imu_data", Imu, callback)
    rospy.spin()



if __name__ == '__main__':
    listener()
