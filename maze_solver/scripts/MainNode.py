#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Float64
from maze_solver.msg import ProcessedScan
import sys

#reset the values of the global twist
def stop_robot():
    main_twist.linear.x = 0
    main_twist.angular.z = 0

#update the global value of the last scan
def scan_callback(msg):
    global last_scan
    last_scan = msg

#pid attempt---
#def pid_callback(msg):
#    global last_control
#    last_control = msg.data

#state callback responds to FSM states from StateController, updating global twist
def callback(msg):

    global last_scan, main_twist, last_control
    state = msg.data
    print(state)
    if state == "find": #rotate and run towards the closest wall when it's in front
        stop_robot()
        if last_scan.min_bearing > 5 and last_scan.min_bearing < 355:
            main_twist.angular.z = .3
        else:
            main_twist.linear.x = .5
    elif state == "follow": #drive straight until state changes
        stop_robot()
        main_twist.linear.x = .3
        #pid attempt---
        #main_twist.angular.z = last_control
        #print(last_control)
    elif state == "rturn": #pivot around right wheel until state changes
        main_twist.angular.z = -1
        main_twist.linear.x = .1
    elif state == "lturn": #turn clockwise until state changes
        stop_robot()
        main_twist.angular.z = .5
    elif state == "win": #cease function
        stop_robot()

#global vars
last_scan = ProcessedScan()
last_control = 0
main_twist = Twist()

#init publishers and subscribers
rospy.init_node('main_node')
process_sub = rospy.Subscriber('/processed_scan', ProcessedScan, scan_callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
state_sub = rospy.Subscriber('/fsm_state', String, callback)

#pid attempt---
#pid_sub = rospy.Subscriber('/control_effort', Float64, pid_callback)

#continuously publish global twist
rate = rospy.Rate(10)
while not rospy.is_shutdown():
   cmd_vel_pub.publish(main_twist)
   rate.sleep()