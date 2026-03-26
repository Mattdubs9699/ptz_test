#!/usr/bin/env python3
import cv2
import numpy as np
from ptz.controller import PTZController
from ptz.devices import list_video_devices
import time
from pathlib import Path

# -----------------------------
# Camera selection
# -----------------------------
cameras = list_video_devices()
print("Detected cameras:")
for i, cam in enumerate(cameras):
    print(f"{i}: {cam['path']}")

while True:
    try:
        selection = int(input("Enter the number of the camera you want to use: "))
        if 0 <= selection < len(cameras):
            break
    except ValueError:
        pass
    print("Invalid selection, try again.")

cam_path = cameras[selection]["path"]
print(f"\nUsing camera: {cam_path}\n")

# -----------------------------
# Initialize PTZ controller
# -----------------------------
ptz = PTZController(cam_path)

print("PTZ Capabilities:")
for k, v in ptz.capabilities.items():
    print(f"  {k}: {'Yes' if v else 'No'}")

# For software zoom fallback if hardware zoom is not available
use_software_zoom = not ptz.capabilities.get("zoom", False)
zoom_level = 1.0  # 1.0 = original size
zoom_step = 0.1   # each zoom increment

# -----------------------------
# OpenCV video capture
# -----------------------------
cap = cv2.VideoCapture(str(cam_path))
if not cap.isOpened():
    raise RuntimeError(f"Cannot open camera {cam_path}")

# Get frame dimensions
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Failed to read from camera")
h, w = frame.shape[:2]

# -----------------------------
# Control loop
# -----------------------------
print("\nArrow keys to control:")
print("  Left/Right → Pan (if supported)")
print("  Up/Down → Zoom (hardware or software)")
print("Press 'q' to quit.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display_frame = frame.copy()

    # Apply software zoom if necessary
    if use_software_zoom and zoom_level != 1.0:
        center_x, center_y = w // 2, h // 2
        new_w, new_h = int(w / zoom_level), int(h / zoom_level)
        x1 = max(center_x - new_w // 2, 0)
        y1 = max(center_y - new_h // 2, 0)
        x2 = min(x1 + new_w, w)
        y2 = min(y1 + new_h, h)
        crop = display_frame[y1:y2, x1:x2]
        display_frame = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)

    cv2.imshow("PTZ Test Preview", display_frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord("q"):
        break
    elif key == 81:  # Left arrow
        if ptz.capabilities.get("pan"):
            ptz.pan(-10)
    elif key == 83:  # Right arrow
        if ptz.capabilities.get("pan"):
            ptz.pan(10)
    elif key == 82:  # Up arrow
        if ptz.capabilities.get("zoom"):
            ptz.zoom(1)
        elif use_software_zoom:
            zoom_level = min(zoom_level + zoom_step, 3.0)  # max 3x zoom
    elif key == 84:  # Down arrow
        if ptz.capabilities.get("zoom"):
            ptz.zoom(-1)
        elif use_software_zoom:
            zoom_level = max(zoom_level - zoom_step, 1.0)  # min 1x zoom

cap.release()
cv2.destroyAllWindows()
print("PTZ test finished.")
