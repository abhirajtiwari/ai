#!/usr/bin/env python
import rospy
import pygame
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen 

pygame.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

rospy.init_node('joy', anonymous=True)
pub = rospy.Publisher('ib/cmd_vel', Twist, queue_size=10)

try:
    numgears = 5
    x_joy = 0
    y_joy = 0
    gear= 0
    x_joy_last = 0
    y_joy_last = 0
    gear_last = 0
    state = False
    while True:
        # time.sleep(0.01) #WHY?????? DOES THIS MAKE IT SMOOTH
        x_joy = x_joy_last 
        y_joy = y_joy_last
        gear = gear_last
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    x_joy = event.value #-255 because the joystick was reverse mapped
                elif event.axis == 1:
                    y_joy = event.value*-1
                elif event.axis == 3:
                    gear = event.value
            elif event.type == pygame.JOYBUTTONDOWN:
                if joy.get_button(1):
                    state = not state
                    rospy.wait_for_service('/turtle1/set_pen')
                    pen_service = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
                    pen_service(0,0,0,0, state)

        x_joy_last = x_joy
        y_joy_last = y_joy
        gear_last = gear
        gear = int(abs((gear * (numgears/2)) - (numgears/2)))+1
        data = Twist()
        data.linear.x = y_joy*gear
        data.linear.y = data.linear.z = 0
        data.angular.x = data.angular.y = 0
        data.angular.z = x_joy*gear
        rospy.loginfo(data)
        rospy.loginfo(gear)
        pub.publish(data)

except KeyboardInterrupt:
    pass

pygame.quit()

