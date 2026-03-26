# ptz/controller.py
import threading
import time
from v4l2py import Device

class PTZController:
    def __init__(self, device_path="/dev/video0"):
        self.device_path = device_path
        self.device = Device(device_path)
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        self.active_control = None
        self.step = 0
        self.min_val = 0
        self.max_val = 0
        self.interval = 0.05  # original ~25s full pan

        # detect capabilities
        self.capabilities = self.detect_capabilities()

    def _get_ctrl(self, name):
        if self.device.controls is None or name not in self.device.controls:
            return 0
        return self.device.controls[name].value

    def _set_ctrl(self, name, value):
        if self.device.controls is None or name not in self.device.controls:
            return
        self.device.controls[name].value = int(value)

    def detect_capabilities(self):
        ctrls = self.device.controls
        if ctrls is None:
            ctrls = {}
        return {
            "pan": "pan_absolute" in ctrls,
            "tilt": "tilt_absolute" in ctrls,
            "zoom": "zoom_absolute" in ctrls
        }

    def _loop(self):
        while self.running:
            with self.lock:
                ctrl = self.active_control
                step = self.step
                min_val = self.min_val
                max_val = self.max_val

            current = self._get_ctrl(ctrl)
            new = max(min(current + step, max_val), min_val)

            self._set_ctrl(ctrl, new)
            time.sleep(self.interval)

    def start(self, control, step, min_val, max_val):
        self.stop()  # single active movement

        with self.lock:
            self.active_control = control
            self.step = step
            self.min_val = min_val
            self.max_val = max_val

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=0.2)
        self.thread = None
