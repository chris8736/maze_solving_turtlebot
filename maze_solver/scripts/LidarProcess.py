#!/usr/bin/env python
#This node recieves /scan messages from the Lidar on the turtlebot, 
#and publishes the minimum overall and individual wedge scans
#(corresponding to the robot's front, front left and right,
#side left and right, and back left and right).
#It computes the wedge scans via python slicing.

import rospy
from sensor_msgs.msg import LaserScan
from maze_solver.msg import ProcessedScan
import sys
import numpy as np

#when i receive a scan, publish the closest overall and wedge scans
def callback(scan):
    ranges = map(lambda x: np.inf if x == 0 else x, scan.ranges) #replace null vals with inf
    msg = ProcessedScan()
    #get wedges via python slicing
    msg.back_left =     min(ranges[90:126])
    msg.left =          min(ranges[54:90])
    msg.front_left =    min(ranges[18:54])
    msg.front =         min(ranges[0:18] + ranges[342:])
    msg.front_right =   min(ranges[306:342])
    msg.right =         min(ranges[270:306])
    msg.back_right =    min(ranges[234:270])
    #get closest bearing and distance
    msg.min_bearing =   np.argmin(ranges)
    msg.min_distance =  ranges[msg.min_bearing]
    msg.right_distance =        ranges[270]
    pub.publish(msg)

#subscribe to scan, publish to process_scan
rospy.init_node('lidar_process')
pub = rospy.Publisher('/processed_scan', ProcessedScan, queue_size=1)
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
