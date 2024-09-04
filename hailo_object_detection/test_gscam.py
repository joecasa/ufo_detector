import json
from gscam import GStreamerCamera

if __name__ == "__main__":
    camera = GStreamerCamera()

    # Get all controls from the camera
    controls = camera.get_all_controls()

    # Display the full control data structure for camera controls
    print("Complete Camera Control Structure:")
    print(json.dumps(controls, indent=4))

    # Save camera controls to JSON file
    with open('camera_controls.json', 'w') as f:
        json.dump(controls, f, indent=4)

    # Get GStreamer pipeline options and save to JSON file
    gstreamer_options = camera.get_gstreamer_pipeline_config()
    print("Complete GStreamer Options Structure:")
    print(json.dumps(gstreamer_options, indent=4))

    with open('gstreamer_options.json', 'w') as f:
        json.dump(gstreamer_options, f, indent=4)

    # Load the JSON config for GStreamer and configure the pipeline
    with open('gstreamer_options.json', 'r') as f:
        gstreamer_config = json.load(f)

    # Enable local display by setting the 'display' option to True
    gstreamer_config['display']['enabled'] = False

    # Disable streaming or appsink for local display
    gstreamer_config['stream']['enabled'] = True
    gstreamer_config['stream']['ip'] = "192.168.1.56"  # IP address of the receiving machine
    gstreamer_config['stream']['port'] = 5000  # Port for streaming
    
    # Example for local display
    # gstreamer_config['display']['enabled'] = True

    # Example for appsink
    # gstreamer_config['appsink']['enabled'] = False

    # Configure and run GStreamer pipeline based on the updated configuration
    camera.configure_gstreamer(gstreamer_config)

    camera.close()
