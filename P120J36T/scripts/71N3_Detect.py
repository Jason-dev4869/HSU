#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge

class LineDetector:
    def __init__(self):
        rospy.init_node('line_detector')
        self.bridge = CvBridge()
        
        self.sub = rospy.Subscriber('/camera/image_raw', Image, self.callback)
        self.pub_error = rospy.Publisher('/line/error', Float32, queue_size=1)
        self.pub_debug = rospy.Publisher('/line/debug_image', Image, queue_size=1)

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        roi = frame[int(h * 0.6):h, :]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # --- Đổi range màu theo màu line thực tế của bạn ---
        # Line vàng:
        lower = np.array([20, 100, 100])
        upper = np.array([35, 255, 255])
        # Line trắng: lower=[0,0,180], upper=[180,30,255]
        # Line đen:  lower=[0,0,0],   upper=[180,255,50]

        mask = cv2.inRange(hsv, lower, upper)
        
        # Morphology để loại noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Tìm centroid của line
        M = cv2.moments(mask)
        if M['m00'] > 500:  # đủ pixel line
            cx = int(M['m10'] / M['m00'])
            error = (cx - w / 2) / (w / 2)  # normalize [-1, 1]
            self.pub_error.publish(Float32(error))

            # Debug visualization
            cv2.circle(roi, (cx, roi.shape[0]//2), 10, (0,255,0), -1)
            cv2.line(roi, (w//2, 0), (w//2, roi.shape[0]), (255,0,0), 2)
        else:
            # Mất line — publish NaN để controller xử lý
            self.pub_error.publish(Float32(float('nan')))

        self.pub_debug.publish(self.bridge.cv2_to_imgmsg(roi, 'bgr8'))

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    LineDetector().run()