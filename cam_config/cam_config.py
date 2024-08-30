import os
import subprocess

class CameraConfigurator:
    def __init__(self, video_device, width=640, height=480, pixel_format='YUYV'):
        self.video_device = video_device
        self.width = width
        self.height = height
        self.pixel_format = pixel_format

    def _get_camera_info(self):
        try:
            result = subprocess.run(
                ["v4l2-ctl", "-d", self.video_device, "--all"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            print("=== Camera Info ===")
            print(result.stdout)
            print("===================")
            return result.stdout
        except Exception as e:
            print(f"Failed to retrieve camera info: {e}")
            return ""

    def adjust_camera_settings_for_opencv(self):
        print("Adjusting camera settings for OpenCV compatibility...")
        
        # Adjust pixel format and resolution based on external settings
        command = f"v4l2-ctl -d {self.video_device} --set-fmt-video=width={self.width},height={self.height},pixelformat={self.pixel_format}"
        print(f"Setting format: {command}")
        os.system(command)
        
        # Verify the resolution was set correctly
        camera_info = self._get_camera_info()
        if f"Width/Height      : {self.width}/{self.height}" not in camera_info:
            print(f"Warning: Resolution {self.width}x{self.height} was not applied. The camera might not support this resolution.")
        
        print("Camera settings adjusted.")

    def apply_camera_settings(self, camera_settings):
        print("Applying modifiable controls to the camera...")
        modifiable_controls = {
            "brightness": camera_settings.brightness,
            "contrast": camera_settings.contrast,
            "saturation": camera_settings.saturation,
            "hue": camera_settings.hue,
            "white_balance_automatic": int(camera_settings.white_balance_automatic),
            "gamma": camera_settings.gamma,
            "gain": camera_settings.gain,
            "power_line_frequency": camera_settings.power_line_frequency,
            "sharpness": camera_settings.sharpness,
            "backlight_compensation": camera_settings.backlight_compensation,
            "auto_exposure": camera_settings.auto_exposure,
            "exposure_dynamic_framerate": int(camera_settings.exposure_dynamic_framerate),
        }
        
        for control, value in modifiable_controls.items():
            command = f"v4l2-ctl -d {self.video_device} --set-ctrl {control}={value}"
            print(f"Running command: {command}")
            os.system(command)
