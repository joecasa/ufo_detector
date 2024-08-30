from dataclasses import dataclass
import cv2
import os
import subprocess

@dataclass
class CameraSettings:
    brightness: int = 10
    contrast: int = 40
    saturation: int = 70
    hue: int = 0
    white_balance_automatic: bool = True
    gamma: int = 150
    gain: int = 5
    power_line_frequency: int = 2  # 60 Hz for North American NTSC
    sharpness: int = 4
    backlight_compensation: int = 1
    auto_exposure: int = 3  # Aperture Priority Mode
    exposure_dynamic_framerate: bool = False

@dataclass
class V4LSettings:
    device_path: str
    camera_settings: CameraSettings
    pixel_format: str = "MJPG"  # Default to MJPG, but can be adjusted externally
    width: int = 1280
    height: int = 720

class HailoObjectDetector:
    def __init__(self, video_device: str, camera_settings: CameraSettings, v4l_settings: V4LSettings):
        self.video_device = video_device
        self.camera_settings = camera_settings
        self.v4l_settings = v4l_settings
        self.model_path = model_path
        self.capture = None
        print(f"Initializing HailoObjectDetector for video device: {self.video_device} with resolution {self.v4l_settings.width}x{self.v4l_settings.height} and pixel format {self.v4l_settings.pixel_format}")
        self._adjust_camera_settings_for_opencv()
    
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

    def _adjust_camera_settings_for_opencv(self):
        print("Adjusting camera settings for OpenCV compatibility...")
        
        # Adjust pixel format and resolution based on external settings
        command = f"v4l2-ctl -d {self.video_device} --set-fmt-video=width={self.v4l_settings.width},height={self.v4l_settings.height},pixelformat={self.v4l_settings.pixel_format}"
        print(f"Setting format: {command}")
        os.system(command)
        
        # Verify the resolution was set correctly
        camera_info = self._get_camera_info()
        if f"Width/Height      : {self.v4l_settings.width}/{self.v4l_settings.height}" not in camera_info:
            print(f"Warning: Resolution {self.v4l_settings.width}x{self.v4l_settings.height} was not applied. The camera might not support this resolution.")
        
        print("Camera settings adjusted.")

    def _apply_camera_settings(self):
        # Apply only the modifiable controls
        print("Applying modifiable controls to the camera...")
        modifiable_controls = {
            "brightness": self.camera_settings.brightness,
            "contrast": self.camera_settings.contrast,
            "saturation": self.camera_settings.saturation,
            "hue": self.camera_settings.hue,
            "white_balance_automatic": int(self.camera_settings.white_balance_automatic),
            "gamma": self.camera_settings.gamma,
            "gain": self.camera_settings.gain,
            "power_line_frequency": self.camera_settings.power_line_frequency,
            "sharpness": self.camera_settings.sharpness,
            "backlight_compensation": self.camera_settings.backlight_compensation,
            "auto_exposure": self.camera_settings.auto_exposure,
            "exposure_dynamic_framerate": int(self.camera_settings.exposure_dynamic_framerate),
        }
        
        for control, value in modifiable_controls.items():
            command = f"v4l2-ctl -d {self.video_device} --set-ctrl {control}={value}"
            print(f"Running command: {command}")
            os.system(command)
    
    def start_detection(self):
        # Set up software-based decoding with OpenCV
        print(f"Starting video capture on {self.video_device} with resolution {self.v4l_settings.width}x{self.v4l_settings.height} and pixel format {self.v4l_settings.pixel_format}...")
        self.capture = cv2.VideoCapture(self.video_device)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.v4l_settings.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.v4l_settings.height)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.v4l_settings.pixel_format))

        # Verify resolution match
        actual_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if actual_width != self.v4l_settings.width or actual_height != self.v4l_settings.height:
            print(f"Warning: Requested resolution {self.v4l_settings.width}x{self.v4l_settings.height} could not be set. Using {actual_width}x{actual_height} instead.")
        
        if not self.capture.isOpened():
            raise Exception(f"Cannot open video device {self.video_device}")
        
        print("Video capture started. Press 'q' to quit.")
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to read from video device.")
                break
            
            # Resize the display window to match the resolution
            frame = cv2.resize(frame, (self.v4l_settings.width, self.v4l_settings.height))
            cv2.imshow('Live Feed', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping video capture.")
                break
        
        self.capture.release()
        cv2.destroyAllWindows()
        print("Video capture stopped.")
