
import rospy
from geometry_msgs.msg import Twist
import pygame
import time


pygame.init()
pygame.joystick.init()

joyStick = pygame.joystick.Joystick(0)
joyStick.init()

x_value = 0.00
z_value = 0.00


obj = Twist()

def talker(x,z):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    obj.linear.x = x
    obj.angular.z = z
    #objz.angular.z = str(z)
    rospy.loginfo(obj)
    pub.publish(obj)
    rate.sleep()

if __name__ == '__main__':
    while True:
        try:
            for event in pygame.event.get():
                if(event.axis==0):
                    x_value = joyStick.get_axis(0)  #gets the position of the joystick on x axis
                elif(event.axis==1):
                    z_value = -joyStick.get_axis(1)
                else:
                    print('not on the axis')
                x_pwm = x_value
                z_pwm = z_value
                print('pwm',x_pwm,z_pwm)
                talker(x_pwm,z_pwm)
        except KeyboardInterrupt:
            break
    talker(0,0)
