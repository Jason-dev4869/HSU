import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from src.utils.camera import CameraStream
from src.inference.predictor import MaskPredictor


class AppWindow:
    """Builds and orchestrates the desktop UI layout and refresh loops."""

    def __init__(self, window_title="Face Mask Detection Live System"):
        self.window = tk.Tk()
        self.window.title(window_title)
        self.window.geometry("950x620")
        self.window.configure(bg="#2C3E50")  # Dark Slate theme

        # Dependency Injection of Core Systems
        self.camera = CameraStream(source=0)
        self.predictor = MaskPredictor()

        # Build Layout Elements
        self._initialize_layout()
        
        # Refresh rate configuration (~60 FPS target loop cap, bound by inference time)
        self.loop_delay = 15 
        self._update_application_loop()

    def _initialize_layout(self):
        """Draws components using clean Tkinter frame hierarchies."""
        # Top Header Banner
        header = tk.Label(
            self.window, 
            text="REAL-TIME FACE MASK MONITORING SYSTEM", 
            font=("Helvetica", 16, "bold"), 
            fg="#ECF0F1", 
            bg="#34495E", 
            pady=12
        )
        header.pack(fill=tk.X)

        # Main Containers
        container = tk.Frame(self.window, bg="#2C3E50")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Container - Canvas for video streaming
        self.canvas = tk.Canvas(container, width=640, height=480, bg="#1A252F", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right Container - Analytics and Status Sidebar
        sidebar = tk.Frame(container, width=240, bg="#34495E", padx=15, pady=20)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))

        # Metadata Metrics Labels
        lbl_section = tk.Label(
            sidebar, 
            text="MONITORING DIAGNOSTICS", 
            font=("Helvetica", 11, "bold"), 
            fg="#BDC3C7", 
            bg="#34495E"
        )
        lbl_section.pack(anchor=tk.W, pady=(0, 15))

        tk.Label(sidebar, text="Detected Classification:", font=("Helvetica", 10), fg="#ECF0F1", bg="#34495E").pack(anchor=tk.W)
        self.lbl_status = tk.Label(
            sidebar, 
            text="Connecting...", 
            font=("Helvetica", 13, "bold"), 
            fg="#F1C40F", 
            bg="#34495E", 
            wraplength=200, 
            justify="left"
        )
        self.lbl_status.pack(anchor=tk.W, pady=(5, 15))

        self.lbl_confidence = tk.Label(
            sidebar, 
            text="Confidence: 0.0%", 
            font=("Helvetica", 11), 
            fg="#ECF0F1", 
            bg="#34495E"
        )
        self.lbl_confidence.pack(anchor=tk.W, pady=(0, 20))

        # UI Separator line
        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', pady=10)

        # App operational tips
        tips = (
            "System Information:\n"
            "- Green: Safe / Mask Correct\n"
            "- Orange/Yellow: Incorrect Mask\n"
            "- Red: Danger / No Mask"
        )
        lbl_tips = tk.Label(
            sidebar, 
            text=tips, 
            font=("Helvetica", 9, "italic"), 
            fg="#95A5A6", 
            bg="#34495E", 
            justify="left"
        )
        lbl_tips.pack(side=tk.TOP, anchor=tk.W, pady=20)

        # Bottom exit control call
        btn_exit = tk.Button(
            sidebar, 
            text="SHUTDOWN SYSTEM", 
            command=self._on_window_close, 
            font=("Helvetica", 10, "bold"), 
            bg="#E74C3C", 
            fg="white", 
            activebackground="#C0392B", 
            activeforeground="white", 
            bd=0, 
            pady=10
        )
        btn_exit.pack(side=tk.BOTTOM, fill=tk.X)

        # Trap OS Window Close Events
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)

    def _update_application_loop(self):
        """Core application runtime execution loop."""
        success, frame = self.camera.get_frame()
        if success:
            # Process AI Inference Core
            _, label, confidence, hex_color = self.predictor.predict(frame)
            
            # Dynamic UI Component Updates
            self.lbl_status.config(text=label.upper(), fg=hex_color)
            self.lbl_confidence.config(text=f"Confidence: {confidence * 100:.1f}%")
            
            # Mirror the camera view frame for comfortable self-viewing feedback
            frame = cv2.flip(frame, 1)
            
            # Convert raw frame to UI compatible format
            rgb_conversion = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_conversion)
            pil_image = pil_image.resize((640, 480), Image.Resampling.LANCZOS)
            
            # Retain a reference memory allocation block to prevent Garbage Collection cleanup drops
            self.current_photo = ImageTk.PhotoImage(image=pil_image)
            self.canvas.create_image(0, 0, image=self.current_photo, anchor=tk.NW)
            
        # Register next callback execution instance
        self.window.after(self.loop_delay, self._update_application_loop)

    def _on_window_close(self):
        """Graceful resource teardown on exit command."""
        print("[INFO] Shutting down application routines cleanly...")
        self.camera.release()
        self.window.destroy()

    def launch(self):
        """Starts main loop UI context execution."""
        self.window.mainloop()