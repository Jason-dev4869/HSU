import AIlib as al
import cv2
import numpy as np
import os
import zipfile
import urllib.request

def extract_face_features(face_region):
    """Trích xuất đặc trưng khuôn mặt từ ảnh đã được cắt (grayscale)."""
    # Đảm bảo ảnh vùng mặt là grayscale trước khi tính HOG
    if len(face_region.shape) == 3:
        face_region = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)

    # Trích xuất đặc trưng HOG từ vùng mặt
    hog_face = al.hog_feature(face_region)
    return hog_face

def extract_animal_features(animal_region):
    """Trích xuất đặc trưng động vật (chó, mèo) từ ảnh đã được cắt (grayscale)."""
    # Đảm bảo ảnh vùng động vật là grayscale trước khi tính HOG
    if len(animal_region.shape) == 3:
        animal_region = cv2.cvtColor(animal_region, cv2.COLOR_BGR2GRAY)

    # Trích xuất đặc trưng HOG từ vùng động vật
    hog_animal = al.hog_feature(animal_region)
    return hog_animal

def preproces_img(img_path, target_size=(256, 256), lv=16):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Unable to read image at {img_path}")
        return []
    
    img = np.uint8(img / lv) * lv
    img = cv2.resize(img, target_size)
    
    # Trích xuất đặc trưng từ khuôn mặt và động vật
    face_features = []
    animal_features = []
    
    # Tải mô hình Haar Cascade cho khuôn mặt chó và mèo
    dog_face_cas = cv2.CascadeClassifier(r'D:\HSU_Code\Py\project\dog_face.xml')  # Đường dẫn đến tệp dog_face.xml
    cat_face_cas = cv2.CascadeClassifier(r'D:\HSU_Code\Py\project\haarcascade_frontalcatface_extended.xml')  # Đường dẫn đến tệp cat_face.xml
    
    # Phát hiện khuôn mặt chó trong ảnh
    dog_faces = dog_face_cas.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in dog_faces:
        dog_face_region = img[y:y+h, x:x+w]
        face_features.append(extract_face_features(dog_face_region))  # Trích xuất đặc trưng khuôn mặt chó
        
        # Giả sử bạn cũng muốn trích xuất các đặc trưng của động vật (mắt chó)
        eyes = dog_face_cas.detectMultiScale(dog_face_region)
        for (ex, ey, ew, eh) in eyes:
            eye_region = dog_face_region[ey:ey+eh, ex:ex+ew]
            animal_features.append(extract_animal_features(eye_region))  # Giả sử mắt cũng có thể coi là thuộc tính động vật

    # Phát hiện khuôn mặt mèo trong ảnh
    cat_faces = cat_face_cas.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in cat_faces:
        cat_face_region = img[y:y+h, x:x+w]
        face_features.append(extract_face_features(cat_face_region))  # Trích xuất đặc trưng khuôn mặt mèo
        
        # Giả sử bạn cũng muốn trích xuất các đặc trưng của động vật (mắt mèo)
        eyes = cat_face_cas.detectMultiScale(cat_face_region)
        for (ex, ey, ew, eh) in eyes:
            eye_region = cat_face_region[ey:ey+eh, ex:ex+ew]
            animal_features.append(extract_animal_features(eye_region))  # Giả sử mắt cũng có thể coi là thuộc tính động vật

    # Trả về tất cả các đặc trưng đã trích xuất từ khuôn mặt chó và mèo
    return face_features + animal_features

