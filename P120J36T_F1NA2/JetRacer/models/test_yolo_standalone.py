#!/usr/bin/env python3
"""
Test doc lap cv2.dnn (YOLOv4-tiny) tren 1 anh tinh, KHONG qua ROS/gscam.
Dung de xac nhan model+weights hoat dong dung, tach rieng khoi van de
chat luong anh camera (mo, goc chup, crop bat thuong...).

Cach dung:
    python3 test_yolo_standalone.py /tmp/debug_frame.jpg
    python3 test_yolo_standalone.py /path/to/anh_nguoi_ro_net.jpg
"""
import sys
import cv2
import numpy as np

CFG = "/home/jetson/catkin_ws/src/human_following/models/yolov3-tiny.cfg"
WEIGHTS = "/home/jetson/catkin_ws/src/human_following/models/yolov3-tiny.weights"
PERSON_CLASS_ID = 0

if len(sys.argv) < 2:
    print("Dung: python3 test_yolo_standalone.py <duong_dan_anh.jpg>")
    sys.exit(1)

img_path = sys.argv[1]
img = cv2.imread(img_path)
if img is None:
    print(f"LOI: khong doc duoc anh tai {img_path}")
    sys.exit(1)

print(f"Anh: {img_path}, shape={img.shape}")

net = cv2.dnn.readNetFromDarknet(CFG, WEIGHTS)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

ln = net.getLayerNames()
out_layers = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
outputs = net.forward(out_layers)

best_person = 0.0
best_any_conf = 0.0
best_any_class = -1
total_rows = 0
num_above_01 = 0

for out in outputs:
    for det in out:
        total_rows += 1
        scores = det[5:]
        class_id = int(np.argmax(scores))
        conf = float(scores[class_id])
        if conf > 0.1:
            num_above_01 += 1
        if conf > best_any_conf:
            best_any_conf = conf
            best_any_class = class_id
        if class_id == PERSON_CLASS_ID and conf > best_person:
            best_person = conf

print(f"Tong so rows: {total_rows}")
print(f"Best person conf: {best_person:.8e}")
print(f"Best any class={best_any_class}, conf={best_any_conf:.8e}")
print(f"So cell co conf > 0.1 (bat ky class): {num_above_01}")

if best_any_conf < 1e-6:
    print("\n=> KET LUAN: network output gan nhu zero tuyet doi o MOI class.")
    print("   Day la dau hieu model/weights bi loi, KHONG phai do anh xau.")
else:
    print(f"\n=> KET LUAN: network CO phan hoi (best_any_conf={best_any_conf:.4f}).")
    print("   Model hoat dong binh thuong - van de truoc do co the do anh dau vao.")