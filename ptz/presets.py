# ptz/presets.py
class PTZPresetManager:
    def __init__(self, controller):
        self.controller = controller
        self.presets = {}

    def save_preset(self, name):
        caps = self.controller.capabilities
        data = {}
        if caps.get("pan", False):
            data["pan"] = self.controller._get_ctrl("pan_absolute")
        if caps.get("tilt", False):
            data["tilt"] = self.controller._get_ctrl("tilt_absolute")
        if caps.get("zoom", False):
            data["zoom"] = self.controller._get_ctrl("zoom_absolute")
        self.presets[name] = data

    def load_preset(self, name):
        if name not in self.presets:
            return
        data = self.presets[name]
        if "pan" in data:
            self.controller._set_ctrl("pan_absolute", data["pan"])
        if "tilt" in data:
            self.controller._set_ctrl("tilt_absolute", data["tilt"])
        if "zoom" in data:
            self.controller._set_ctrl("zoom_absolute", data["zoom"])
