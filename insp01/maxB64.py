#!/usr/bin/python

import time
from subprocess import Popen
import cv2
import numpy as np
import roslib
import rospy
from std_msgs.msg import String
from rospy.numpy_msg import numpy_msg
import base64

def cb_ps(msg): #callback of ps_floats
  global cbtime,tamax,tamin,tacount
  pc=np.frombuffer(base64.b64decode(msg.data),dtype=np.float32).reshape((-1,3))
  tn=time.time()
  ta=tn-cbtime
  if tacount<5:
    tamax=ta
    tamin=ta
    print tacount,len(pc),ta
  else:
    if tamax<ta: tamax=ta
    if tamin>ta: tamin=ta
    print tacount,len(pc),ta,tamin,tamax
  cbtime=tn
  tacount=tacount+1
  return


########################################################
rospy.init_node("cropper",anonymous=True)

cbtime=time.time()
tamax=0
tamin=0
tacount=0
sub=rospy.Subscriber("/rovi/ps_base64",String,cb_ps)

proc=Popen("rostopic pub -r1 /rovi/X1 std_msgs/Bool True".strip().split(" ") )

while not rospy.is_shutdown():
  if time.time()-cbtime>5: break
  rospy.sleep(1)

print "cb_ps timeout"
proc.terminate()
sub.unregister()
rospy.spin()


