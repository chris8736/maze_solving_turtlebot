#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import sys
import numpy as np
import time

#when i receive a scan, print its ranges
def callback(scan):
    ranges = map(lambda x: np.inf if x == 0 else x, scan.ranges) #replace null vals with inf
    print("-----")
    for i in ranges:
        print(i)
    time.sleep(5)

#subscribe to scans, publish to warnings
rospy.init_node('lidar_process')
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()