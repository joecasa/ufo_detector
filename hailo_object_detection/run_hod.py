import argparse
from ufodCam import ufodCam, CameraConfig

def main():
    parser = argparse.ArgumentParser(description="Configure and stream a video feed to VLC via ufodCam.")
    parser.add_argument("--video_device", type=str, default="/dev/video0", help="Video device path")
    parser.add_argument("--width", type=int, default=640, help="Width of the video")
    parser.add_argument("--height", type=int, default=480, help="Height of the video")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate in frames per second")
    parser.add_argument("--pixel_format", type=str, default="YUY2", help="Pixel format")
    parser.add_argument("--brightness", type=int, default=10, help="Brightness setting")
    parser.add_argument("--contrast", type=int, default=20, help="Contrast setting")
    parser.add_argument("--saturation", type=int, default=70, help="Saturation setting")
    parser.add_argument("--hue", type=int, default=0, help="Hue setting")
    parser.add_argument("--white_balance_automatic", action='store_true', help="Automatic white balance")
    parser.add_argument("--gamma", type=int, default=150, help="Gamma setting")
    parser.add_argument("--gain", type=int, default=5, help="Gain setting")
    parser.add_argument("--power_line_frequency", type=int, default=2, help="Power line frequency")
    parser.add_argument("--sharpness", type=int, default=4, help="Sharpness setting")
    parser.add_argument("--backlight_compensation", type=int, default=1, help="Backlight compensation")
    parser.add_argument("--auto_exposure", type=int, default=3, help="Auto exposure mode")
    parser.add_argument("--exposure_dynamic_framerate", action='store_true', help="Dynamic framerate for exposure")
    parser.add_argument("--mode", type=str, default='stream', help="Operation mode of the camera (appsink, display, stream)")
    parser.add_argument("--multicast_group", type=str, default="239.255.12.42", help="Multicast IP address for streaming")
    parser.add_argument("--multicast_port", type=int, default=5004, help="Multicast port for streaming")

    args = parser.parse_args()

    # Initialize the CameraConfig with parsed arguments
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
        multicast_group=args.multicast_group,
        multicast_port=args.multicast_port
    )

    # Instantiate the camera using ufodCam
    camera = ufodCam(config)
    camera.setup_pipeline(mode=args.mode)
    camera.start_video_stream()

if __name__ == "__main__":
    main()
