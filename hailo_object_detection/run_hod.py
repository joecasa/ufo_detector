import argparse
from ufodCam import ufodCam, CameraConfig

def main():
    parser = argparse.ArgumentParser(description="Starts the camera streaming based on specified parameters.")
    parser.add_argument("--video_device", type=str, default="/dev/video0", help="The video device path.")
    parser.add_argument("--width", type=int, default=640, help="Video width.")
    parser.add_argument("--height", type=int, default=480, help="Video height.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--pixel_format", type=str, default="YUY2", choices=['YUY2', 'MJPG'], help="Pixel format for video.")
    parser.add_argument("--video_format", type=str, default="MJPG", choices=['YUY2', 'MJPG'], help="Video format for RTP streaming.")
    parser.add_argument("--brightness", type=int, default=10, help="Camera brightness setting.")
    parser.add_argument("--contrast", type=int, default=20, help="Camera contrast setting.")
    parser.add_argument("--saturation", type=int, default=70, help="Camera saturation setting.")
    parser.add_argument("--hue", type=int, default=0, help="Camera hue setting.")
    parser.add_argument("--white_balance_automatic", action='store_true', help="Enable automatic white balance.")
    parser.add_argument("--gamma", type=int, default=150, help="Camera gamma setting.")
    parser.add_argument("--gain", type=int, default=5, help="Camera gain setting.")
    parser.add_argument("--power_line_frequency", type=int, default=2, help="Camera power line frequency setting (e.g., 50 Hz, 60 Hz).")
    parser.add_argument("--sharpness", type=int, default=4, help="Camera sharpness setting.")
    parser.add_argument("--backlight_compensation", type=int, default=1, help="Camera backlight compensation setting.")
    parser.add_argument("--auto_exposure", type=int, default=3, help="Camera auto exposure setting.")
    parser.add_argument("--exposure_dynamic_framerate", action='store_true', help="Enable dynamic framerate based on exposure.")
    parser.add_argument("--stream_mode", type=str, choices=['display', 'appsink', 'multicast', 'unicast', 'rtp'], default="display", help="Stream mode.")
    parser.add_argument("--multicast_group", type=str, default="239.255.12.42", help="Multicast group address.")
    parser.add_argument("--multicast_port", type=int, default=5004, help="Multicast port.")
    parser.add_argument("--unicast_address", type=str, default="192.168.1.100", help="Unicast address.")
    parser.add_argument("--unicast_port", type=int, default=5004, help="Unicast port.")
    parser.add_argument("--rtp_port", type=int, default=5004, help="RTP stream port.")
    parser.add_argument("--debug", action='store_true', help="Enable debugging.")
    parser.add_argument("--debug_level", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default="WARNING", help="Debug level for GStreamer.")

    args = parser.parse_args()

    config = CameraConfig(
        video_device=args.video_device,
        width=args.width,
        height=args.height,
        fps=args.fps,
        pixel_format=args.pixel_format,
        video_format=args.video_format,
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
        rtp_port=args.rtp_port,
        debug=args.debug,
        debug_level=args.debug_level
    )

    camera = ufodCam(config)
    camera.start_video_stream()

if __name__ == "__main__":
    main()
