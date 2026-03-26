# ptz/devices.py
import os

def list_video_devices():
    """
    Return a list of dicts with 'name' and 'path' for /dev/video* devices
    """
    devices = []
    for entry in os.listdir("/dev"):
        if entry.startswith("video"):
            path = os.path.join("/dev", entry)
            devices.append({
                "name": entry,
                "path": path
            })
    return devices
