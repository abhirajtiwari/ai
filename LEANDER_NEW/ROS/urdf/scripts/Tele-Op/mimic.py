import rospy
from geometry_msgs.msg import Twist
import time
from multiprocessing import Process


f = open("x_coordinate_only.txt", "r")
g = open("y_coordinate_only.txt", "r")
h = open("time_only.txt",'r')

ob1 = Twist()

ob1.linear.y = 0
ob1.linear.z = 0

ob1.angular.x = 0
ob1.angular.y = 0



def linearity():

    f1 = f.readlines()
    g1 = g.readlines()
    h1 = h.readlines()

    for reader, reading , timing in zip(f1, g1, h1):

        reader = float(reader)
        ob1.linear.x = reader

        reading = float(reading)
        ob1.angular.z = reading

        timing = float(timing)

        pub.publish(ob1)

        print(reader,reading,timing)

        time.sleep(timing)





def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.


    while not rospy.is_shutdown():

        linearity()

        rospy.sleep(0.01)

    # spin() simply keeps python from exiting until this node is stopped


if __name__ == '__main__':
    try:
        global ob1
        pub = rospy.Publisher('champ', Twist, queue_size=10)
        rospy.init_node('Communication', anonymous=True)
        rate = rospy.Rate(1)  # 1hz

        rospy.loginfo(ob1)

        listener()

    except rospy.ROSInterruptException:
        f.close()

