#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from maze_solver.msg import MinScan
import sys

#when i receive a warning, update global twist, rotating in the opposite
#direction if necessary
def callback(msg):

   global lock
   print("Got Warning: " + str(msg.bearing) + ", " + str(msg.distance))
   if not lock:
      if msg.distance < .3:
         lock = True
      else:
         main_twist.linear.x = .2
         return

   if (abs(msg.bearing - 90) < 10):
      main_twist.linear.x = .2
   else:
      main_twist.linear.x = 0
      if msg.bearing > 90 and msg.bearing < 270:
         main_twist.angular.z = .3
      else:
         main_twist.angular.z = -.3

   """
   main_twist.linear.x = .1
   if main_twist.angular.z > -.5 and msg.bearing < 90:
      main_twist.angular.z += -.02
   elif main_twist.angular.z > -.5 and msg.bearing > 90 and msg.bearing <:
      main_twist.angular.z += .02
      """

#init cmd_vel publisher
rospy.init_node('main_node')
sub = rospy.Subscriber('/min_scan', MinScan, callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

lock = False
main_twist = Twist()

#continuously publish global twist
while not rospy.is_shutdown():
   cmd_vel_pub.publish(main_twist)
   rate.sleep()