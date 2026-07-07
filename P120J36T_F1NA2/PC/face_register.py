import os
import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis

# Ngưỡng nhận diện thử nghiệm trên PC (Từ 0.4 - 0.45)
THRESHOLD = 0.42 

def collect_face_data():
    print("\n--- [PC] HÀM THU THẬP DỮ LIỆU KHUÔN MẶT ---")
    name = input("Nhập tên người cần đăng ký: ").strip()
    if not name: return

    save_dir = os.path.join("dataset", name)
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0) # Sử dụng webcam của PC
    count = len(os.listdir(save_dir))

    print("=> Nhấn [SPACE] để chụp, [Q] để hoàn thành.")
    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow("PC Register Face", frame)
        key = cv2.waitKey(1)
        if key == ord(' '):
            filename = os.path.join(save_dir, f"{count:03d}.jpg")
            cv2.imwrite(filename, frame)
            print("Đã lưu vào PC:", filename)
            count += 1
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def train_face_embeddings():
    print("\n--- [PC] HÀM TRÍCH XUẤT VECTOR ĐẶC TRƯNG ---")
    if not os.path.exists("dataset") or not os.listdir("dataset"):
        print("Thư mục 'dataset' trên PC trống!")
        return

    print("Đang khởi tạo InsightFace trên PC...")
    # Dung buffalo_sc (nhe) de KHOP voi model chay tren JetRacer (jetracer_follow_node.py)
    # Neu dung FaceAnalysis() mac dinh (buffalo_l) o day nhung JetRacer dung buffalo_sc,
    # embedding 2 ben se KHONG cung khong gian vector -> so sanh cosine vo nghia.
    app = FaceAnalysis(name='buffalo_sc')
    app.prepare(ctx_id=0) 

    database = {}
    for person in os.listdir("dataset"):
        person_dir = os.path.join("dataset", person)
        if not os.path.isdir(person_dir): continue
        
        embeddings = []
        for img_name in os.listdir(person_dir):
            img = cv2.imread(os.path.join(person_dir, img_name))
            if img is None: continue
            faces = app.get(img)
            if len(faces) == 1:
                embeddings.append(faces[0].embedding)

        if embeddings:
            database[person] = np.mean(embeddings, axis=0).tolist()  # list thuan, khong phu thuoc numpy version
            print(f"-> Đã xử lý xong dữ liệu của: {person}")

    with open("faces.pkl", "wb") as f:
        # protocol=4 (KHONG dung mac dinh/5) de Jetson Nano (Python 3.6) doc duoc file nay.
        # Python 3.6 chi ho tro toi da pickle protocol 4.
        pickle.dump(database, f, protocol=4)
    print("\n=> THÀNH CÔNG! Đã tạo ra file 'faces.pkl' trên PC.")


def verify_recognition():
    """HÀM THỨ 3: KIỂM TRA ĐỘ CHÍNH XÁC CỦA FILE FACES.PKL NGAY TRÊN PC"""
    print("\n--- [PC] HÀM KIỂM TRA NHẬN DẠNG QUA FILE FACES.PKL ---")
    
    # Kiểm tra xem file pkl đã tồn tại chưa
    if not os.path.exists("faces.pkl"):
        print("LỖI: Không tìm thấy file 'faces.pkl' trên PC!")
        print("Vui lòng chọn mục (2) để huấn luyện dữ liệu trước.")
        return

    # Đọc file pkl
    with open("faces.pkl", "rb") as f:
        database = pickle.load(f)
    print(f"-> Đã nạp thành công file pkl. Hiện có dữ liệu của {len(database)} người.")

    print("Đang khởi tạo webcam và mô hình AI kiểm tra...")
    app = FaceAnalysis(name='buffalo_sc')  # khop voi model dung luc train
    app.prepare(ctx_id=0) # Dùng GPU nếu có, không thì đổi thành -1

    cap = cv2.VideoCapture(0)
    print("=> Đang test nhận dạng... Nhấn [Q] tại cửa sổ camera để đóng test.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Quét khuôn mặt từ webcam PC
        faces = app.get(frame)

        for face in faces:
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            current_embedding = face.embedding
            identity = "Unknown"
            max_sim = -1.0

            # So sánh với dữ liệu vừa nạp từ file pkl
            for name, saved_embedding in database.items():
                saved_embedding = np.array(saved_embedding)
                sim = np.dot(current_embedding, saved_embedding) / (
                    np.linalg.norm(current_embedding) * np.linalg.norm(saved_embedding)
                )
                if sim > max_sim:
                    max_sim = sim
                    if sim > THRESHOLD:
                        identity = name

            # Hiển thị kết quả test lên màn hình PC
            label = f"TEST: {identity} ({max_sim:.2f})"
            color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
            cv2.putText(frame, label, (bbox[0], bbox[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("PC Verification Test", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ==========================================
# PC MENU ĐIỀU KHIỂN CHÍNH
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n================ PC MASTER MENU ================")
        print("1. Chụp ảnh đăng ký khuôn mặt mới (Collect Data)")
        print("2. Huấn luyện & Xuất file faces.pkl (Train & Save)")
        print("3. CHẠY THỬ NHẬN DẠNG QUA FILE PKL (Verify Recognition)")
        print("4. Thoát Chương Trình")
        
        choice = input("Nhập lựa chọn của bạn (1-4): ").strip()

        if choice == '1': 
            collect_face_data()
        elif choice == '2': 
            train_face_embeddings()
        elif choice == '3': 
            verify_recognition()
        elif choice == '4': 
            print("Đã thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ!")