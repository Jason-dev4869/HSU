#!/usr/bin/env python3
"""
camera_node.py — JetRacer ROS Line Follower
Publish camera frames lên /camera/image_raw

Hỗ trợ:
  - CSI camera (Jetson Nano, dùng GStreamer + nvarguscamerasrc)
  - USB camera (bất kỳ /dev/videoX)

Topic publish:
  /camera/image_raw      (sensor_msgs/Image)
  /camera/camera_info    (sensor_msgs/CameraInfo)  [nếu có calibration file]

Parameters (set qua launch file hoặc rosparam):
  ~camera_type    : "CSI" | "USB"       (default: "CSI")
  ~device_id      : int                  (default: 0  → /dev/video0)
  ~width          : int                  (default: 640)
  ~height         : int                  (default: 480)
  ~fps            : int                  (default: 30)
  ~flip_method    : int  CSI only        (default: 0)
                    0=no flip, 1=CW 90°, 2=rotate 180°, 3=CCW 90°
                    4=horizontal flip, 5=upper-right diagonal flip
                    6=vertical flip, 7=upper-left diagonal flip
  ~queue_size     : int                  (default: 1)
                    Luôn để 1 để line_detector nhận frame mới nhất
  ~calibration    : str  path to .yaml  (default: "" = bỏ qua camera_info)
"""

import sys
import rospy
import cv2
import numpy as np

from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Header
from cv_bridge import CvBridge, CvBridgeError


# ─────────────────────────────────────────────────────────────
# GStreamer pipeline builder cho CSI camera trên Jetson Nano
# ─────────────────────────────────────────────────────────────

def _gstreamer_pipeline(width: int, height: int, fps: int, flip_method: int) -> str:
    """
    Tạo GStreamer pipeline chuẩn cho CSI camera trên Jetson Nano.

    nvarguscamerasrc  → capture raw từ ISP của Jetson
    nvvidconv         → convert NV12 (NVMM memory) → BGRx (CPU memory)
    videoconvert      → BGRx → BGR (format mà OpenCV hiểu)
    appsink           → đẩy frame vào Python/OpenCV

    flip_method:
        0 = không flip (camera gắn thẳng)
        2 = xoay 180° (camera gắn ngược đầu — rất phổ biến trên JetRacer)
        6 = lật dọc
    """
    return (
        f"nvarguscamerasrc ! "
        f"video/x-raw(memory:NVMM), "
        f"width=(int){width}, height=(int){height}, "
        f"format=(string)NV12, framerate=(fraction){fps}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){width}, height=(int){height}, "
        f"format=(string)BGRx ! "
        f"videoconvert ! "
        f"video/x-raw, format=(string)BGR ! "
        f"appsink max-buffers=1 drop=true"
        # max-buffers=1 drop=true: chỉ giữ frame mới nhất, bỏ frame cũ
        # tránh tích lũy buffer gây lag
    )


# ─────────────────────────────────────────────────────────────
# Loader calibration từ .yaml (tùy chọn)
# ─────────────────────────────────────────────────────────────

def _load_camera_info(yaml_path: str) -> CameraInfo | None:
    """
    Đọc camera calibration file (định dạng ROS camera_calibration).
    Trả về None nếu file không tồn tại hoặc lỗi parse.

    Format yaml cần có:
        image_width, image_height,
        camera_matrix (data: [...]),
        distortion_coefficients (data: [...]),
        rectification_matrix (data: [...]),
        projection_matrix (data: [...])
    """
    if not yaml_path:
        return None

    try:
        import yaml
        with open(yaml_path, 'r') as f:
            calib = yaml.safe_load(f)

        info = CameraInfo()
        info.width  = calib['image_width']
        info.height = calib['image_height']
        info.distortion_model = calib.get('distortion_model', 'plumb_bob')

        info.K = calib['camera_matrix']['data']           # 3×3 intrinsic
        info.D = calib['distortion_coefficients']['data'] # distortion coeffs
        info.R = calib['rectification_matrix']['data']    # 3×3 rectification
        info.P = calib['projection_matrix']['data']       # 3×4 projection

        rospy.loginfo(f"[camera_node] Calibration loaded from: {yaml_path}")
        return info

    except FileNotFoundError:
        rospy.logwarn(f"[camera_node] Calibration file not found: {yaml_path}")
        return None
    except KeyError as e:
        rospy.logwarn(f"[camera_node] Calibration yaml thiếu key: {e}")
        return None
    except Exception as e:
        rospy.logwarn(f"[camera_node] Lỗi đọc calibration: {e}")
        return None


