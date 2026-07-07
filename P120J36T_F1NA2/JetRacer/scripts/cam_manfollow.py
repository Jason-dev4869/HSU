#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cam_manfollow.py
========================
Node DOC LAP chi test Camera + YOLO person-following, KHONG test obstacle
avoidance tong quat (da tach rieng sang lidar_avoidobj.py). LiDAR o day
CHI dung de giu khoang cach voi nguoi dang theo + dung an toan toi thieu
phia truoc/sau, khong co logic "ne sang trai/phai" nhu file lidar rieng.

Pipeline:
  [Camera] YOLOv3-tiny (person detection, cv2.dnn) -> bbox nguoi
     -> Lock vao nguoi GAN NHAT (bbox lon nhat) khi SEARCHING.
     -> IoU tracking giua cac frame khi da lock target.
     -> HSV histogram fallback de tai nhan dien khi mat IoU match.
  [LiDAR] Giu khoang cach voi nguoi dang theo (TARGET_FOLLOW_DIST) +
          chan lui neu phia sau co vat can (an toan toi thieu).
  [Output] geometry_msgs/Twist -> /cmd_vel

Sau khi xac nhan ca file nay VA lidar_avoidobj.py deu chay tot rieng le,
gop logic ca 2 lai vao manfollow_avoidobj.py.
"""

import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_THREAD_LIMIT', '1')

import sys
# tensorrt_demos nam o human_following/tensorrt_demos/, can them vao path de import utils.*
TENSORRT_DEMOS_DIR = os.path.expanduser('~/catkin_ws/src/human_following/tensorrt_demos')
sys.path.append(TENSORRT_DEMOS_DIR)

# QUAN TRONG: utils.yolo_with_plugins load file './plugins/libyolo_layer.so' theo
# duong dan TUONG DOI ngay luc IMPORT module (khong phai luc goi TrtYOLO()), nen
# phai chdir TRUOC dong import nay, khong phai trong __init__ cua PersonDetector.
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
USE_FACE_ID = False  # False: lock vao nguoi GAN NHAT, khong can khop khuon mat

YOLO_INPUT_SIZE = (416, 416)
YOLO_CONF_THRES = 0.25
YOLO_NMS_THRES = 0.4

# Steering (Ackermann)
MAX_STEER = 0.34
WHEELBASE = 0.16
MAX_STEER_ANGLE = np.deg2rad(25)
STEER_DEADBAND = 0.12    # tang tu 0.08 -> giam re sai khi nguoi dung gan, bbox de bi nhieu
STEER_GAIN = 0.32        # giam tu 0.45 -> servo van con re hoi lo, giam them

# Toc do TU DIEU CHINH theo goc lai: re gat -> giam toc, di thang -> toc binh thuong.
# Giam dich chuyen moi lenh luc dang re, bot overshoot.
TURN_SLOWDOWN_RATIO = 0.6  # 0: khong giam gi luc re, 1: giam toi da 100% khi re full max

# He so SCALE CUOI CUNG cho angular.z truoc khi gui xuong chassis driver -- chinh
# THUC NGHIEM, doc lap voi STEER_GAIN/Ackermann phia tren. Driver jetracer tu co
# he so PWM rieng (khong nam trong code nay), neu servo van re lo du da giam
# STEER_GAIN -> giam tiep so nay (0.5, 0.3...) cho toi khi vua y.
SERVO_ANGULAR_SCALE = 0.5

# Lam muot lenh dieu khien (low-pass filter) -- QUAN TRONG: camera+YOLO chi cap nhat
# duoc ~3-6Hz tren Jetson Nano (CPU), neu lenh thay doi nhanh hon toc do cam nhan se
# gay dao dong/mat lock lien tuc. Alpha nho = muot hon nhung phan ung cham hon.
SMOOTH_ALPHA_STEER = 0.3
SMOOTH_ALPHA_SPEED = 0.3

# ---- Khi mat track: lui thang ve vi tri cu, KHONG tien tim theo huong nua ----
SEARCH_RECOVERY_SPEED = -0.30   # m/s (am = lui)
SEARCH_RECOVERY_MAX_FRAMES = 30  # so frame toi da lui truoc khi dung han

# ---- Giu khoang cach bang LiDAR (KHONG dung bbox height nua) ----
TARGET_FOLLOW_DIST = 0.45      # m - giua vung dung 0.30-0.60m
FOLLOW_DEADBAND = 0.15         # m - +-0.15 quanh 0.45 = dung tai 0.30-0.60m
DIST_SPEED_GAIN = 1.2          # he so chuyen doi sai so khoang cach (m) -> toc do (m/s)
DIST_DAMPING_GAIN = 0.5        # (PD) phanh/tang toc som theo TOC DO thay doi khoang cach,
                                # khong chi theo khoang cach hien tai -- giam dao dong tien/lui
DIST_VELOCITY_ALPHA = 0.4      # do muot uoc luong toc do thay doi khoang cach (EMA)

OFFSET_PREDICT_LEAD = 2.5      # so frame du doan truoc vi tri nguoi (lead control khi lai)
OFFSET_VELOCITY_ALPHA = 0.5    # do muot uoc luong van toc lech tam (EMA)
MAX_SPEED = 0.3
MIN_SPEED = -0.30
NO_LIDAR_FALLBACK_SPEED = 0.25  # toc do tien cham khi LiDAR khong thay gi phia truoc (qua xa pham vi do)

# An toan tuyet doi - override bat ke dang lam gi
SAFE_STOP_DIST = 0.30   # < 30cm: dung hoan toan
OBSTACLE_DIST = 0.45    # 30-45cm: giam toc
FRONT_HALF_ANGLE_DEG = 25
REAR_HALF_ANGLE_DEG = 30    # vung quet phia SAU, de chan lui vao vat can/tuong
REAR_SAFE_DIST = 0.30       # < 30cm phia sau -> khong cho lui


def imgmsg_to_cv2(msg):
    """Tu decode sensor_msgs/Image -> numpy BGR array, khong dung cv_bridge."""
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


# ================= PERSON DETECTOR (YOLOv3-tiny qua cv2.dnn) =================
class PersonDetector(object):
    """Dung TensorRT engine (yolov3-tiny.trt) thay cho cv2.dnn.
    Tu tao CUDA context rieng (khong dung pycuda.autoinit) va truyen vao
    TrtYOLO de class do tu push()/pop() dung luc detect() - quan trong vi
    image_cb cua ROS chay tren thread khac voi thread khoi tao."""

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

    # Don dep CUDA context qua rospy.on_shutdown() trong JetRacerFollower._cleanup(),
    # KHONG dung __del__ o day (khong dang tin cay luc Python thoat qua signal).


# ================= FACE-ID MATCHER (InsightFace buffalo_sc) =================
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
    def __init__(self):
        self.obstacle = False
        self.steer_bias = 0.0
        self.min_front_dist = float('inf')
        self.min_rear_dist = float('inf')

    def update(self, scan):
        ranges = np.array(scan.ranges)
        angles = scan.angle_min + np.arange(len(ranges)) * scan.angle_increment
        angles_deg = np.degrees(angles)

        front_mask = np.abs(angles_deg) <= FRONT_HALF_ANGLE_DEG
        # phia sau: goc gan +-180 do (vi du 170..180 va -180..-170)
        rear_mask = np.abs(np.abs(angles_deg) - 180) <= REAR_HALF_ANGLE_DEG

        front_ranges = ranges[front_mask]
        front_angles = angles[front_mask]
        valid_front = np.isfinite(front_ranges) & (front_ranges > 0.01)

        rear_ranges = ranges[rear_mask]
        valid_rear = np.isfinite(rear_ranges) & (rear_ranges > 0.01)
        self.min_rear_dist = float(np.min(rear_ranges[valid_rear])) if np.any(valid_rear) else float('inf')

        if not np.any(valid_front):
            self.obstacle = False
            self.min_front_dist = float('inf')
            return

        front_ranges = front_ranges[valid_front]
        front_angles = front_angles[valid_front]
        self.min_front_dist = float(np.min(front_ranges))

        if self.min_front_dist < OBSTACLE_DIST:
            self.obstacle = True
            left_mean = np.mean(front_ranges[front_angles > 0]) if np.any(front_angles > 0) else 0
            right_mean = np.mean(front_ranges[front_angles < 0]) if np.any(front_angles < 0) else 0
            self.steer_bias = MAX_STEER if left_mean > right_mean else -MAX_STEER
        else:
            self.obstacle = False
            self.steer_bias = 0.0


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
        self.last_offset = 0.0           # offset cuoi cung trc khi mat track (>0: nguoi o ben phai)
        self.search_recovery_frames = 0  # so frame da co gang tim lai theo huong cuoi

        # Du doan motion: uoc luong van toc lech tam (cho lai) va van toc
        # khoang cach (cho phanh/tang toc som hon, giam dao dong)
        self.prev_offset = 0.0
        self.offset_velocity = 0.0
        self.prev_lidar_dist = None
        self.lidar_dist_velocity = 0.0
        self.prev_valid_lidar_dist = None  # gia tri hop le gan nhat, de phat hien vung mu LiDAR

        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.debug_pub = rospy.Publisher('/follow_debug', String, queue_size=1)
        rospy.Subscriber('/csi_cam_0/image_raw', Image, self.image_cb, queue_size=1, buff_size=2**24)
        rospy.Subscriber('/scan', LaserScan, self.lidar_cb, queue_size=1)

        rospy.loginfo("JetRacerFollower da khoi dong. State=%s", self.state)

    def lidar_cb(self, scan):
        self.lidar_guard.update(scan)

    def _cleanup(self):
        rospy.loginfo("Dang don CUDA context truoc khi thoat...")
        self._shutting_down = True
        time.sleep(0.3)  # cho image_cb dang chay (neu co) kip ket thuc truoc khi pop context
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
            rospy.loginfo_throttle(5, "DEBUG: frame_count=%d, da luu debug_frame.jpg", self.frame_count)

        detections = self.detector.detect(frame)

        if self.state == self.STATE_SEARCHING:
            self._handle_searching(frame, detections)
        else:
            self._handle_tracking(frame, detections)

        steer, speed = self._compute_drive_cmd(w, h)
        self._publish_cmd(steer, speed)
        self._publish_debug(steer, speed, len(detections), w, h)

    def _publish_debug(self, steer, speed, num_detections, img_w, img_h):
        info = {
            "state": self.state,
            "target_name": self.locked_name,
            "bbox": [float(v) for v in self.locked_bbox] if self.locked_bbox is not None else None,
            "img_w": img_w,
            "img_h": img_h,
            "num_detections": num_detections,
            "steer": round(float(steer), 4),
            "speed": round(float(speed), 4),
            "lidar_obstacle": bool(self.lidar_guard.obstacle),
            "lidar_min_dist": round(float(self.lidar_guard.min_front_dist), 3)
                if self.lidar_guard.min_front_dist != float('inf') else None,
            "lidar_min_rear_dist": round(float(self.lidar_guard.min_rear_dist), 3)
                if self.lidar_guard.min_rear_dist != float('inf') else None,
        }
        self.debug_pub.publish(String(data=json.dumps(info)))

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
            self.search_recovery_frames = 0  # bat dau dot tim lai theo huong cuoi
            self.offset_velocity = 0.0
            self.prev_offset = 0.0
            self.lidar_dist_velocity = 0.0
            self.prev_lidar_dist = None
            self.prev_valid_lidar_dist = None

    # ---------------- drive command ----------------
    def _search_recovery_cmd(self):
        """Khi mat track: LUI THANG ve vi tri cu (khong danh lai), thay vi
        tien tim mo theo huong cuoi -- on dinh hon, dung dung y "tro ve vi
        tri cu" ma nguoi dung mong muon."""
        if self.search_recovery_frames >= SEARCH_RECOVERY_MAX_FRAMES:
            self.prev_steer, self.prev_speed = 0.0, 0.0
            return 0.0, 0.0

        # Kiem tra an toan phia SAU truoc khi lui, giong logic o _compute_drive_cmd
        if self.lidar_guard.min_rear_dist < REAR_SAFE_DIST:
            self.prev_steer, self.prev_speed = 0.0, 0.0
            return 0.0, 0.0

        self.search_recovery_frames += 1
        speed = SEARCH_RECOVERY_SPEED
        steer = 0.0  # lui thang, khong danh lai

        steer = SMOOTH_ALPHA_STEER * steer + (1 - SMOOTH_ALPHA_STEER) * self.prev_steer
        speed = SMOOTH_ALPHA_SPEED * speed + (1 - SMOOTH_ALPHA_SPEED) * self.prev_speed
        self.prev_steer, self.prev_speed = steer, speed
        return steer, speed

    def _compute_drive_cmd(self, img_w, img_h):
        if self.state != self.STATE_TRACKING or self.locked_bbox is None:
            return self._search_recovery_cmd()

        x1, y1, x2, y2 = self.locked_bbox
        center_x = (x1 + x2) / 2.0

        # --- LAI: vision (can giua nguoi theo truc x), proportional thuan + deadband ---
        offset = (center_x - img_w / 2.0) / (img_w / 2.0)
        self.last_offset = offset  # nho lai de dung khi mat track

        if abs(offset) < STEER_DEADBAND:
            delta = 0.0
        else:
            delta = clip(-offset * STEER_GAIN * MAX_STEER_ANGLE, -MAX_STEER_ANGLE, MAX_STEER_ANGLE)

        # --- TOC DO: dung khoang cach LiDAR THUC, proportional thuan ---
        lidar_dist = self.lidar_guard.min_front_dist

        if lidar_dist == float('inf'):
            # LiDAR khong thay gi phia truoc -- co 2 truong hop hoan toan nguoc nhau:
            # (a) nguoi/vat o XA ngoai pham vi do -> nen tien tim.
            # (b) nguoi/vat QUA GAN, roi vao vung mu cua RPLIDAR A1 (~15-20cm,
            #     khong doc duoc) -> PHAI lui, KHONG duoc tien (neu khong se dam vao).
            # Phan biet bang gia tri hop le GAN NHAT truoc do: neu vua roi con rat
            # gan (<SAFE_STOP_DIST) thi gan nhu chac chan la truong hop (b).
            if (self.prev_valid_lidar_dist is not None
                    and self.prev_valid_lidar_dist < SAFE_STOP_DIST):
                speed = MIN_SPEED * 0.6  # vung mu do qua gan -> lui nhe de thoat vung mu
            else:
                speed = NO_LIDAR_FALLBACK_SPEED  # thuc su khong thay gi, xa -> tien tim
        else:
            self.prev_valid_lidar_dist = lidar_dist
            dist_error = lidar_dist - TARGET_FOLLOW_DIST  # > 0: con xa, can tien. < 0: qua gan, can lui.
            if abs(dist_error) < FOLLOW_DEADBAND:
                speed = 0.0
            else:
                speed = clip(dist_error * DIST_SPEED_GAIN, MIN_SPEED, MAX_SPEED)

        # --- TOC DO TU DIEU CHINH: re gat -> giam toc, di thang -> binh thuong ---
        turn_factor = 1.0 - (abs(delta) / MAX_STEER_ANGLE) * TURN_SLOWDOWN_RATIO
        speed = speed * turn_factor

        # --- AN TOAN: override cuoi cung, bat ke logic tren tinh ra gi ---
        if speed < 0:
            # Dang dinh LUI -- kiem tra phia SAU co vat can khong truoc khi cho lui
            if self.lidar_guard.min_rear_dist < REAR_SAFE_DIST:
                speed = 0.0  # vat can phia sau qua gan, KHONG cho lui, dung han
        else:
            # Dang dinh TIEN -- ap dung gioi han nhu cu cho phia truoc
            if lidar_dist < SAFE_STOP_DIST:
                speed = 0.0
            elif lidar_dist < OBSTACLE_DIST:
                speed = speed * 0.6

        if abs(speed) < 1e-3:
            steer = 0.0
        else:
            R = WHEELBASE / np.tan(delta) if abs(delta) > 1e-4 else float('inf')
            steer = speed / R if np.isfinite(R) and abs(R) > 1e-4 else 0.0

        # --- LAM MUOT: tranh lenh nhay qua nhanh so voi toc do camera/YOLO cap nhat ---
        steer = SMOOTH_ALPHA_STEER * steer + (1 - SMOOTH_ALPHA_STEER) * self.prev_steer
        speed = SMOOTH_ALPHA_SPEED * speed + (1 - SMOOTH_ALPHA_SPEED) * self.prev_speed
        self.prev_steer = steer
        self.prev_speed = speed

        return steer, speed

    def _publish_cmd(self, steer, speed):
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = steer * SERVO_ANGULAR_SCALE
        self.cmd_pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('cam_manfollow')
    JetRacerFollower()
    rospy.spin()