#!/usr/bin/env python

import rospy
from beginner_tutorials.srv import * 

def handle_req(data):
    return AddTwoIntsResponse(data.a + data.b)

def main():
    rospy.init_node('add_two_nodes_server')
    s = rospy.Service('add_two_ints', AddTwoInts, handle_req) 
    rospy.spin()

if __name__ == '__main__':
    main()
