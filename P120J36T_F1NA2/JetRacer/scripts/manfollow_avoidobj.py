#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manfollow_avoidobj.py
========================
JetRacer ROS node - Person Following + Obstacle Avoidance (BAN GOP HOAN CHINH)

Gop tu 2 file da test rieng le on dinh:
  - cam_manfollow.py   (Camera + YOLOv3-tiny qua TensorRT + giu khoang cach LiDAR)
  - lidar_avoidobj.py  (Ne vat can bang LiDAR, Ackermann steering)

=== XU LY MAU THUAN KHI CA 2 CUNG DOI QUYEN DIEU KHIEN ===
Toc do: KHONG mau thuan thuc su -- da co thu tu uu tien ro rang (an toan LiDAR
  luon de len toc do theo nguoi: dung/lui neu qua gan).
Lai (steer): day la mau thuan THAT -- theo nguoi can lai CAN GIUA nguoi, ne vat
  can can lai VE PHIA THOANG HON. Khong the lam ca 2 cung luc.

Giai phap: uoc luong GOC (bearing) cua vat can gan nhat qua LiDAR, so sanh voi
huong cua nguoi (uoc luong tu offset camera, gia dinh camera/LiDAR cung huong
phia truoc). Neu lech goc nhieu -> vat can KHAC nguoi (ban, tuong...) -> uu
tien ne (override lai + toc do). Neu trung huong -> vat can DUNG LA nguoi dang
theo -> giu logic cu (lai theo nguoi, toc do/an toan LiDAR xu ly khoang cach).

