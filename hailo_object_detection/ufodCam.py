import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
from dataclasses import dataclass

@dataclass
class CameraConfig:
    video_device: str = "/dev/video0"
    width: int = 640
    height: int = 480
    fps: int = 30
    pixel_format: str = "YUY2"  # Default pixel format
    video_format: str = "MJPG"  # Default video format for RTP streaming
    brightness: int = 10
    contrast: int = 20
    saturation: int = 70
    hue: int = 0
    white_balance_automatic: bool = True
    gamma: int = 150
    gain: int = 5
    power_line_frequency: int = 2
    sharpness: int = 4
    backlight_compensation: int = 1
    auto_exposure: int = 3
    exposure_dynamic_framerate: bool = False
    stream_mode: str = 'display'
    multicast_group: str = "239.255.12.42"
    multicast_port: int = 5004
    unicast_address: str = "192.168.1.100"
    unicast_port: int = 5004
    rtp_port: int = 5004
    debug: bool = False
    debug_level: str = "WARNING"  # Default debug level

class ufodCam:
    def __init__(self, config: CameraConfig):
        self.config = config
        Gst.init(None)
        if self.config.debug:
            Gst.debug_set_active(True)
            Gst.debug_set_default_threshold(Gst.DebugLevel.from_string(self.config.debug_level))
        self.pipeline = None
        self.setup_pipeline()

    def setup_pipeline(self):
        self.determine_capabilities()  # Determine if conversion is necessary based on the camera's capabilities
        sink = self.determine_sink()
        encoder, payloader = self.get_rtp_elements()

        if self.needs_conversion:
            print(f"Converting from {self.config.pixel_format} to {self.config.video_format} for RTP streaming.")
            pipeline_str = (
                f"v4l2src device={self.config.video_device} ! "
                f"video/x-raw, format={self.config.pixel_format}, width={self.config.width}, height={self.config.height}, "
                f"framerate={self.config.fps}/1 ! "
                f"videoconvert ! "
                f"{encoder} ! {payloader} ! "
                f"{sink}"
            )
        else:
            print(f"Using {self.config.video_format} directly from the camera.")
            if self.config.video_format == "MJPG":
                pipeline_str = (
                    f"v4l2src device={self.config.video_device} ! "
                    f"image/jpeg, width={self.config.width}, height={self.config.height}, "
                    f"framerate={self.config.fps}/1 ! "
                    f"{encoder} ! {payloader} ! "
                    f"{sink}"
                )
            else:
                pipeline_str = (
                    f"v4l2src device={self.config.video_device} ! "
                    f"video/x-raw, format={self.config.video_format}, width={self.config.width}, height={self.config.height}, "
                    f"framerate={self.config.fps}/1 ! "
                    f"{encoder} ! {payloader} ! "
                    f"{sink}"
                )

        self.pipeline = Gst.parse_launch(pipeline_str)
        self.start_video_stream()

    def determine_capabilities(self):
        # Check the camera capabilities
        self.needs_conversion = True  # Assume conversion is necessary
        device_caps = Gst.DeviceMonitor()
        device_caps.start()
        devices = device_caps.get_devices()
        for device in devices:
            if device.get_device_class() == "Video/Source":
                caps = device.get_caps()
                for i in range(caps.get_size()):
                    structure = caps.get_structure(i)
                    if structure.get_name() == 'video/x-raw' and structure.has_field('format'):
                        if structure.get_string('format') == self.config.video_format:
                            self.needs_conversion = False
                            break
        device_caps.stop()

    def get_rtp_elements(self):
        if self.config.video_format == "MJPG":
            return ("jpegenc", "rtpjpegpay")
        elif self.config.video_format == "YUY2":
            return ("vp8enc error-resilient=partitions keyframe-max-dist=30 auto-alt-ref=true cpu-used=-5 deadline=1", "rtpvp8pay")
        return ("", "")  # Fallback or default encoder and payloader

    def determine_sink(self):
        if self.config.stream_mode == 'display':
            return "autovideosink"
        elif self.config.stream_mode == 'appsink':
            return "appsink emit-signals=True sync=false"
        elif self.config.stream_mode == 'multicast':
            return f"udpsink host={self.config.multicast_group} port={self.config.multicast_port} auto-multicast=true"
        elif self.config.stream_mode == 'unicast':
            return f"udpsink host={self.config.unicast_address} port={self.config.unicast_port} auto-multicast=false"
        elif self.config.stream_mode == 'rtp':
            return f"udpsink host={self.config.unicast_address} port={self.config.rtp_port} auto-multicast=false"
        return "fakesink"  # default fallback

    def start_video_stream(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        GLib.MainLoop().run()

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            print("End of stream")
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, {debug}")
            self.pipeline.set_state(Gst.State.NULL)
