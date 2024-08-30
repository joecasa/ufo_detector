from hailo_object_detector import CameraSettings, V4LSettings, HailoObjectDetector
import sys

def main():
    # Check if enough command-line arguments are provided
    if len(sys.argv) < 5:
        print("Usage: python3 test_hailo_detector.py /dev/videoX width height pixel_format model_path")
        sys.exit(1)
    
    video_device = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    pixel_format = sys.argv[4]
    model_path = sys.argv[5]
    
    # Declare the camera and V4L settings
    camera_settings = CameraSettings(
        brightness=10,
        contrast=40,
        saturation=70,
        hue=0,
        white_balance_automatic=True,
        gamma=150,
        gain=5,
        power_line_frequency=2,  # Set to 2 for 60Hz (North American NTSC)
        sharpness=4,
        backlight_compensation=1,
        auto_exposure=3,  # Aperture Priority Mode
        exposure_dynamic_framerate=False
    )
    
    v4l_settings = V4LSettings(
        device_path=video_device,
        camera_settings=camera_settings,
        width=width,
        height=height,
        pixel_format=pixel_format
    )
    
    detector = HailoObjectDetector(
        video_device=video_device, 
        camera_settings=camera_settings, 
        v4l_settings=v4l_settings, 
        model_path=model_path
    )
    
    # Apply camera settings and start object detection
    detector._apply_camera_settings()
    detector.start_detection()

if __name__ == "__main__":
    main()
