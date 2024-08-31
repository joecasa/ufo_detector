import gi
import subprocess
import sys
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from dataclasses import dataclass

@dataclass
class CameraConfig:
    video_device: str = "/dev/video0"
    width: int = 640
    height: int = 480
    fps: int = 30
    pixel_format: str = "YUY2"
    brightness: int = 10
    contrast: int = 20
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
    multicast_group: str = "239.255.12.42"
    multicast_port: int = 5004

class ufodCam:
    def __init__(self, config: CameraConfig):
        self.config = config
        Gst.init(None)
        self.pipeline = None
        self.loop = GLib.MainLoop()
        self.setup_pipeline()

    def setup_pipeline(self, mode='display'):
        sink = self.determine_sink(mode)
        pipeline_str = (
            f"v4l2src device={self.config.video_device} ! "
            f"video/x-raw, format={self.config.pixel_format}, width={self.config.width}, height={self.config.height}, "
            f"framerate={self.config.fps}/1, brightness={self.config.brightness}, contrast={self.config.contrast}, "
            f"saturation={self.config.saturation}, hue={self.config.hue}, gamma={self.config.gamma}, "
            f"gain={self.config.gain}, power-line-frequency={self.config.power_line_frequency}, "
            f"sharpness={self.config.sharpness}, backlight-compensation={self.config.backlight_compensation}, "
            f"white-balance-temperature-auto={self.config.white_balance_automatic}, exposure-auto={self.config.auto_exposure}, "
            f"exposure-dynamic-framerate={int(self.config.exposure_dynamic_framerate)} ! "
            f"videoconvert ! videoscale ! {sink}"
        )
        self.pipeline = Gst.parse_launch(pipeline_str)
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def determine_sink(self, mode):
        if mode == 'appsink':
            return "appsink emit-signals=True"
        elif mode == 'display':
            return "autovideosink"
        elif mode == 'stream':
            return f"udpsink host={self.config.multicast_group} port={self.config.multicast_port} auto-multicast=true"
        return "autovideosink"  # default fallback

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()
            print("End of stream")
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, {debug}")
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()

    def start_video_stream(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        try:
            self.loop.run()
        except:
            pass
        print("GStreamer pipeline activated with camera settings.")

    def display_camera_settings(self):
        result = subprocess.run(['v4l2-ctl', '--list-ctrls', '--device', self.config.video_device], capture_output=True, text=True)
        if result.stdout:
            print("Current camera settings:")
            print(result.stdout)
        else:
            print("Failed to retrieve camera settings or no settings available.")
