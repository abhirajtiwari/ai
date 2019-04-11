#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Vector3Stamped, Twist
from math import atan2
import pyproj
import numpy as np

geod = pyproj.Geod(ellps='WGS84')

destination = [49.900093,8.900088]

move_command = Twist()
coords = NavSatFix()
mag_vals = Vector3Stamped()

pub = rospy.Publisher('/gpsmag/cmd_vel', Twist, queue_size=10)
rospy.init_node('gps_mag')

def getGPS(data):
    global coords
    coords = data

def getMag(data):
    global mag_vals
    mag_vals = data

def do():
    global mag_vals
    reached = False
    heading = atan2(mag_vals.vector.y, mag_vals.vector.x)*(180/3.1415926)
    if heading < 0:
        heading += 360

    azi, bazi, dist = geod.inv(coords.longitude, coords.latitude, destination[1], destination[0])
    
    if dist < 2:
        reached = True

    rotate_by = azi - heading

    if azi >= heading:
        if abs(rotate_by) >= 180:
            turn_direction = False
        else:
            turn_direction = True
    elif heading >= azi:
        if abs(rotate_by) >= 180:
            turn_direction = True
        else:
            turn_direction = False

    if rotate_by > -15 and rotate_by < 15:
        rotate_by = 0
    if rotate_by == 0:
        move_command.linear.x = 1
        move_command.angular.z = 0
    elif turn_direction == True:
        move_command.linear.x = 0
        move_command.angular.z = 0.5
    elif turn_direction == False:
        move_command.linear.x = 0
        move_command.angular.z = -0.5
    if reached == True:
        move_command.linear.x = 0
        move_command.angular.z = 0

    pub.publish(move_command)

    rospy.loginfo('heading: %f, azi: %f, dist: %f, reached: %d' % (heading, azi, dist, reached))
    
    # rospy.loginfo(heading)

rospy.Subscriber('/magnetic', Vector3Stamped, getMag)
rospy.Subscriber('/fix', NavSatFix, getGPS)
while not rospy.is_shutdown():
    do()
    rospy.sleep(0.02)