Khi SEARCHING (mat track, dang lui ve vi tri cu): KHONG kich hoat logic ne/lan
truong (CRUISE) cua lidar_avoidobj -- vi do la hanh vi "tu lai di tham do" khi
khong co nguoi de theo, khong phu hop luc dang co tim lai 1 nguoi cu the. Chi
giu hanh vi lui an toan (co check phia sau) nhu da co.
"""

import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_THREAD_LIMIT', '1')

import sys
TENSORRT_DEMOS_DIR = os.path.expanduser('~/catkin_ws/src/human_following/tensorrt_demos')
sys.path.append(TENSORRT_DEMOS_DIR)

# QUAN TRONG: utils.yolo_with_plugins load './plugins/libyolo_layer.so' theo duong
# dan TUONG DOI ngay luc IMPORT module -> phai chdir TRUOC dong import nay.
os.chdir(TENSORRT_DEMOS_DIR)

import pycuda.driver as cuda
from utils.yolo_with_plugins import TrtYOLO

import json
import pickle
import time
import numpy as np
import cv2
cv2.setNumThreads(1)

import rospy
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

from insightface.app import FaceAnalysis


# ================= CONFIG =================
PERSON_CLASS_ID = 0  # COCO 'person'

FACE_SIM_THRESHOLD = 0.42
IOU_MATCH_THRESHOLD = 0.20
HSV_SIM_THRESHOLD = 0.55
LOST_FRAMES_LIMIT = 15
REID_INTERVAL = 15
USE_FACE_ID = True  # False: lock vao nguoi GAN NHAT, khong can khop khuon mat

YOLO_INPUT_SIZE = (416, 416)
YOLO_CONF_THRES = 0.25
YOLO_NMS_THRES = 0.4

# ---- Steering (Ackermann) ----
MAX_STEER = 0.34
WHEELBASE = 0.16
MAX_STEER_ANGLE = np.deg2rad(25)
STEER_DEADBAND = 0.12
STEER_GAIN = 0.32

# Toc do TU DIEU CHINH theo goc lai: re gat -> giam toc, di thang -> toc binh thuong.
TURN_SLOWDOWN_RATIO = 0.6

# He so SCALE CUOI CUNG cho angular.z truoc khi gui xuong chassis driver -- chinh
# THUC NGHIEM, doc lap voi STEER_GAIN/Ackermann. Driver jetracer tu co he so PWM
# rieng; neu servo van re lo du da giam STEER_GAIN -> giam tiep so nay.
SERVO_ANGULAR_SCALE = 0.5

# Lam muot lenh dieu khien (low-pass filter)
SMOOTH_ALPHA_STEER = 0.3
SMOOTH_ALPHA_SPEED = 0.3

# ---- Khi mat track: lui thang ve vi tri cu (KHONG tu lai di tim/lan truong) ----
SEARCH_RECOVERY_SPEED = -0.30
SEARCH_RECOVERY_MAX_FRAMES = 30

# ---- Giu khoang cach voi NGUOI bang LiDAR ----
TARGET_FOLLOW_DIST = 0.45      # m - giua vung dung 0.30-0.60m
FOLLOW_DEADBAND = 0.15         # m - +-0.15 quanh 0.45 = dung tai 0.30-0.60m
DIST_SPEED_GAIN = 1.2
MAX_SPEED = 0.3
MIN_SPEED = -0.30
NO_LIDAR_FALLBACK_SPEED = 0.25

# ---- Ne VAT CAN KHAC (khong phai nguoi dang theo) ----
CRUISE_SPEED = 0.30
CAUTION_SPEED = 0.18
AVOID_CREEP_SPEED = 0.18
AVOID_REVERSE_SPEED = -0.15

# SAFETY_MARGIN: LiDAR 2D chi quet 1 mat phang ngang, KHONG thay duoc vat thap
# hon do cao lap dat (chan ghe, chan ban...). Cong them margin de du phong.
SAFETY_MARGIN = 0.15

OBSTACLE_DIST = 0.50 + SAFETY_MARGIN    # m - bat dau de y / vong tranh
SAFE_STOP_DIST = 0.30 + SAFETY_MARGIN   # m - qua gan phia truoc -> dung/chuyen lui
CAUTION_DIST = 0.90 + SAFETY_MARGIN     # m - vung canh giac, giam toc nhe
REAR_SAFE_DIST = 0.30 + SAFETY_MARGIN   # m - phia sau can it nhat khoang nay moi cho lui

FRONT_HALF_ANGLE_DEG = 35
REAR_HALF_ANGLE_DEG = 30

# ---- Phan biet "vat can = nguoi dang theo" vs "vat can KHAC" ----
CAMERA_FOV_HALF_DEG = 35   # uoc luong goc nhin ngang cua camera (gan dung voi FRONT_HALF_ANGLE_DEG)
ALIGN_TOLERANCE_DEG = 20   # lech duoi nguong nay -> coi nhu cung huong (la chinh nguoi)


def imgmsg_to_cv2(msg):
    arr = np.frombuffer(msg.data, dtype=np.uint8)
    if msg.encoding in ('bgr8', 'rgb8'):
        img = arr.reshape(msg.height, msg.width, 3)
        if msg.encoding == 'rgb8':
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
    elif msg.encoding == 'mono8':
        gray = arr.reshape(msg.height, msg.width)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    else:
        raise ValueError("Encoding chua ho tro: {}".format(msg.encoding))


def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    denom = areaA + areaB - inter
    if denom <= 0:
        return 0.0
    return inter / float(denom)


def crop_bbox(img, bbox):
    x1, y1, x2, y2 = [int(v) for v in bbox]
    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return None
    return img[y1:y2, x1:x2]


def hsv_hist(img, bbox):
    crop = crop_bbox(img, bbox)
    if crop is None or crop.size == 0:
        return None
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [30, 32], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist


def hist_similarity(h1, h2):
    if h1 is None or h2 is None:
        return 0.0
    return cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)


def clip(v, lo, hi):
    return max(lo, min(hi, v))


def ackermann_angular(speed, delta):
    """Chuyen (toc do, goc lai banh truoc) -> angular.z theo dung Ackermann."""
    if abs(delta) < 1e-4 or abs(speed) < 1e-3:
        return 0.0
    R = WHEELBASE / np.tan(delta)
    return speed / R


# ================= PERSON DETECTOR (YOLOv3-tiny qua TensorRT) =================
class PersonDetector(object):
    """Tu tao CUDA context rieng (khong dung pycuda.autoinit), truyen vao
    TrtYOLO de class do tu push()/pop() dung luc detect() - an toan vi
    image_cb cua ROS chay tren thread khac thread khoi tao."""

    def __init__(self, model_name='yolov3-tiny', category_num=80):
        cuda.init()
        self.cuda_ctx = cuda.Device(0).make_context()
        self.trt_yolo = TrtYOLO(model_name, category_num, letter_box=False,
                                 cuda_ctx=self.cuda_ctx)
        rospy.loginfo("YOLO Backend : TensorRT (engine=%s)", model_name)

    def detect(self, frame):
        boxes, confs, clss = self.trt_yolo.detect(frame, YOLO_CONF_THRES)
        person_boxes = []
        best_person_conf = 0.0
        for box, conf, cls in zip(boxes, confs, clss):
            if int(cls) != PERSON_CLASS_ID:
                continue
            person_boxes.append([float(box[0]), float(box[1]), float(box[2]), float(box[3])])
            if conf > best_person_conf:
                best_person_conf = float(conf)
        if person_boxes:
            rospy.loginfo_throttle(3, "YOLO(TensorRT): tim thay %d person, best_conf=%.4f",
                                    len(person_boxes), best_person_conf)
        return person_boxes
    # Don dep CUDA context qua rospy.on_shutdown() trong JetRacerFollower._cleanup().


# ================= FACE-ID MATCHER (InsightFace buffalo_sc, tuy chon) =================
class FaceIDMatcher(object):
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            raise FileNotFoundError("Khong tim thay faces.pkl tai: {}".format(db_path))
        with open(db_path, 'rb') as f:
            raw_db = pickle.load(f)
        self.database = {name: np.array(emb) for name, emb in raw_db.items()}
        rospy.loginfo("Face DB loaded: %d nguoi", len(self.database))
        self.app = FaceAnalysis(name='buffalo_sc')
        self.app.prepare(ctx_id=0)

    def match_in_bbox(self, frame, bbox):
        crop = crop_bbox(frame, bbox)
        if crop is None:
            return None, 0.0
        faces = self.app.get(crop)
        if not faces:
            return None, 0.0
        face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        emb = face.embedding
        best_name, best_sim = None, -1.0
        for name, saved_emb in self.database.items():
            sim = float(np.dot(emb, saved_emb) / (np.linalg.norm(emb) * np.linalg.norm(saved_emb)))
            if sim > best_sim:
                best_sim = sim
                best_name = name
        if best_sim >= FACE_SIM_THRESHOLD:
            return best_name, best_sim
        return None, best_sim


# ================= LIDAR GUARD =================
class LidarGuard(object):
    """Theo doi vat can phia truoc/sau, kem GOC (bearing) cua vat can gan nhat
    de phan biet voi huong nguoi dang theo (xem ALIGN_TOLERANCE_DEG)."""

    def __init__(self):
        self.min_front_dist = float('inf')
        self.min_rear_dist = float('inf')
        self.nearest_angle_deg = 0.0   # goc (do) cua vat can gan nhat phia truoc
        self.avoid_steer_bias = 0.0    # huong thoang hon (+: trai, -: phai), o MAX_STEER_ANGLE

    def update(self, scan):
        ranges = np.array(scan.ranges)
        angles = scan.angle_min + np.arange(len(ranges)) * scan.angle_increment
        angles_deg = np.degrees(angles)

        front_mask = np.abs(angles_deg) <= FRONT_HALF_ANGLE_DEG
        rear_mask = np.abs(np.abs(angles_deg) - 180) <= REAR_HALF_ANGLE_DEG

        front_ranges = ranges[front_mask]
        front_angles_deg = angles_deg[front_mask]
        valid_front = np.isfinite(front_ranges) & (front_ranges > 0.01)

        rear_ranges = ranges[rear_mask]
        valid_rear = np.isfinite(rear_ranges) & (rear_ranges > 0.01)
        self.min_rear_dist = float(np.min(rear_ranges[valid_rear])) if np.any(valid_rear) else float('inf')

        if not np.any(valid_front):
            self.min_front_dist = float('inf')
            self.nearest_angle_deg = 0.0
            self.avoid_steer_bias = 0.0
            return

        front_ranges = front_ranges[valid_front]
        front_angles_deg = front_angles_deg[valid_front]
        idx_min = int(np.argmin(front_ranges))
        self.min_front_dist = float(front_ranges[idx_min])
        self.nearest_angle_deg = float(front_angles_deg[idx_min])

        left_mean = np.mean(front_ranges[front_angles_deg > 0]) if np.any(front_angles_deg > 0) else 0
        right_mean = np.mean(front_ranges[front_angles_deg < 0]) if np.any(front_angles_deg < 0) else 0
        self.avoid_steer_bias = MAX_STEER_ANGLE if left_mean > right_mean else -MAX_STEER_ANGLE


# ================= MAIN NODE =================
class JetRacerFollower(object):
    STATE_SEARCHING = 'SEARCHING'
    STATE_TRACKING = 'TRACKING'

    def __init__(self):
        face_db_path = rospy.get_param('~face_db', os.path.expanduser('~/jetracer_ws/faces.pkl'))
        trt_model_name = rospy.get_param('~trt_model_name', 'yolov3-tiny')
        rospy.loginfo("face_db=%s trt_model_name=%s", face_db_path, trt_model_name)

        self.detector = PersonDetector(trt_model_name)
        self._shutting_down = False
        rospy.on_shutdown(self._cleanup)

        if USE_FACE_ID:
            self.face_matcher = FaceIDMatcher(face_db_path)
        else:
            self.face_matcher = None
            rospy.loginfo("USE_FACE_ID=False -> lock vao nguoi gan nhat, khong dung InsightFace")

        self.lidar_guard = LidarGuard()

        self.state = self.STATE_SEARCHING
        self.locked_bbox = None
        self.locked_hist = None
        self.locked_name = None
        self.lost_counter = 0
        self.frame_count = 0
        self.prev_steer = 0.0
        self.prev_speed = 0.0
        self.last_offset = 0.0
        self.search_recovery_frames = 0
        self.prev_valid_lidar_dist = None  # phat hien vung mu LiDAR khi qua gan

        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.debug_pub = rospy.Publisher('/follow_debug', String, queue_size=1)
        rospy.Subscriber('/csi_cam_0/image_raw', Image, self.image_cb, queue_size=1, buff_size=2**24)
        rospy.Subscriber('/scan', LaserScan, self.lidar_cb, queue_size=1)

        rospy.loginfo("JetRacerFollower (manfollow_avoidobj) da khoi dong. State=%s", self.state)

    def lidar_cb(self, scan):
        self.lidar_guard.update(scan)

    def _cleanup(self):
        rospy.loginfo("Dang don CUDA context truoc khi thoat...")
        self._shutting_down = True
        time.sleep(0.3)
        try:
            self.detector.cuda_ctx.pop()
            self.detector.cuda_ctx.detach()
        except Exception as e:
            rospy.logwarn("Loi luc don CUDA context: %s", e)

    def image_cb(self, img_msg):
        if self._shutting_down:
            return
        frame = imgmsg_to_cv2(img_msg)
        self.frame_count += 1
        h, w = frame.shape[:2]

        if self.frame_count % 5 == 0:
            cv2.imwrite('/tmp/debug_frame.jpg', frame)

        detections = self.detector.detect(frame)

        if self.state == self.STATE_SEARCHING:
            self._handle_searching(frame, detections)
        else:
            self._handle_tracking(frame, detections)

        steer, speed, mode = self._compute_drive_cmd(w, h)
        self._publish_cmd(steer, speed)
        self._publish_debug(steer, speed, len(detections), w, h, mode)

    def _publish_debug(self, steer, speed, num_detections, img_w, img_h, mode):
        info = {
            "state": self.state,
            "mode": mode,  # "FOLLOW_PERSON" hoac "AVOID_OBSTACLE" hoac "SEARCH_RECOVERY" / "IDLE"
            "target_name": self.locked_name,
            "bbox": [float(v) for v in self.locked_bbox] if self.locked_bbox is not None else None,
            "img_w": img_w,
            "img_h": img_h,
            "num_detections": num_detections,
            "steer": round(float(steer), 4),
            "speed": round(float(speed), 4),
            "lidar_min_dist": round(float(self.lidar_guard.min_front_dist), 3)
                if self.lidar_guard.min_front_dist != float('inf') else None,
            "lidar_min_rear_dist": round(float(self.lidar_guard.min_rear_dist), 3)
                if self.lidar_guard.min_rear_dist != float('inf') else None,
            "obstacle_angle_deg": round(float(self.lidar_guard.nearest_angle_deg), 1),
        }
        self.debug_pub.publish(String(data=json.dumps(info)))

    # ---------------- state logic (giong cam_manfollow.py) ----------------
    def _handle_searching(self, frame, detections):
        if not detections:
            return
        if not USE_FACE_ID:
            bbox = max(detections, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
            self.locked_bbox = bbox
            self.locked_hist = hsv_hist(frame, bbox)
            self.locked_name = "nearest"
            self.lost_counter = 0
            self.state = self.STATE_TRACKING
            rospy.loginfo("Lock target (nearest, khong khop mat)")
            return

        if self.frame_count % REID_INTERVAL != 0:
            return
        for bbox in detections:
            name, score = self.face_matcher.match_in_bbox(frame, bbox)
            if name is not None:
                self.locked_bbox = bbox
                self.locked_hist = hsv_hist(frame, bbox)
                self.locked_name = name
                self.lost_counter = 0
                self.state = self.STATE_TRACKING
                rospy.loginfo("Lock target: %s (sim=%.2f)", name, score)
                return

    def _handle_tracking(self, frame, detections):
        if not detections:
            self._register_lost()
            return

        best_iou, best_box = 0.0, None
        for bbox in detections:
            score = iou(self.locked_bbox, bbox)
            if score > best_iou:
                best_iou, best_box = score, bbox

        if best_iou >= IOU_MATCH_THRESHOLD:
            self.locked_bbox = best_box
            self.locked_hist = hsv_hist(frame, best_box)
            self.lost_counter = 0
            return

        best_sim, best_box = -1.0, None
        for bbox in detections:
            hh = hsv_hist(frame, bbox)
            sim = hist_similarity(self.locked_hist, hh)
            if sim > best_sim:
                best_sim, best_box = sim, bbox

        if best_sim >= HSV_SIM_THRESHOLD:
            self.locked_bbox = best_box
            self.locked_hist = hsv_hist(frame, best_box)
            self.lost_counter = 0
            return

        self._register_lost()

    def _register_lost(self):
        self.lost_counter += 1
        if self.lost_counter > LOST_FRAMES_LIMIT:
            rospy.logwarn("Mat target '%s', quay lai SEARCHING", self.locked_name)
            self.state = self.STATE_SEARCHING
            self.locked_bbox = None
            self.locked_hist = None
            self.locked_name = None
            self.lost_counter = 0
            self.prev_steer = 0.0
            self.prev_speed = 0.0
            self.search_recovery_frames = 0
            self.prev_valid_lidar_dist = None

    # ---------------- drive command ----------------
    def _search_recovery_cmd(self):
        """Mat track: LUI THANG ve vi tri cu (khong danh lai, khong tu lai
        di tim/lan truong) -- xem docstring dau file ve quyet dinh nay."""
        if self.search_recovery_frames >= SEARCH_RECOVERY_MAX_FRAMES:
            self.prev_steer, self.prev_speed = 0.0, 0.0
            return 0.0, 0.0, "IDLE"

        if self.lidar_guard.min_rear_dist < REAR_SAFE_DIST:
            self.prev_steer, self.prev_speed = 0.0, 0.0
            return 0.0, 0.0, "IDLE"

        self.search_recovery_frames += 1
        speed = SEARCH_RECOVERY_SPEED
        steer = 0.0
        steer = SMOOTH_ALPHA_STEER * steer + (1 - SMOOTH_ALPHA_STEER) * self.prev_steer
        speed = SMOOTH_ALPHA_SPEED * speed + (1 - SMOOTH_ALPHA_SPEED) * self.prev_speed
        self.prev_steer, self.prev_speed = steer, speed
        return steer, speed, "SEARCH_RECOVERY"

    def _compute_drive_cmd(self, img_w, img_h):
        if self.state != self.STATE_TRACKING or self.locked_bbox is None:
            return self._search_recovery_cmd()

        x1, y1, x2, y2 = self.locked_bbox
        center_x = (x1 + x2) / 2.0
        offset = (center_x - img_w / 2.0) / (img_w / 2.0)
        self.last_offset = offset

        # ===== 1) Tinh lai+toc do THEO NGUOI (mac dinh) =====
        if abs(offset) < STEER_DEADBAND:
            delta_person = 0.0
        else:
            delta_person = clip(-offset * STEER_GAIN * MAX_STEER_ANGLE,
                                 -MAX_STEER_ANGLE, MAX_STEER_ANGLE)

        lidar_dist = self.lidar_guard.min_front_dist
        if lidar_dist == float('inf'):
            if (self.prev_valid_lidar_dist is not None
                    and self.prev_valid_lidar_dist < SAFE_STOP_DIST):
                speed_person = MIN_SPEED * 0.6  # vung mu do qua gan -> lui nhe
            else:
                speed_person = NO_LIDAR_FALLBACK_SPEED
        else:
            self.prev_valid_lidar_dist = lidar_dist
            dist_error = lidar_dist - TARGET_FOLLOW_DIST
            if abs(dist_error) < FOLLOW_DEADBAND:
                speed_person = 0.0
            else:
                speed_person = clip(dist_error * DIST_SPEED_GAIN, MIN_SPEED, MAX_SPEED)

        mode = "FOLLOW_PERSON"

        # ===== 2) Kiem tra co VAT CAN KHAC (khong phai nguoi) can ne khong =====
        if lidar_dist != float('inf') and lidar_dist < OBSTACLE_DIST:
            person_bearing_deg = offset * CAMERA_FOV_HALF_DEG
            angle_diff = abs(self.lidar_guard.nearest_angle_deg - person_bearing_deg)
            is_same_as_person = angle_diff < ALIGN_TOLERANCE_DEG

            if not is_same_as_person:
                # Vat can KHAC nguoi dang theo -> uu tien NE, override ca lai va toc do
                mode = "AVOID_OBSTACLE"
                if lidar_dist < SAFE_STOP_DIST:
                    if self.lidar_guard.min_rear_dist < REAR_SAFE_DIST:
                        delta_person, speed_person = 0.0, 0.0  # ket ca 2 phia -> dung
                    else:
                        delta_person = self.lidar_guard.avoid_steer_bias
                        speed_person = AVOID_REVERSE_SPEED
                else:
                    delta_person = self.lidar_guard.avoid_steer_bias
                    speed_person = AVOID_CREEP_SPEED
            # else: trung huong nguoi -> day chinh la nguoi dang theo, GIU logic
            # theo nguoi nhu cu (an toan khoang cach o tren da tu xu ly dung/lui).

        delta, speed = delta_person, speed_person

        # ===== 3) Toc do tu dieu chinh theo goc lai (re gat -> giam toc) =====
        turn_factor = 1.0 - (abs(delta) / MAX_STEER_ANGLE) * TURN_SLOWDOWN_RATIO
        speed = speed * turn_factor

        # ===== 4) An toan tuyet doi cuoi cung =====
        if speed < 0:
            if self.lidar_guard.min_rear_dist < REAR_SAFE_DIST:
                speed = 0.0
        else:
            if lidar_dist != float('inf') and lidar_dist < SAFE_STOP_DIST:
                speed = 0.0
            elif lidar_dist != float('inf') and lidar_dist < CAUTION_DIST and mode == "FOLLOW_PERSON":
                speed = min(speed, CAUTION_SPEED)

        if abs(speed) < 1e-3:
            steer = 0.0
        else:
            steer = ackermann_angular(speed, delta)

        # ===== 5) Lam muot =====
        steer = SMOOTH_ALPHA_STEER * steer + (1 - SMOOTH_ALPHA_STEER) * self.prev_steer
        speed = SMOOTH_ALPHA_SPEED * speed + (1 - SMOOTH_ALPHA_SPEED) * self.prev_speed
        self.prev_steer = steer
        self.prev_speed = speed

        return steer, speed, mode

    def _publish_cmd(self, steer, speed):
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = steer * SERVO_ANGULAR_SCALE
        self.cmd_pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('manfollow_avoidobj')
    JetRacerFollower()
    rospy.spin()