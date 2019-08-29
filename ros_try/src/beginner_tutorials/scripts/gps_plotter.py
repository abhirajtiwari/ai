#!/usr/bin/env python

import rospy
import matplotlib.pyplot as plt
import numpy as np
from sensor_msgs.msg import NavSatFix
from scipy.ndimage.interpolation import shift

dataLon = np.zeros(100)
dataLat = np.zeros(100)

iteration=0

def plot(x):
    global iteration
    global dataLat, dataLon
    dataLat[iteration] = x.latitude 
    dataLon[iteration] = x.longitude
    print dataLat
    print dataLon
    iteration+=1
    if iteration == 99:
        np.save('lat', dataLat)
        np.save('lon', dataLon)
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++'
        iteration = 0

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/phone1/android/fix', NavSatFix, plot)
    rospy.spin()

if __name__=='__main__':
    listener()
