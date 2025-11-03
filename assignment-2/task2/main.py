"""
Road Lane Detection using Canny Edge Detection and Hough Line Transform
Provides both a grid visualization of different configurations and an interactive parameter tuning UI
"""

import cv2
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import Scale, HORIZONTAL, Canvas
from PIL import Image, ImageTk


class LaneDetector:
    """Lane detection using Canny edge detection and Hough line transform"""

    def __init__(self, image_path):
        """Initialize with an image file"""
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError(f"Could not load image: {image_path}")
        self.image_path = image_path

        # Resize for faster processing if too large
        height, width = self.original_image.shape[:2]
        if width > 1280 or height > 720:
            scale = min(1280 / width, 720 / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            self.original_image = cv2.resize(self.original_image, (new_width, new_height))

    def detect_lanes(self, canny_low=50, canny_high=150, hough_threshold=50,
                     hough_min_length=50, hough_max_gap=10, roi_top=50, roi_bottom=100):
        """
        Detect lanes in the image

        Args:
            canny_low: Lower threshold for Canny edge detection
            canny_high: Upper threshold for Canny edge detection
            hough_threshold: Minimum number of votes for Hough line detection
            hough_min_length: Minimum line length for Hough transform
            hough_max_gap: Maximum gap between line segments for Hough transform
            roi_top: ROI top position as percentage from top (0-100)
            roi_bottom: ROI bottom position as percentage from top (0-100)

        Returns:
            result_image: Image with detected lines drawn
            edges: Canny edge detection result
            lines: Detected lines
        """
        # Convert to grayscale
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny edge detection
        edges = cv2.Canny(blurred, canny_low, canny_high)

        # Region of interest (adjustable)
        height, width = edges.shape
        roi_mask = np.zeros_like(edges)
        roi_top_pixel = int(height * roi_top / 100)
        roi_bottom_pixel = int(height * roi_bottom / 100)

        vertices = np.array([
            [0, height],
            [0, roi_top_pixel],
            [width, roi_top_pixel],
            [width, height]
        ], dtype=np.int32)
        cv2.fillPoly(roi_mask, [vertices], 255)
        edges_roi = cv2.bitwise_and(edges, roi_mask)

        # Hough line detection
        lines = cv2.HoughLinesP(
            edges_roi,
            rho=1,
            theta=np.pi / 180,
            threshold=hough_threshold,
            minLineLength=hough_min_length,
            maxLineGap=hough_max_gap
        )

        # Draw detected lines on original image
        result_image = self.original_image.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(result_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw ROI region (optional, for visualization)
        cv2.polylines(result_image, [vertices], True, (255, 0, 0), 2)

        return result_image, edges, lines

    def get_original_image(self):
        """Get original image for display"""
        return self.original_image



class InteractiveParameterTuner:
    """Interactive UI for tuning lane detection parameters"""

    def __init__(self, root, image_path):
        self.root = root
        self.root.title(f"Lane Detection Parameter Tuner - {Path(image_path).name}")
        self.root.geometry("1400x800")

        self.detector = LaneDetector(image_path)
        self.current_result = None

        # Create GUI elements
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """Create GUI widgets"""
        # Control panel (left side)
        control_frame = tk.Frame(self.root, bg="#f0f0f0", width=250)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Title
        title = tk.Label(control_frame, text="Parameter Tuner", font=("Arial", 14, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Canny Low
        tk.Label(control_frame, text="Canny Low:", bg="#f0f0f0").pack(anchor=tk.W)
        self.canny_low = Scale(
            control_frame, from_=1, to=200, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.canny_low.set(50)
        self.canny_low.pack(fill=tk.X)
        self.canny_low_label = tk.Label(control_frame, text="50", bg="#f0f0f0")
        self.canny_low_label.pack(anchor=tk.W)

        # Canny High
        tk.Label(control_frame, text="Canny High:", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.canny_high = Scale(
            control_frame, from_=50, to=500, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.canny_high.set(281)
        self.canny_high.pack(fill=tk.X)
        self.canny_high_label = tk.Label(control_frame, text="281", bg="#f0f0f0")
        self.canny_high_label.pack(anchor=tk.W)

        # Hough Threshold
        tk.Label(control_frame, text="Hough Threshold:", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.hough_threshold = Scale(
            control_frame, from_=10, to=200, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.hough_threshold.set(66)
        self.hough_threshold.pack(fill=tk.X)
        self.hough_threshold_label = tk.Label(control_frame, text="66", bg="#f0f0f0")
        self.hough_threshold_label.pack(anchor=tk.W)

        # Hough Min Length
        tk.Label(control_frame, text="Hough Min Length:", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.hough_min_length = Scale(
            control_frame, from_=10, to=300, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.hough_min_length.set(50)
        self.hough_min_length.pack(fill=tk.X)
        self.hough_min_length_label = tk.Label(control_frame, text="50", bg="#f0f0f0")
        self.hough_min_length_label.pack(anchor=tk.W)

        # Hough Max Gap
        tk.Label(control_frame, text="Hough Max Gap:", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.hough_max_gap = Scale(
            control_frame, from_=1, to=50, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.hough_max_gap.set(10)
        self.hough_max_gap.pack(fill=tk.X)
        self.hough_max_gap_label = tk.Label(control_frame, text="10", bg="#f0f0f0")
        self.hough_max_gap_label.pack(anchor=tk.W)

        # ROI Top
        tk.Label(control_frame, text="ROI Top (%):", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.roi_top = Scale(
            control_frame, from_=0, to=100, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.roi_top.set(38)
        self.roi_top.pack(fill=tk.X)
        self.roi_top_label = tk.Label(control_frame, text="38", bg="#f0f0f0")
        self.roi_top_label.pack(anchor=tk.W)

        # ROI Bottom
        tk.Label(control_frame, text="ROI Bottom (%):", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
        self.roi_bottom = Scale(
            control_frame, from_=0, to=100, orient=HORIZONTAL,
            command=lambda x: self.update_display(), bg="#e0e0e0"
        )
        self.roi_bottom.set(100)
        self.roi_bottom.pack(fill=tk.X)
        self.roi_bottom_label = tk.Label(control_frame, text="100", bg="#f0f0f0")
        self.roi_bottom_label.pack(anchor=tk.W)

        # Info label
        self.info_label = tk.Label(control_frame, text="", bg="#f0f0f0", justify=tk.LEFT, wraplength=220)
        self.info_label.pack(pady=20, anchor=tk.W)

        # Presets
        tk.Label(control_frame, text="Presets:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))

        preset_buttons = [
            ("Conservative", 30, 90, 80, 100, 5),
            ("Balanced", 50, 150, 50, 50, 10),
            ("Aggressive", 20, 60, 30, 30, 20),
        ]

        for name, clow, chigh, hthresh, hlen, hgap in preset_buttons:
            btn = tk.Button(
                control_frame,
                text=name,
                command=lambda c1=clow, c2=chigh, ht=hthresh, hl=hlen, hg=hgap: self.load_preset(c1, c2, ht, hl, hg),
                bg="#d0d0d0",
                relief=tk.RAISED
            )
            btn.pack(fill=tk.X, pady=2)

        # Display panel (right side)
        display_frame = tk.Frame(self.root)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = Canvas(display_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_preset(self, clow, chigh, hthresh, hlen, hgap):
        """Load preset configuration"""
        self.canny_low.set(clow)
        self.canny_high.set(chigh)
        self.hough_threshold.set(hthresh)
        self.hough_min_length.set(hlen)
        self.hough_max_gap.set(hgap)

    def update_display(self):
        """Update the display with current parameters"""
        # Update labels
        self.canny_low_label.config(text=str(int(self.canny_low.get())))
        self.canny_high_label.config(text=str(int(self.canny_high.get())))
        self.hough_threshold_label.config(text=str(int(self.hough_threshold.get())))
        self.hough_min_length_label.config(text=str(int(self.hough_min_length.get())))
        self.hough_max_gap_label.config(text=str(int(self.hough_max_gap.get())))
        self.roi_top_label.config(text=str(int(self.roi_top.get())))
        self.roi_bottom_label.config(text=str(int(self.roi_bottom.get())))

        # Detect lanes
        result, edges, lines = self.detector.detect_lanes(
            canny_low=int(self.canny_low.get()),
            canny_high=int(self.canny_high.get()),
            hough_threshold=int(self.hough_threshold.get()),
            hough_min_length=int(self.hough_min_length.get()),
            hough_max_gap=int(self.hough_max_gap.get()),
            roi_top=int(self.roi_top.get()),
            roi_bottom=int(self.roi_bottom.get())
        )

        num_lines = len(lines) if lines is not None else 0

        # Update info
        info_text = f"Lines detected: {num_lines}\n\n"
        if lines is not None and len(lines) > 0:
            info_text += f"Avg line length: {np.mean([np.sqrt((x2-x1)**2 + (y2-y1)**2) for x1,y1,x2,y2 in lines[:,0]]):.1f}\n"

        self.info_label.config(text=info_text)

        # Display result
        self.display_image(result)

    def display_image(self, image):
        """Display image on canvas"""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width > 1 and canvas_height > 1:
            h, w = image_rgb.shape[:2]
            scale = min(canvas_width / w, canvas_height / h)
            new_width = int(w * scale)
            new_height = int(h * scale)
            image_rgb = cv2.resize(image_rgb, (new_width, new_height))

        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        photo = ImageTk.PhotoImage(pil_image)

        # Update canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo


def main():
    """Main function"""
    images_dir = Path(__file__).parent / "images"
    image_files = sorted(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")))

    if not image_files:
        print(f"No images found in {images_dir}")
        return

    print("Lane Detection - Canny + Hough Transform")
    print("=" * 50)
    print(f"Found {len(image_files)} image(s)")

    if len(image_files) > 0:
        root = tk.Tk()
        app = InteractiveParameterTuner(root, str(image_files[0]))
        root.mainloop()
    else:
        print("No images found to process")


if __name__ == "__main__":
    main()

