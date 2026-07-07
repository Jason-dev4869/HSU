#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lidar_avoidobj.py
==================
Node DOC LAP chi test LiDAR obstacle avoidance, KHONG dung camera/YOLO.

QUAN TRONG: JetRacer la xe kieu ACKERMANN (banh truoc danh lai), KHONG THE
xoay tai cho nhu xe 2 banh differential drive. Moi lenh ne vat can PHAI
luon kem theo linear.x khac 0 (tien hoac lui), goc lai duoc chuyen sang
angular.z qua dung cong thuc Ackermann:
    R = WHEELBASE / tan(delta)
    angular_z = linear_speed / R
Neu chi gui angular.z ma linear.x=0, xe se KHONG DI CHUYEN/QUAY duoc gi ca
(day la nguyen nhan ban dau xe bi "ket" mai o 1 khoang cach, khong ne duoc).

Hanh vi:
  - CRUISE: khong co vat can phia truoc trong OBSTACLE_DIST -> di thang.
  - AVOID (vat can 0.30-0.50m phia truoc): tien cham (AVOID_CREEP_SPEED) +
    danh lai het ve phia thoang hon (MAX_STEER_ANGLE), xe se VONG tranh vat.
  - REVERSE_AVOID (vat can <0.30m phia truoc, qua gan de tien): lui cham
    (AVOID_REVERSE_SPEED) + danh lai, NHUNG chi khi phia SAU an toan
    (>REAR_SAFE_DIST). Neu ca truoc va sau deu bi ket -> dung han.

