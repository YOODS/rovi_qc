#!/usr/bin/python

import cv2
import numpy as np
from scipy import fftpack
import roslib
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
#import matplotlib.pyplot as plt

def fft(img0):
  fimg = np.fft.fft2(img0)
#  fimg = fftpack.fft2(img0)
#  fimg = np.fft.fftshift(fimg)
#  fimg[np.where(np.abs(fimg)<1)]=1
#  fimg = np.log(np.abs(fimg))
  return np.abs(fimg)

def hpf(img,thres):
  h = img.shape[0]
  w = img.shape[1]
  xr = int(w*thres)
  img1 = img[:,0:xr]
  img2 = img[:,w-xr:w]
  m1=np.mean(img1)
  m2=np.mean(img2)
#  x = np.arange(0,len(ras)).astype(float)
#  y = ras
#  plt.plot(x, y)
#  plt.show()
  return (m1+m2)/2

lpf=[]

def cb_image(rosimg):
  global sb_im,lpf
  sb_im.unregister()
  try:
    img0 = bridge.imgmsg_to_cv2(rosimg, "mono8")
  except CvBridgeError, e:
    print e
    return
  h=img0.shape[0]
  w=img0.shape[1]
  im0=img0[h/2-4:h/2+4,:]
  sp0=fft(im0)
  v=hpf(sp0,0.02)
  lpf.append(v)
  if len(lpf)==10:
    report=String()
    focus=int(np.mean(np.array(lpf)))
    iave=int(np.mean(im0))
    bave=int(np.mean(im0[np.where(im0<=iave)]))
    wave=int(np.mean(im0[np.where(im0>=iave)]))
    report.data='focus='+str(focus)+' brightness=('+str(iave)+','+str(bave)+','+str(wave)+')'
    pb_report.publish(report)
    lpf.pop(0)
  sb_im=rospy.Subscriber('image_raw',Image,cb_image)


###############################################################
if __name__ == "__main__":
  rospy.init_node('fft',anonymous=True)
  bridge=CvBridge()
  sb_im=rospy.Subscriber('image_raw',Image,cb_image)
  pb_report=rospy.Publisher('fft/report',String,queue_size=1)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
