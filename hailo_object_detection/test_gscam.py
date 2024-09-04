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

    # Modify some GStreamer config (optional)
    # gstreamer_config['brightness']['current_value'] = 0.5

    # Configure and run GStreamer pipeline
    camera.configure_gstreamer(gstreamer_config)

    camera.close()
