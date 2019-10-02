#!/usr/bin/env python

"""
todo: this is a copy of MainNode2; refactor into pure state control.
"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from maze_solver.msg import ProcessedScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion
import sys

def callback(msg):
    if msg.left < max_dist:
        state = "follow"
    elif msg.front < max_dist:
        state = "right"
    else:
        state = "find"
    #msg.front > d and msg.front_left > d and msg.front_right > d:
        #state = "find"
    pub.publish(state)

state = "find"
max_dist = .3

rospy.init_node('state_controller')
sub = rospy.Subscriber('/processed_scan', ProcessedScan, callback)
pub = rospy.Publisher('/state', String, queue_size=1)
rate = rospy.Rate(10)

rospy.spin()