Output: geometry_msgs/Twist -> /cmd_vel
Input: sensor_msgs/LaserScan -> /scan
"""

import numpy as np
import json
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# Ackermann geometry (giong cam_manfollow.py / manfollow_avoidobj.py)
WHEELBASE = 0.16
MAX_STEER_ANGLE = np.deg2rad(25)

CRUISE_SPEED = 0.30           # m/s khi di thang, khong co vat can
CAUTION_SPEED = 0.18          # m/s trong vung canh giac (gan vat nhung chua can ne)
AVOID_CREEP_SPEED = 0.18      # m/s tien cham khi vua tien vua vong tranh
AVOID_REVERSE_SPEED = -0.15   # m/s lui cham khi qua gan, can lui+quay

# SAFETY_MARGIN: LiDAR 2D chi quet 1 mat phang ngang, KHONG thay duoc vat thap
# hon do cao lap dat (chan ghe, chan ban...). Cong them margin nay vao moi
# nguong khoang cach de "du phong" cho phan khong nhin thay duoc co the
# nhoi ra xa hon phan than vat ma LiDAR thay (vi du: than ghe LiDAR thay duoc,
# nhung chan ghe co the chia ra ngoai pham vi than ghe).
SAFETY_MARGIN = 0.15          # m

OBSTACLE_DIST = 0.50 + SAFETY_MARGIN    # m - bat dau vong tranh (tien + danh lai)
SAFE_STOP_DIST = 0.30 + SAFETY_MARGIN   # m - qua gan de tien, chuyen sang lui
CAUTION_DIST = 0.90 + SAFETY_MARGIN     # m - vung canh giac, giam toc truoc khi can ne han
REAR_SAFE_DIST = 0.30 + SAFETY_MARGIN   # m - phia sau can it nhat khoang nay moi cho lui

FRONT_HALF_ANGLE_DEG = 35
REAR_HALF_ANGLE_DEG = 30


def ackermann_angular(speed, delta):
    """Chuyen (toc do, goc lai banh truoc) -> angular.z theo dung Ackermann."""
    if abs(delta) < 1e-4 or abs(speed) < 1e-3:
        return 0.0
    R = WHEELBASE / np.tan(delta)
    return speed / R


class LidarAvoidDemo(object):
    def __init__(self):
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.debug_pub = rospy.Publisher('/lidar_avoid_debug', String, queue_size=1)
        rospy.Subscriber('/scan', LaserScan, self.scan_cb, queue_size=1)
        rospy.loginfo("lidar_avoidobj da khoi dong (Ackermann). CRUISE=%.2f OBSTACLE_DIST=%.2f",
                      CRUISE_SPEED, OBSTACLE_DIST)

    def scan_cb(self, scan):
        ranges = np.array(scan.ranges)
        angles = scan.angle_min + np.arange(len(ranges)) * scan.angle_increment
        angles_deg = np.degrees(angles)

        front_mask = np.abs(angles_deg) <= FRONT_HALF_ANGLE_DEG
        rear_mask = np.abs(np.abs(angles_deg) - 180) <= REAR_HALF_ANGLE_DEG

        front_ranges = ranges[front_mask]
        front_angles = angles[front_mask]
        valid_front = np.isfinite(front_ranges) & (front_ranges > 0.01)

        rear_ranges = ranges[rear_mask]
        valid_rear = np.isfinite(rear_ranges) & (rear_ranges > 0.01)
        rear_min_dist = float(np.min(rear_ranges[valid_rear])) if np.any(valid_rear) else float('inf')

        if not np.any(valid_front):
            speed, delta = CRUISE_SPEED, 0.0
            min_dist = None
            state = "CRUISE (khong thay vat can)"
        else:
            front_ranges = front_ranges[valid_front]
            front_angles = front_angles[valid_front]
            min_dist = float(np.min(front_ranges))

            left_mean = np.mean(front_ranges[front_angles > 0]) if np.any(front_angles > 0) else 0
            right_mean = np.mean(front_ranges[front_angles < 0]) if np.any(front_angles < 0) else 0
            # delta > 0: danh lai trai. Vat can ben nao thoang hon thi quay ve ben do.
            steer_toward_open = MAX_STEER_ANGLE if left_mean > right_mean else -MAX_STEER_ANGLE

            if min_dist < SAFE_STOP_DIST:
                if rear_min_dist < REAR_SAFE_DIST:
                    speed, delta = 0.0, 0.0
                    state = "STOP (ket ca truoc %.2fm va sau %.2fm)" % (min_dist, rear_min_dist)
                else:
                    speed = AVOID_REVERSE_SPEED
                    delta = steer_toward_open
                    state = "REVERSE_AVOID (truoc %.2fm, lui+quay)" % min_dist
            elif min_dist < OBSTACLE_DIST:
                speed = AVOID_CREEP_SPEED
                delta = steer_toward_open
                state = "AVOID (%.2fm, tien+vong %s)" % (
                    min_dist, "trai" if delta > 0 else "phai")
            elif min_dist < CAUTION_DIST:
                # Vung canh giac: gan vat (co the thay 1 phan, ben duoi co the con
                # phan khong thay duoc) -> giam toc, KHONG danh lai, tang thoi
                # gian phan ung cho lan quet sau.
                speed, delta = CAUTION_SPEED, 0.0
                state = "CAUTION (%.2fm, giam toc de phong)" % min_dist
            else:
                speed, delta = CRUISE_SPEED, 0.0
                state = "CRUISE (%.2fm, an toan)" % min_dist

        angular = ackermann_angular(speed, delta)

        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

        rospy.loginfo_throttle(1, "LIDAR_AVOID: %s | speed=%.2f delta=%.1f* angular=%.2f",
                                state, speed, np.degrees(delta), angular)
        self.debug_pub.publish(String(data=json.dumps({
            "state": state,
            "min_front_dist": min_dist,
            "min_rear_dist": rear_min_dist if rear_min_dist != float('inf') else None,
            "speed": speed,
            "steer_deg": float(np.degrees(delta)),
            "angular": angular,
        })))


if __name__ == '__main__':
    rospy.init_node('lidar_avoidobj')
    LidarAvoidDemo()
    rospy.spin()