#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from maze_solver.msg import MinScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import sys

def stop_robot():
   main_twist.linear.x = 0
   main_twist.angular.z = 0

#callback for odom info
def odom_callback(msg):

   global curr_yaw

   #update curr_units or init initial_units
   curr_q = msg.pose.pose.orientation
   curr_q_list = [curr_q.x, curr_q.y, curr_q.z, curr_q.w]
   (roll, pitch, yaw) = euler_from_quaternion(curr_q_list)
   curr_yaw = yaw

#when i receive a warning, update global twist, rotating in the opposite
#direction if necessary
def callback(msg):

   global state, last_lread, main_twist, curr_yaw, rate

   print(state)
   #print("Got Warning: " + str(msg.bearing) + ", " + str(msg.distance))
   
   if state == "find":
      main_twist.angular.z = 0
      if msg.distance < .3:
         if msg.bearing > 10:
            main_twist.angular.z = .3
         else:
            stop_robot()
            state = "align"
      else:
         if msg.bearing > 10:             #cutoff
            main_twist.angular.z = .3
         else:
            main_twist.linear.x = .2
         return
   
   elif state == "align":
      main_twist.angular.z = -.3
      if abs(msg.bearing - 90) < 10:
         stop_robot()
         last_lread = msg.ninety
         state = "follow"

   elif state == "follow":
      if msg.zero < .4:
         stop_robot()
         state = "rturn"
         return
      if msg.ninety > .9:
         stop_robot()
         state = "lturn"
         return
      elif msg.ninety < .15:            #todo rewrite logic
         main_twist.angular.z = -.1
      elif msg.ninety > .25:
         main_twist.angular.z = .1
      elif msg.ninety < last_lread:
         main_twist.angular.z = -.1
      elif msg.ninety > last_lread:
         main_twist.angular.z = .1
      main_twist.linear.x = .15
      last_lread = msg.ninety

   elif state == "lturn":
      init_yaw = curr_yaw
      target_yaw = (curr_yaw + 1.6)
      while target_yaw > 3.1415:
         target_yaw -= 6.283
      print(init_yaw, target_yaw)
      if curr_yaw < target_yaw:
         while curr_yaw < target_yaw:
            print(curr_yaw)
            cmd_vel_pub.publish(main_twist)
            main_twist.angular.z = .3
            rate.sleep()
      else:
         while not (curr_yaw > target_yaw and curr_yaw < init_yaw):
            print(curr_yaw)
            cmd_vel_pub.publish(main_twist)
            main_twist.angular.z = .3
            rate.sleep()
      stop_robot()
      state = "find"
      """
      main_twist.angular.z = .3
      #main_twist.linear.x = .5
      if msg.ninety < .3:
         stop_robot()
         state = "align" 
      """

   elif state == "rturn":
      main_twist = Twist()
      main_twist.angular.z = -1
      if msg.zero > .5:
         stop_robot()
         state = "follow"

state = "find"
last_lread = 0
main_twist = Twist()
curr_yaw = 0

#init cmd_vel publisher
rospy.init_node('main_node')
sub = rospy.Subscriber('/min_scan', MinScan, callback)
odom_sub = rospy.Subscriber('/odom', Odometry, odom_callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

#continuously publish global twist
while not rospy.is_shutdown():
   cmd_vel_pub.publish(main_twist)
   rate.sleep()