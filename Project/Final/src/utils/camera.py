import cv2


class CameraStream:
    """Safe wrapper for hardware video capture processing."""

    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        # Đã sửa thành isOpened()
        if not self.cap.isOpened():
            print(f"[WARNING] Failed to open video source device ID: {source}")

    def get_frame(self):
        """Reads and captures a single frame from the camera stream."""
        # Đã sửa thành isOpened()
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return True, frame
        return False, None

    def release(self):
        """Safely deallocates video capture hardware locks."""
        # Đã sửa thành isOpened()
        if self.cap.isOpened():
            self.cap.release()