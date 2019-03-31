#!/usr/bin/python

import numpy as np
import roslib
import rospy
from std_msgs.msg import String

score_L='---'
score_R='---'

def cb_left(msg):
  global score_L,score_R
  score_L=msg.data
  print score_L,score_R

def cb_right(msg):
  global score_L,score_R
  score_R=msg.data
  print score_L,score_R

###############################################################
if __name__ == "__main__":
  rospy.init_node('fft_logger',anonymous=True)
  sb_left=rospy.Subscriber('left/fft/report',String,cb_left)
  sb_right=rospy.Subscriber('right/fft/report',String,cb_right)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
