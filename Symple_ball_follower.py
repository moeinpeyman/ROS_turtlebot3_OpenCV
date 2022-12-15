#!/usr/bin/env python


from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

class TakePhoto:
    def __init__(self):

        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=rospy.Rate(1)
        self.rot=Twist()

        self.cx=0
        self.cy=0

        self.bridge = CvBridge()
        self.image_received = False

        # Connect image topic
        img_topic = "/camera/rgb/image_raw"
        self.image_sub = rospy.Subscriber(img_topic, Image, self.callback)

        # Allow up to one second to connection
        rospy.sleep(1)

    def callback(self, data):

        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image
        #self.show_image(cv_image)
        self.find_object(cv_image)
        self.move_to_object()

    def show_image(self,img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)
        

    def find_object(self,img):
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_frame = cv2.resize(hsv_frame,(640,300))

        low_H=0
        low_S=200
        low_V=50
        high_H=180
        high_S=255
        high_V=255


        mask_frame=cv2.inRange(hsv_frame, (low_H, low_S, low_V), (high_H, high_S, high_V))
        cv2.imshow("mask",mask_frame)
        contours, hierarchy = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #_, contours, _= cv2.findContours(mask_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        X,Y,W,H=0,0,0,0


        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            if(area > 30):
                
                x, y, w, h = cv2.boundingRect(contour)
                if(w*h>W*H):
                    X, Y, W, H= x, y, w, h

        img = cv2.rectangle(img, (X, Y),(X +W, Y + H),(0, 0, 255), 2)
        self.cx =X
        self.cy = Y


        print(self.cx)
        cv2.imshow("window", img)
        cv2.waitKey(3)

    def move_to_object(self):
        
        if(self.cx==0):
            text="searching"
            self.rot.angular.z=0.4
            self.rot.linear.x=0

        else:
        
            obj_x=self.cx-320

            if(obj_x<=30 and obj_x>=-30):
                text="straight"
                self.rot.angular.z=0
                self.rot.linear.x=0.2
            elif(obj_x>30):
                text="Left"
                self.rot.angular.z=-0.1
                self.rot.linear.x=0
            elif(obj_x<-30):
                text="Right"
                self.rot.angular.z=0.1
                self.rot.linear.x=0


        self.pub.publish(self.rot)
        print(text)

    def stop(self):
        self.rot.angular.z=0
        self.rot.linear.x=0
        self.pub.publish(self.rot)
        print(text)


if __name__ == '__main__':

    # Initialize
    rospy.init_node('take_photo', anonymous=False)
    camera = TakePhoto()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)
        rospy.spin()

    camera.stop

