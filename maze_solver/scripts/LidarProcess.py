#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from maze_solver.msg import MinScan
import sys
import numpy as np

#when i receive a scan, publish the bearing and data of the minimum scan
def callback(scan):
    ranges = map(lambda x: np.inf if x == 0 else x, scan.ranges) #replace null vals with inf
    bearing = np.argmin(ranges)
    min_range_ahead = ranges[bearing]
    msg = MinScan()
    msg.bearing = bearing
    msg.distance = ranges[bearing]
    msg.ninety = ranges[90]
    cmd_vel_pub.publish(msg)

#subscribe to scans, publish to warnings
rospy.init_node('lidar_process')
cmd_vel_pub = rospy.Publisher('/min_scan', MinScan, queue_size=1)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()