import cv2
import os
import subprocess
import hailo
import numpy as np

from dataclasses import dataclass

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
    pixel_format: str = "YUYV"
    width: int = 640
    height: int = 480

class HailoObjectDetector:
    def __init__(self, video_device: str, camera_settings: CameraSettings, v4l_settings: V4LSettings, model_path: str):
        self.video_device = video_device
        self.camera_settings = camera_settings
        self.v4l_settings = v4l_settings
        self.model_path = model_path
        self.capture = None
        print(f"Initializing HailoObjectDetector for video device: {self.video_device} with resolution {self.v4l_settings.width}x{self.v4l_settings.height} and pixel format {self.v4l_settings.pixel_format}")
        self._adjust_camera_settings_for_opencv()
        self._setup_hailo()

    def _adjust_camera_settings_for_opencv(self):
        print("Adjusting camera settings for OpenCV compatibility...")
        command = f"v4l2-ctl -d {self.video_device} --set-fmt-video=width={self.v4l_settings.width},height={self.v4l_settings.height},pixelformat={self.v4l_settings.pixel_format}"
        print(f"Setting format: {command}")
        os.system(command)

    def _setup_hailo(self):
        print(f"Loading model from {self.model_path}...")
        self.hef = hailo.Hef(self.model_path)  # Adjusted for the Hailo Runtime
        self.network_group = self.hef.configure(self.hef.create_config_params())[0]
        self.input_tensor_shape = self.network_group.get_input_vstream_shape(0)
        self.output_tensor_shape = self.network_group.get_output_vstream_shape(0)
        print(f"Model loaded. Input tensor shape: {self.input_tensor_shape}, Output tensor shape: {self.output_tensor_shape}")

    def _run_inference(self, frame):
        input_data = cv2.resize(frame, (self.input_tensor_shape[2], self.input_tensor_shape[1]))
        input_data = input_data.astype(np.float32)
        input_data = np.expand_dims(input_data, axis=0)  # Add batch dimension
        self.network_group.write_vstream("input_0", input_data)
        output_data = self.network_group.read_vstream("output_0")
        return output_data

    def start_detection(self):
        print(f"Starting video capture on {self.video_device} with resolution {self.v4l_settings.width}x{self.v4l_settings.height} and pixel format {self.v4l_settings.pixel_format}...")
        self.capture = cv2.VideoCapture(self.video_device)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.v4l_settings.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.v4l_settings.height)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.v4l_settings.pixel_format))

        if not self.capture.isOpened():
            raise Exception(f"Cannot open video device {self.video_device}")

        print("Video capture started. Press 'q' to quit.")
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to read from video device.")
                break
            
            output_data = self._run_inference(frame)
            # Process the output_data to extract bounding boxes, labels, etc.
            cv2.imshow('Live Feed', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping video capture.")
                break
        
        self.capture.release()
        cv2.destroyAllWindows()
        print("Video capture stopped.")
