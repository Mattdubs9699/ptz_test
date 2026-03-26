# ptz/actions.py
from .controller import PTZController
from .presets import PTZPresetManager

ptz = PTZController()
preset_mgr = PTZPresetManager(ptz)

# PAN
def pan_left_down():
    if not ptz.capabilities.get("pan", False):
        return
    ptz.start("pan_absolute", -3600, -36000, 36000)

def pan_right_down():
    if not ptz.capabilities.get("pan", False):
        return
    ptz.start("pan_absolute", 3600, -36000, 36000)

# TILT
def tilt_up_down():
    if not ptz.capabilities.get("tilt", False):
        return
    ptz.start("tilt_absolute", 3600, -36000, 36000)

def tilt_down_down():
    if not ptz.capabilities.get("tilt", False):
        return
    ptz.start("tilt_absolute", -3600, -36000, 36000)

# ZOOM
def zoom_in_down():
    if not ptz.capabilities.get("zoom", False):
        return
    ptz.start("zoom_absolute", 1, 1, 5)

def zoom_out_down():
    if not ptz.capabilities.get("zoom", False):
        return
    ptz.start("zoom_absolute", -1, 1, 5)

# PRESETS
def save_preset(name):
    preset_mgr.save_preset(name)

def load_preset(name):
    preset_mgr.load_preset(name)

# STOP
def stop_all():
    ptz.stop()
