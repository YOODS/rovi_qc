#!/usr/bin/python

import time
from subprocess import Popen
import cv2
import numpy as np
import roslib
import rospy
from std_msgs.msg import Bool
from rovi.msg import Floats
from rospy.numpy_msg import numpy_msg

def cb_ps(msg): #callback of ps_floats
  global cbtime,tamax,tamin,tacount,pcarray
  pc=np.reshape(msg.data,(-1,3))
  pcarray.append(len(pc))
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

def cb_Y1(msg):
  global ycam
  if msg.data is False: ycam=False

########################################################
rospy.init_node("maxrate",anonymous=True)

cbtime=time.time()
tamax=0
tamin=0
tacount=0
ycam=True
rospy.Subscriber("/rovi/ps_floats",numpy_msg(Floats),cb_ps)
rospy.Subscriber("/rovi/Y1",Bool,cb_Y1)
pcarray=[]

proc=Popen("rostopic pub -r10 /rovi/X1 std_msgs/Bool True".strip().split(" ") )

while not rospy.is_shutdown():
  if time.time()-cbtime>10:
    print "cb_ps timeout"
    break
  if ycam is False:
    print "YCAM not normal"
    break
  if len(pcarray)>10:
    pcmin=min(pcarray[:-1])
    pcmax=max(pcarray[:-1])
    pcave=sum(pcarray[:-1])/len(pcarray[:-1])
    if pcmax>pcave*1.2: continue
    if pcmin<pcave*0.8: continue
    if pcarray[-1]<pcave*0.5:
      print "Too few points"
      break
    pcarray.pop(0)
rospy.sleep(1)

proc.terminate()
rospy.spin()

