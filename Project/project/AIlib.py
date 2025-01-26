import cv2
import numpy as np
from ortools.linear_solver import pywraplp

def computer_gradients(img):
    # Tính toán gradient của ảnh sử dụng phép toán Sobel
    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    
    # Tính toán độ lớn gradient và góc gradient
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    grad_angle = np.arctan2(grad_y, grad_x) * (180.0 / np.pi) % 180
    return grad_mag, grad_angle

def hog_feature(img, cell_size=(8,8), block_size=(2,2), bins=9):
    # Lấy kích thước của ảnh
    height, width = img.shape
    cells_x = width // cell_size[1]
    cells_y = height // cell_size[0]
    
    # Nếu kích thước ảnh không chia hết cho kích thước ô, thay đổi kích thước ảnh
    if width % cell_size[1] != 0 or height % cell_size[0] != 0:
        new_width = (width // cell_size[1]) * cell_size[1]
        new_height = (height // cell_size[0]) * cell_size[0]
        img = cv2.resize(img, (new_width, new_height))
        height, width = img.shape
        cells_x = width // cell_size[1]
        cells_y = height // cell_size[0]
    
    # Tính toán các đặc trưng HOG (Histogram of Oriented Gradients)
    mag, ang = computer_gradients(img)
    cell_histograms = np.zeros((cells_y, cells_x, bins))
    
    # Tính toán histogram cho mỗi ô
    for i in range(cells_y):
        for j in range(cells_x):
            cell_mag = mag[i*cell_size[0]:(i+1)*cell_size[0], j*cell_size[1]:(j+1)*cell_size[1]]
            cell_angle = ang[i*cell_size[0]:(i+1)*cell_size[0], j*cell_size[1]:(j+1)*cell_size[1]]
            for m in range(cell_size[0]):
                for n in range(cell_size[1]):
                    bin_idx = int(cell_angle[m, n] // (180 / bins))
                    cell_histograms[i, j, bin_idx] += cell_mag[m, n]
    
    # Tính toán histogram cho các block
    block_histograms = []
    for i in range(cells_y - block_size[0] + 1):
        for j in range(cells_x - block_size[1] + 1):
            block = cell_histograms[i:i + block_size[0], j:j + block_size[1]]
            block_histograms.append(block.flatten())
    
    # Trả về các histogram block đã được làm phẳng
    return np.array(block_histograms).flatten()

import numpy as np
from scipy.spatial import distance
from ortools.linear_solver import pywraplp


def Euclidean_Distance(x, y):
    """
    Tính khoảng cách Euclidean giữa hai điểm.
    """
    return np.sqrt(np.sum((x - y) ** 2))


class BallTree:
    """
    Cấu trúc cây BallTree để tối ưu hóa việc tìm kiếm lân cận.
    """
    def __init__(self, data, leaf_size=10):
        self.data = np.array(data)
        self.leaf_size = leaf_size
        self.tree = self.build_tree(self.data)

    def build_tree(self, data):
        """
        Xây dựng cây BallTree dựa trên dữ liệu.
        """
        if len(data) <= self.leaf_size:
            return {"leaf": True, "data": data}
        else:
            # Chia dữ liệu dựa trên trung điểm
            center = np.mean(data, axis=0)
            distances = np.linalg.norm(data - center, axis=1)
            median_distance = np.median(distances)

            left_data = data[distances <= median_distance]
            right_data = data[distances > median_distance]

            return {
                "leaf": False,
                "center": center,
                "radius": median_distance,
                "left": self.build_tree(left_data),
                "right": self.build_tree(right_data),
            }

    def query(self, point, k=1):
        """
        Tìm k điểm gần nhất với một điểm cho trước.
        """
        return self._query(self.tree, point, k, [])

    def _query(self, node, point, k, heap):
        if node["leaf"]:
            # Tính khoảng cách và thêm vào heap
            for data_point in node["data"]:
                dist = Euclidean_Distance(point, data_point)
                heap.append((dist, data_point))
            heap.sort(key=lambda x: x[0])
            return heap[:k]
        else:
            # Kiểm tra cây con nào gần hơn
            left_dist = Euclidean_Distance(point, node["left"]["center"])
            right_dist = Euclidean_Distance(point, node["right"]["center"])

            # Tìm kiếm trong cây gần hơn trước
            if left_dist < right_dist:
                heap = self._query(node["left"], point, k, heap)
                if len(heap) < k or right_dist < heap[-1][0]:
                    heap = self._query(node["right"], point, k, heap)
            else:
                heap = self._query(node["right"], point, k, heap)
                if len(heap) < k or left_dist < heap[-1][0]:
                    heap = self._query(node["left"], point, k, heap)

            heap.sort(key=lambda x: x[0])
            return heap[:k]


class KNNBallTree:
    """
    Mô hình KNN sử dụng cấu trúc cây BallTree.
    """
    def __init__(self, k=5, metric="euclidean", leaf_size=10):
        self.k = k
        self.metric = metric
        self.leaf_size = leaf_size
        self.ball_tree = None
        self.labels = None

    def fit(self, features, labels):
        """
        Huấn luyện mô hình KNN với BallTree.
        """
        self.ball_tree = BallTree(features, leaf_size=self.leaf_size)
        self.labels = np.array(labels)

    def predict(self, feature_vector):
        """
        Dự đoán nhãn của vector đặc trưng.
        """
        if self.ball_tree is None or self.labels is None:
            raise ValueError("Model chưa được huấn luyện.")

        # Tìm k điểm gần nhất
        nearest_neighbors = self.ball_tree.query(feature_vector, k=self.k)
        indices = [np.where((self.ball_tree.data == nn[1]).all(axis=1))[0][0] for nn in nearest_neighbors]
        nearest_labels = self.labels[indices]

        # Bầu chọn nhãn xuất hiện nhiều nhất
        unique, counts = np.unique(nearest_labels, return_counts=True)
        return unique[np.argmax(counts)]


class KNN_BallTree_Optimizer:
    """
    Tối ưu hóa việc lựa chọn k sử dụng OR-Tools.
    """
    def __init__(self, data, labels, k_values=[3, 5, 7, 9]):
        self.data = data
        self.labels = labels
        self.k_values = k_values

    def optimize_knn(self):
        """
        Tối ưu hóa giá trị k sử dụng OR-Tools.
        """
        # Tạo solver OR-Tools
        solver = pywraplp.Solver.CreateSolver("SCIP")

        # Biến quyết định cho mỗi k
        k_var = {}
        for k in self.k_values:
            k_var[k] = solver.IntVar(0, 1, f"k_{k}")

        # Đặt mục tiêu tối thiểu hóa khoảng cách (hàm mục tiêu có thể thay đổi)
        objective = solver.Objective()
        for k in self.k_values:
            objective.SetCoefficient(k_var[k], 1)
        objective.SetMinimization()

        # Ràng buộc: Chỉ chọn duy nhất một giá trị k
        constraint = solver.Constraint(1, 1)
        for k in self.k_values:
            constraint.SetCoefficient(k_var[k], 1)

        # Giải quyết bài toán tối ưu hóa
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            for k in self.k_values:
                if k_var[k].solution_value() == 1:
                    return k
        else:
            raise ValueError("Không tìm thấy giải pháp tối ưu.")