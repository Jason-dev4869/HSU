import sys
from pathlib import Path
import numpy as np
import cv2
import tensorflow as tf
import keras


class MaskPredictor:
    """Handles deep learning model loading, frame preprocessing, and inference."""

    def __init__(self, model_path="model/best_model.keras"):
        self.model_path = Path(model_path)
        
        if not self.model_path.exists():
            print(f"[ERROR] Trained model artifact not found at: {self.model_path}")
            print("Please run train.py first to generate the model.")
            sys.exit(1)
            
        print(f"[INFO] Loading Keras model from {self.model_path}...")
        self.model = keras.models.load_model(self.model_path)
        
        # Explicitly matching the 6 classes from the training phase
        self.class_mapping = {
            0: "Incorrect Mask (MC)",
            1: "Incorrect Mask (MMC)",
            2: "With Mask (Complex)",
            3: "With Mask (Simple)",
            4: "Without Mask (Complex)",
            5: "Without Mask (Simple)"
        }
        
        # Color coding for UI overlays (HEX formats)
        self.class_colors = {
            0: "#FFC107",  # Yellow
            1: "#FF9800",  # Orange
            2: "#4CAF50",  # Green
            3: "#2ECC71",  # Light Green
            4: "#E74C3C",  # Red
            5: "#C0392B"   # Dark Red
        }

    def predict(self, bgr_frame):
        """
        Executes inference on a raw BGR frame from OpenCV.
        Returns:
            class_idx (int): Predicted class index.
            label (str): Human-readable class name.
            confidence (float): Probability score.
            color (str): Hex color bound to the class state.
        """
        # Convert BGR (OpenCV standard) to RGB
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        
        # Input shape mapping (224, 224, 3)
        resized_frame = cv2.resize(rgb_frame, (224, 224))
        
        # Standard MobileNetV2 preprocessing scale [-1, 1]
        preprocessed = keras.applications.mobilenet_v2.preprocess_input(resized_frame)
        
        # Expand dimensions to create batch tensor (1, 224, 224, 3)
        input_tensor = np.expand_dims(preprocessed, axis=0)
        
        # Run execution loop
        predictions = self.model.predict(input_tensor, verbose=0)[0]
        class_idx = np.argmax(predictions)
        confidence = predictions[class_idx]
        
        return (
            class_idx, 
            self.class_mapping[class_idx], 
            confidence, 
            self.class_colors[class_idx]
        )