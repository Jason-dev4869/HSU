import tkinter as tk
from tkinter import filedialog, Label, Button, IntVar, Scale, Frame
from PIL import Image, ImageTk
import cv2
import numpy as np
import AIlib as al

def preproces_img(img_path, target_size=(256, 256), lv=16):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Unable to read image at {img_path}")
        return None

    img = np.uint8(img / lv) * lv
    img = cv2.resize(img, target_size)

    dog_face_cas = cv2.CascadeClassifier(r'D:\HSU_Code\Py\project\dog_face.xml')
    cat_face_cas = cv2.CascadeClassifier(r'D:\HSU_Code\Py\project\haarcascade_frontalcatface_extended.xml')

    dog_faces = dog_face_cas.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    cat_faces = cat_face_cas.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(dog_faces) > 0:
        return "dog"
    elif len(cat_faces) > 0:
        return "cat"
    else:
        return "unknown"

class CatDogClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat-Dog Classifier")

        self.selected_image_path = None
        self.result_label = None

        self.label = Label(root, text="Choose an image to classify", font=("Arial", 14))
        self.label.pack(pady=10)

        frame = Frame(self.root)
        frame.pack(pady=10)

        self.img_label = Label(frame)
        self.img_label.pack(side="left", padx=10)

        self.preprocessed_img_label = Label(frame)
        self.preprocessed_img_label.pack(side="right", padx=10)

        self.choose_btn = Button(root, text="Choose Image", command=self.choose_image)
        self.choose_btn.pack(pady=10)

        self.classify_btn = Button(root, text="Classify", command=self.classify_image)
        self.classify_btn.pack(pady=10)

        self.result_label = Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def choose_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
        )
        if self.selected_image_path:
            img_pil = Image.open(self.selected_image_path)
            img_pil = img_pil.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img_pil)
            self.img_label.configure(image=img_tk)
            self.img_label.image = img_tk

    def preprocess_for_display(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None

        img_resized = cv2.resize(img, (256, 256))
        img_normalized = np.uint8(img_resized / 16) * 16  # Tiền xử lý
        img_pil = Image.fromarray(img_normalized)
        return img_pil

    def classify_image(self):
        if not self.selected_image_path:
            self.result_label.config(text="Please select an image first!", fg="red")
            return

        result = preproces_img(self.selected_image_path)

        # Hiển thị ảnh tiền xử lý
        processed_img = self.preprocess_for_display(self.selected_image_path)
        if processed_img is not None:
            img_tk = ImageTk.PhotoImage(processed_img)
            self.preprocessed_img_label.configure(image=img_tk)
            self.preprocessed_img_label.image = img_tk

        # Hiển thị kết quả
        if result == "dog":
            self.result_label.config(text="The image is classified as: Dog", fg="green")
        elif result == "cat":
            self.result_label.config(text="The image is classified as: Cat", fg="blue")
        else:
            self.result_label.config(text="Unable to classify the image", fg="orange")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatDogClassifierApp(root)
    root.mainloop()