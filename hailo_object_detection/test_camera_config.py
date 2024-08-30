import sys
from cam_config import CamConfig, CameraSettings
from dataclasses import dataclass

@dataclass
class V4LSettings:
    device_path: str
    camera_settings: CameraSettings
    pixel_format: str = "YUYV"
    width: int = 640
    height: int = 480

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 test_camera_config.py /dev/videoX width height pixel_format")
        sys.exit(1)

    video_device = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    pixel_format = sys.argv[4]

    camera_settings = CameraSettings(
        brightness=10,
        contrast=40,
        saturation=70,
        hue=0,
        white_balance_automatic=True,
        gamma=150,
        gain=5,
        power_line_frequency=2,
        sharpness=4,
        backlight_compensation=1,
        auto_exposure=3,
        exposure_dynamic_framerate=False
    )

    v4l_settings = V4LSettings(
        device_path=video_device,
        camera_settings=camera_settings,
        width=width,
        height=height,
        pixel_format=pixel_format
    )

    cam_config = CamConfig(video_device, camera_settings, v4l_settings)
    cam_config.apply_camera_settings()

    cam_config.start_video_stream()

if __name__ == "__main__":
    main()