def create_training_data(data_dir, output, lv=16):
    # Tạo dữ liệu huấn luyện
    label_map = {"cats": 1, "dogs": 0}  # Đánh dấu nhãn cho mèo và chó
    train_data = []
    feature_lengths = []   # Lưu trữ độ dài các đặc trưng

    for label in label_map.keys():
        folder = os.path.join(data_dir, label).replace(os.sep, '/')
        print(f"Checking folder: {folder}")   # In thông báo khi kiểm tra thư mục
        if os.path.exists(folder.replace('/', os.sep)):  # Kiểm tra nếu thư mục tồn tại
            # List all files in the folder
            print(f"Listing all files in folder: {folder}")
            try:
                files = os.listdir(folder.replace('/', os.sep))
                print(f"Files found: {files}")  # In danh sách tất cả tệp
                # Filter image files
                image_files = [file for file in files if file.lower().endswith((".jpg", ".png"))]
                print(f"Image files found: {image_files}")
                for file in image_files:
                    img_path = os.path.join(folder, file).replace(os.sep, '/')
                    try:
                        hog_features = preproces_img(img_path.replace('/', os.sep), lv=lv)
                        print(f"Processed {img_path} - Features: {len(hog_features)}")  # In số đặc trưng đã trích xuất
                        if hog_features:  # Kiểm tra nếu hog_features không rỗng
                            feature_lengths.append(len(hog_features))
                            for feature in hog_features:
                                train_data.append([feature, label_map[label]])
                    except Exception as e:
                        print(f"Error processing {img_path}: {e}")
            except Exception as e:
                print(f"Error listing files in {folder}: {e}")
        else:
            print(f"Folder does not exist: {folder}")
    
    # Kiểm tra số lượng dữ liệu huấn luyện
    print(f"Number of training samples: {len(train_data)}")
    
    # Đảm bảo rằng tất cả các đặc trưng có cùng độ dài
    max_length = max(feature_lengths)
    padded_features = []

    for feature, label in train_data:
        # Làm phẳng đặc trưng để đảm bảo là mảng một chiều
        feature = np.ravel(feature)
        
        # Nếu độ dài đặc trưng nhỏ hơn max_length, thêm padding
        if len(feature) < max_length:
            # Padding đặc trưng để có độ dài bằng max_length
            padded_feature = np.pad(feature, (0, max_length - len(feature)), mode='constant', constant_values=0)
        else:
            # Nếu độ dài đặc trưng lớn hơn max_length, cắt nó lại
            padded_feature = feature[:max_length]
            
        padded_features.append(padded_feature)

    # Chuyển đổi thành mảng NumPy
    features = np.array(padded_features)
    labels = np.array([label for _, label in train_data])
    
    # Lưu dữ liệu vào npz nếu có dữ liệu
    if len(features) > 0:
        np.savez(output, features=features, labels=labels)
        print(f"Training data saved to {output}")
    else:
        print("No training data to save!")

def train_knn_balltree(npz_file):
    # Tải dữ liệu huấn luyện
    data_dict = np.load(npz_file)
    data = data_dict['features']
    label = data_dict['labels']

    # Huấn luyện KNN với BallTree
    optimizer = al.KNN_BallTree_Optimizer(data, label)
    optimal_k = optimizer.optimize_knn()
    print(f"Optimal k found: {optimal_k}")

    return optimal_k, label, data

def download_and_extract_data(url, extract_to="cats_and_dogs_filtered"):
    # Tải và giải nén bộ dữ liệu từ URL
    if not os.path.exists(extract_to):
        print(f"Downloading data from {url}...")
        urllib.request.urlretrieve(url, "cats_and_dogs_filtered.zip")
        with zipfile.ZipFile("cats_and_dogs_filtered.zip", 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Data extracted successfully.")
    else:
        print(f"Data already exists in {extract_to}.")

def get_correct_data_dir(extracted_dir):
    """
    Kiểm tra cấu trúc thư mục và trả về đường dẫn chính xác đến thư mục train.
    """
    for root, dirs, files in os.walk(extracted_dir):
        if 'train' in dirs and 'validation' in dirs:
            train_dir = os.path.join(root, 'train')
            validation_dir = os.path.join(root, 'validation')
            print(f"Detected correct training directory: {train_dir}")
            return train_dir
    raise FileNotFoundError("Could not find the correct 'train' directory structure.")

if __name__ == "__main__":
    data_url = "https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
    output = "training_data.npz"

    print("Downloading and extracting data...")  
    download_and_extract_data(data_url)

    # Xác định đường dẫn chính xác
    base_dir = "cats_and_dogs_filtered"
    data_dir = get_correct_data_dir(base_dir)

    print("Creating training data...")
    create_training_data(data_dir, output, lv=16)

    print("Training KNN BallTree models...")
    optimal_k, label, data = train_knn_balltree(output)

    print("Models trained and ready for use.")