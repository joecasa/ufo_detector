import subprocess
import json
from uvccamconfig import UVCCamera


class GStreamerCamera(UVCCamera):
    def __init__(self, device='/dev/video0'):
        super().__init__(device)
        self.gstreamer_options = self.get_gstreamer_options()
    
    def get_gstreamer_options(self):
        gstreamer_options = {}

        # Query gstreamer to find supported properties
        result = subprocess.run(
            ['gst-inspect-1.0', 'v4l2src'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if '  ' in line and ':' in line:
                    option, description = line.split(':', 1)
                    option = option.strip()
                    description = description.strip()
                    gstreamer_options[option] = {
                        'description': description,
                        'current_value': None,  # Placeholder for values
                    }
        
        return gstreamer_options
    
    def configure_gstreamer(self, config):
        pipeline_elements = ['v4l2src', f'device={self.device}']
        
        for option, settings in config.items():
            if 'current_value' in settings and settings['current_value'] is not None:
                pipeline_elements.append(f'{option}={settings["current_value"]}')
        
        pipeline_elements.extend(['!', 'videoconvert', '!', 'autovideosink'])
        pipeline_command = ['gst-launch-1.0'] + pipeline_elements

        # Run GStreamer pipeline
        subprocess.call(pipeline_command)
    
    def get_gstreamer_pipeline_config(self):
        return self.gstreamer_options
