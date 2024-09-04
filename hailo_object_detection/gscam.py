import subprocess
import json
from uvccamconfig import UVCCamera


class GStreamerCamera(UVCCamera):
    def __init__(self, device='/dev/video0'):
        super().__init__(device)
        self.gstreamer_options = self.get_gstreamer_options()
    
    def get_gstreamer_options(self):
        gstreamer_options = {
            'display': {
                'description': 'Local display using autovideosink',
                'enabled': False
            },
            'appsink': {
                'description': 'Output video frames to an application using appsink',
                'enabled': False
            },
            'stream': {
                'description': 'Stream video over network using udpsink',
                'enabled': False,
                'ip': '127.0.0.1',  # Default IP for streaming
                'port': 5000  # Default port for streaming
            }
        }
        return gstreamer_options
    
    def configure_gstreamer(self, config):
        pipeline_elements = ['v4l2src', f'device={self.device}', '!']

        # Add a video converter in the pipeline
        pipeline_elements.append('videoconvert')

        if config.get('display', {}).get('enabled'):
            # If display mode is enabled, use autovideosink
            pipeline_elements.extend(['!', 'autovideosink'])

        elif config.get('appsink', {}).get('enabled'):
            # If appsink mode is enabled, use appsink
            pipeline_elements.extend(['!', 'appsink'])

        elif config.get('stream', {}).get('enabled'):
            # If streaming mode is enabled, set up udpsink with IP and port
            stream_ip = config['stream'].get('ip', '127.0.0.1')
            stream_port = config['stream'].get('port', 5000)
            pipeline_elements.extend([
                '!', 'x264enc', 'tune=zerolatency',
                '!', 'rtph264pay', 
                '!', f'udpsink host={stream_ip} port={stream_port}'
            ])

        # Combine the elements into a properly formatted GStreamer pipeline
        pipeline_command = 'gst-launch-1.0 ' + ' '.join(pipeline_elements)

        print(f"Running GStreamer Pipeline: {pipeline_command}")

        # Run GStreamer pipeline
        try:
            subprocess.run(pipeline_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running pipeline: {e}")
    
    def get_gstreamer_pipeline_config(self):
        return self.gstreamer_options
import subprocess
import json
from uvccamconfig import UVCCamera


class GStreamerCamera(UVCCamera):
    def __init__(self, device='/dev/video0'):
        super().__init__(device)
        self.gstreamer_options = self.get_gstreamer_options()
    
    def get_gstreamer_options(self):
        gstreamer_options = {
            'display': {
                'description': 'Local display using autovideosink',
                'enabled': False
            },
            'appsink': {
                'description': 'Output video frames to an application using appsink',
                'enabled': False
            },
            'stream': {
                'description': 'Stream video over network using udpsink',
                'enabled': False,
                'ip': '127.0.0.1',  # Default IP for streaming
                'port': 5000  # Default port for streaming
            }
        }
        return gstreamer_options
    
    def configure_gstreamer(self, config):
        pipeline_elements = ['v4l2src', f'device={self.device}', '!']

        # Add a video converter in the pipeline
        pipeline_elements.append('videoconvert')

        if config.get('display', {}).get('enabled'):
            # If display mode is enabled, use autovideosink
            pipeline_elements.extend(['!', 'autovideosink'])

        elif config.get('appsink', {}).get('enabled'):
            # If appsink mode is enabled, use appsink
            pipeline_elements.extend(['!', 'appsink'])

        elif config.get('stream', {}).get('enabled'):
            # If streaming mode is enabled, set up udpsink with IP and port
            stream_ip = config['stream'].get('ip', '127.0.0.1')
            stream_port = config['stream'].get('port', 5000)
            pipeline_elements.extend([
                '!', 'x264enc', 'tune=zerolatency',
                '!', 'rtph264pay', 
                '!', f'udpsink host={stream_ip} port={stream_port}'
            ])

        # Combine the elements into a properly formatted GStreamer pipeline
        pipeline_command = 'gst-launch-1.0 ' + ' '.join(pipeline_elements)

        print(f"Running GStreamer Pipeline: {pipeline_command}")

        # Run GStreamer pipeline
        try:
            subprocess.run(pipeline_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running pipeline: {e}")
    
    def get_gstreamer_pipeline_config(self):
        return self.gstreamer_options
