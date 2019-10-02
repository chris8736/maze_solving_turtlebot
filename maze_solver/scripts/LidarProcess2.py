#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from maze_solver.msg import ProcessedScan
import sys
import numpy as np

#when i receive a scan, publish the bearing and data of the minimum scan
def callback(scan):
    ranges = map(lambda x: np.inf if x == 0 else x, scan.ranges) #replace null vals with inf
    msg = ProcessedScan()
    msg.back_left =     min(ranges[90:126])
    msg.left =          min(ranges[54:90])
    msg.front_left =    min(ranges[18:54])
    msg.front =         min(ranges[0:18] + ranges[342:])
    msg.front_right =   min(ranges[306:342])
    msg.right =         min(ranges[270:306])
    msg.back_right =    min(ranges[234:270])
    pub.publish(msg)

#subscribe to scans, publish to warnings
rospy.init_node('lidar_process')
pub = rospy.Publisher('/processed_scan', ProcessedScan, queue_size=1)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()