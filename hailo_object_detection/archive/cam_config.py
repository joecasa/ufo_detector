# cam_config.py
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from camera_config import CameraConfig

class CamConfig:
    def __init__(self, config: CameraConfig):
        Gst.init(None)
        self.config = config
        self.pipeline = self.create_pipeline()

    def create_pipeline(self):
        white_balance = "auto" if self.config.white_balance_automatic else "manual"
        return Gst.parse_launch(
            f"v4l2src device={self.config.video_device} ! "
            f"video/x-raw, format={self.config.pixel_format}, width={self.config.width}, height={self.config.height}, "
            f"framerate={self.config.fps}/1, brightness={self.config.brightness}, contrast={self.config.contrast}, "
            f"saturation={self.config.saturation}, hue={self.config.hue}, gamma={self.config.gamma}, "
            f"gain={self.config.gain}, power-line-frequency={self.config.power_line_frequency}, "
            f"sharpness={self.config.sharpness}, backlight-compensation={self.config.backlight_compensation}, "
            f"white-balance-temperature-{white_balance}, exposure-auto={self.config.auto_exposure}, "
            f"exposure-dynamic-framerate={int(self.config.exposure_dynamic_framerate)} ! "
            "videoconvert ! videoscale ! "
            "appsink emit-signals=True"
        )

    def start_video_stream(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        print("GStreamer pipeline started with comprehensive camera settings.")
