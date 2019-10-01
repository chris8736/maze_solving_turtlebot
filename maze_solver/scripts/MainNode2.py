#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from maze_solver.msg import MinScan
import sys

def stop_robot():
   main_twist.linear.x = 0
   main_twist.angular.z = 0

#when i receive a warning, update global twist, rotating in the opposite
#direction if necessary
def callback(msg):

   global state, last_lread

   print(state)
   #print("Got Warning: " + str(msg.bearing) + ", " + str(msg.distance))
   
   if state == "find":
      main_twist.angular.z = 0
      if msg.distance < .3:
         stop_robot()
         state = "align"
      else:
         if msg.bearing > 10:             #cutoff
            main_twist.angular.z = .3
         else:
            main_twist.linear.x = .2
         return
   
   if state == "align":
      main_twist.angular.z = -.3
      if abs(msg.bearing - 90) < 10:
         stop_robot()
         last_lread = msg.ninety
         state = "follow"

   if state == "follow":
      """
      if msg.bearing == 0:
         stop_robot()
         state = "rturn"
         return
      """
      if msg.ninety > .5:
         stop_robot()
         state = "lturn"
         return
      elif msg.ninety < .2:
         main_twist.angular.z = -.1
      elif msg.ninety > .3:
         main_twist.angular.z = .1
      elif msg.ninety < last_lread:
         main_twist.angular.z = -.1
      elif msg.ninety > last_lread:
         main_twist.angular.z = .1
      main_twist.linear.x = .1
      last_lread = msg.ninety

   if state == "lturn":
      main_twist.angular.z = .4
      main_twist.linear.x = .1
      if msg.ninety < .3:
         stop_robot()
         state = "follow"

   if state == "rturn":
      pass

#init cmd_vel publisher
rospy.init_node('main_node')
sub = rospy.Subscriber('/min_scan', MinScan, callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

state = "find"
last_lread = 0
main_twist = Twist()

#continuously publish global twist
while not rospy.is_shutdown():
   cmd_vel_pub.publish(main_twist)
   rate.sleep()