# ─────────────────────────────────────────────────────────────
# Main node class
# ─────────────────────────────────────────────────────────────

class CameraNode:
    """
    ROS node: đọc frame từ camera, publish lên /camera/image_raw.

    Vòng lặp chính:
        1. cap.read() → numpy array BGR
        2. (tuỳ chọn) flip nếu camera USB gắn ngược
        3. cv_bridge.cv2_to_imgmsg() → ROS Image
        4. pub.publish()
    """

    def __init__(self):
        rospy.init_node('camera_node', anonymous=False)

        # ── Đọc parameters ──────────────────────────────────
        self.camera_type  = rospy.get_param('~camera_type',  'CSI').upper()
        self.device_id    = rospy.get_param('~device_id',    0)
        self.width        = rospy.get_param('~width',        640)
        self.height       = rospy.get_param('~height',       480)
        self.fps          = rospy.get_param('~fps',          30)
        self.flip_method  = rospy.get_param('~flip_method',  0)
        self.queue_size   = rospy.get_param('~queue_size',   1)
        calib_path        = rospy.get_param('~calibration',  '')

        # ── Publishers ────────────────────────────────────────
        self.pub_image = rospy.Publisher(
            '/camera/image_raw',
            Image,
            queue_size=self.queue_size   # queue_size=1: drop frame cũ, giữ frame mới nhất
        )
        self.pub_info = rospy.Publisher(
            '/camera/camera_info',
            CameraInfo,
            queue_size=self.queue_size
        )

        # ── cv_bridge ─────────────────────────────────────────
        self.bridge = CvBridge()

        # ── Camera calibration (tuỳ chọn) ────────────────────
        self.camera_info = _load_camera_info(calib_path)

        # ── Mở camera ─────────────────────────────────────────
        self.cap = self._open_camera()

        # ── Counter để log thống kê ───────────────────────────
        self._frame_count = 0
        self._error_count = 0

        # ── Đăng ký shutdown hook ─────────────────────────────
        rospy.on_shutdown(self._shutdown)

        rospy.loginfo(
            f"[camera_node] Ready — "
            f"type={self.camera_type}, "
            f"res={self.width}×{self.height}, "
            f"fps={self.fps}"
        )

    # ─────────────────────────────────────────────────────────
    # Mở camera — tự động chọn CSI hoặc USB
    # ─────────────────────────────────────────────────────────

    def _open_camera(self) -> cv2.VideoCapture:
        """
        Mở VideoCapture theo loại camera.
        Nếu CSI fail (không có nvarguscamerasrc), tự fallback sang USB.
        """
        if self.camera_type == 'CSI':
            return self._open_csi()
        elif self.camera_type == 'USB':
            return self._open_usb()
        else:
            rospy.logwarn(
                f"[camera_node] camera_type '{self.camera_type}' không hợp lệ. "
                f"Dùng 'CSI' hoặc 'USB'. Fallback về USB."
            )
            return self._open_usb()

    def _open_csi(self) -> cv2.VideoCapture:
        """Mở CSI camera qua GStreamer pipeline."""
        pipeline = _gstreamer_pipeline(
            self.width, self.height, self.fps, self.flip_method
        )
        rospy.loginfo(f"[camera_node] GStreamer pipeline:\n  {pipeline}")

        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not cap.isOpened():
            rospy.logwarn(
                "[camera_node] Không mở được CSI camera qua GStreamer. "
                "Kiểm tra:\n"
                "  1. Camera CSI đã cắm chưa?\n"
                "  2. JetPack đã cài nvarguscamerasrc chưa?\n"
                "  3. Thử: nvgstcapture-1.0\n"
                "Fallback sang USB camera..."
            )
            return self._open_usb()

        rospy.loginfo("[camera_node] CSI camera OK (GStreamer)")
        return cap

    def _open_usb(self) -> cv2.VideoCapture:
        """
        Mở USB camera (/dev/videoX).
        Set resolution và fps thủ công (một số camera không nhận).
        """
        rospy.loginfo(f"[camera_node] Mở USB camera /dev/video{self.device_id}")

        cap = cv2.VideoCapture(self.device_id)

        if not cap.isOpened():
            rospy.logfatal(
                f"[camera_node] Không thể mở /dev/video{self.device_id}!\n"
                f"  Kiểm tra: ls /dev/video*\n"
                f"  Thử device_id khác qua: rosparam set /camera_node/device_id 1"
            )
            sys.exit(1)

        # Set properties — không phải camera nào cũng nhận được
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS,          self.fps)

        # Đọc lại giá trị thực tế camera chấp nhận
        actual_w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = cap.get(cv2.CAP_PROP_FPS)

        if actual_w != self.width or actual_h != self.height:
            rospy.logwarn(
                f"[camera_node] Camera không hỗ trợ {self.width}×{self.height}. "
                f"Thực tế: {actual_w}×{actual_h}. "
                f"Sẽ resize về {self.width}×{self.height} bằng phần mềm."
            )
            self._needs_resize = True
        else:
            self._needs_resize = False

        rospy.loginfo(
            f"[camera_node] USB camera OK — "
            f"{actual_w}×{actual_h} @ {actual_fps:.1f}fps"
        )
        return cap

    # ─────────────────────────────────────────────────────────
    # Vòng lặp chính
    # ─────────────────────────────────────────────────────────

    def run(self):
        """
        Spin loop: đọc frame và publish.
        rate.sleep() đảm bảo không publish nhanh hơn fps cần thiết.
        """
        rate = rospy.Rate(self.fps)

        while not rospy.is_shutdown():
            ret, frame = self.cap.read()

            if not ret or frame is None:
                self._error_count += 1
                rospy.logwarn_throttle(
                    5.0,   # log tối đa 1 lần mỗi 5 giây để không spam
                    f"[camera_node] Không đọc được frame "
                    f"(lỗi lần {self._error_count}). "
                    f"Thử kết nối lại..."
                )
                self._try_reconnect()
                rate.sleep()
                continue

            # ── Preprocess ──────────────────────────────────
            frame = self._preprocess(frame)

            # ── Build header với timestamp ───────────────────
            # Dùng rospy.Time.now() để timestamp đồng bộ với ROS clock
            # Quan trọng khi replay với rosbag
            header = Header()
            header.stamp    = rospy.Time.now()
            header.frame_id = 'camera_link'

            # ── Convert và publish image ─────────────────────
            try:
                img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                img_msg.header = header
                self.pub_image.publish(img_msg)
            except CvBridgeError as e:
                rospy.logerr(f"[camera_node] cv_bridge error: {e}")
                rate.sleep()
                continue

            # ── Publish camera_info nếu có calibration ───────
            if self.camera_info is not None:
                self.camera_info.header = header
                self.pub_info.publish(self.camera_info)

            # ── Stats log mỗi 100 frame ──────────────────────
            self._frame_count += 1
            if self._frame_count % 100 == 0:
                rospy.loginfo(
                    f"[camera_node] {self._frame_count} frames published "
                    f"({self._error_count} errors)"
                )

            rate.sleep()

    # ─────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Xử lý frame trước khi publish.
          1. Resize nếu USB camera không nhận resolution yêu cầu
          2. (Có thể thêm: white balance correction, undistort, v.v.)
        """
        # Resize nếu cần (USB camera không nhận resolution yêu cầu)
        if getattr(self, '_needs_resize', False):
            frame = cv2.resize(
                frame,
                (self.width, self.height),
                interpolation=cv2.INTER_LINEAR
            )

        # USB flip (flip_method chỉ có tác dụng với GStreamer/CSI)
        # Dùng cho trường hợp camera USB gắn ngược
        if self.camera_type == 'USB' and self.flip_method == 2:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif self.camera_type == 'USB' and self.flip_method == 6:
            frame = cv2.flip(frame, 0)   # flip dọc
        elif self.camera_type == 'USB' and self.flip_method == 4:
            frame = cv2.flip(frame, 1)   # flip ngang

        return frame

    def _try_reconnect(self):
        """
        Thử reconnect camera nếu mất kết nối.
        Thực tế: USB camera đôi khi timeout, cần release rồi mở lại.
        """
        if self._error_count % 30 != 0:  # thử lại mỗi 30 lần lỗi
            return

        rospy.logwarn("[camera_node] Thử reconnect camera...")
        self.cap.release()
        import time
        time.sleep(1.0)
        self.cap = self._open_camera()

    def _shutdown(self):
        """Cleanup khi node tắt (Ctrl+C hoặc rosnode kill)."""
        rospy.loginfo("[camera_node] Shutting down, releasing camera...")
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        rospy.loginfo(
            f"[camera_node] Done. "
            f"Total frames: {self._frame_count}, "
            f"Total errors: {self._error_count}"
        )


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        node = CameraNode()
        node.run()
    except rospy.ROSInterruptException:
        # Bình thường khi Ctrl+C — không phải lỗi
        pass
    except Exception as e:
        rospy.logfatal(f"[camera_node] Unhandled exception: {e}")
        raise
