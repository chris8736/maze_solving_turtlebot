#!/usr/bin/env python

import rospy
from maze_solver.msg import ProcessedScan
from std_msgs.msg import String
from std_msgs.msg import Float64
import sys

#given a processed scan, publish the state corresponding to the pattern matched
def callback(msg):
    global state
    #exit if done
    if state == "win":                 
        return
    #one condition to exit out of find
    if state == "find":             
        if msg.front < max_dist:
            state = "lturn"
    #detected end of maze
    elif msg.min_distance > .75:
        state = "win"
    # nothing 
    elif msg.front > max_dist and msg.front_left > max_dist and msg.front_right > max_dist:
        state = "rturn"
    # front 
    elif msg.front < max_dist and msg.front_left > max_dist and msg.front_right > max_dist:
        state = "lturn"
    # front right  
    elif msg.front > max_dist and msg.front_left > max_dist and msg.front_right < max_dist:
        state = "follow"
    # front left 
    elif msg.front > max_dist and msg.front_left < max_dist and msg.front_right > max_dist:
        state = "rturn"
    # front and front right 
    elif msg.front < max_dist and msg.front_left > max_dist and msg.front_right < max_dist:
        state = "lturn" 
    # front and front left 
    elif msg.front < max_dist and msg.front_left < max_dist and msg.front_right > max_dist:
        state = "lturn"
    # front and front left and front right 
    elif msg.front < max_dist and msg.front_left < max_dist and msg.front_right < max_dist:
        state = "lturn" 
    # front left and front right 
    elif msg.front > max_dist and msg.front_left < max_dist and msg.front_right < max_dist:
        state = "rturn"
    else:
        state = "something went wrong"
    fsm_state_pub.publish(state)
    state_pub.publish(msg.right_distance)
    setpoint_pub.publish(max_dist/2)

state = "find"
max_dist = .4

rospy.init_node('state_controller')
sub = rospy.Subscriber('/processed_scan', ProcessedScan, callback)
fsm_state_pub = rospy.Publisher('/fsm_state', String, queue_size=1)

#pid attempt---
#state_pub = rospy.Publisher('/state', Float64, queue_size=1)
#setpoint_pub = rospy.Publisher('/setpoint', Float64, queue_size=1)

rospy.spin()