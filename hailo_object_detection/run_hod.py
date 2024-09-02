import argparse
from ufodCam import ufodCam, CameraConfig

def main():
    parser = argparse.ArgumentParser(description="Configure and start a video stream with adjustable settings via ufodCam.")
    parser.add_argument("--video_device", type=str, default="/dev/video0", help="Video device path")
    parser.add_argument("--width", type=int, default=640, help="Width of the video")
    parser.add_argument("--height", type=int, default=480, help="Height of the video")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate in frames per second")
    parser.add_argument("--pixel_format", type=str, default="YUY2", help="Pixel format")
    parser.add_argument("--brightness", type=int, default=10, help="Brightness setting")
    parser.add_argument("--contrast", type=int, default=20, help="Contrast setting")
    parser.add_argument("--saturation", type=int, default=70, help="Saturation setting")
    parser.add_argument("--hue", type=int, default=0, help="Hue setting")
    parser.add_argument("--white_balance_automatic", action='store_true', help="Enable automatic white balance")
    parser.add_argument("--gamma", type=int, default=150, help="Gamma setting")
    parser.add_argument("--gain", type=int, default=5, help="Gain setting")
    parser.add_argument("--power_line_frequency", type=int, default=2, help="Power line frequency")
    parser.add_argument("--sharpness", type=int, default=4, help="Sharpness setting")
    parser.add_argument("--backlight_compensation", type=int, default=1, help="Backlight compensation")
    parser.add_argument("--auto_exposure", type=int, default=3, help="Auto exposure mode")
    parser.add_argument("--exposure_dynamic_framerate", action='store_true', help="Enable dynamic framerate for exposure")
    parser.add_argument("--stream_mode", choices=['multicast', 'unicast', 'display', 'appsink'], default='display', help="Select streaming mode: multicast, unicast, display, or appsink")
    parser.add_argument("--multicast_group", default="239.255.12.42", help="Multicast group IP address for multicast mode")
    parser.add_argument("--multicast_port", type=int, default=5004, help="Multicast port")
    parser.add_argument("--unicast_address", default="192.168.1.100", help="Unicast IP address for point-to-point streaming")
    parser.add_argument("--unicast_port", type=int, default=5004, help="Unicast port for point-to-point streaming")
    parser.add_argument("--debug", action='store_true', help="Enable debugging output")

    args = parser.parse_args()

    config = CameraConfig(
        video_device=args.video_device,
        width=args.width,
        height=args.height,
        fps=args.fps,
        pixel_format=args.pixel_format,
        brightness=args.brightness,
        contrast=args.contrast,
        saturation=args.saturation,
        hue=args.hue,
        white_balance_automatic=args.white_balance_automatic,
        gamma=args.gamma,
        gain=args.gain,
        power_line_frequency=args.power_line_frequency,
        sharpness=args.sharpness,
        backlight_compensation=args.backlight_compensation,
        auto_exposure=args.auto_exposure,
        exposure_dynamic_framerate=args.exposure_dynamic_framerate,
        stream_mode=args.stream_mode,
        multicast_group=args.multicast_group,
        multicast_port=args.multicast_port,
        unicast_address=args.unicast_address,
        unicast_port=args.unicast_port,
        debug=args.debug
    )

    camera = ufodCam(config)
    camera.start_video_stream()

if __name__ == "__main__":
    main()
