import os
import v4l2
import fcntl


class UVCCamera:
    def __init__(self, device='/dev/video0'):
        self.device = device
        self.fd = os.open(self.device, os.O_RDWR)
    
    def get_control_value(self, control_id):
        ctrl = v4l2.v4l2_control()
        ctrl.id = control_id
        fcntl.ioctl(self.fd, v4l2.VIDIOC_G_CTRL, ctrl)
        return ctrl.value
    
    def set_control_value(self, control_id, value):
        ctrl = v4l2.v4l2_control()
        ctrl.id = control_id
        ctrl.value = value
        fcntl.ioctl(self.fd, v4l2.VIDIOC_S_CTRL, ctrl)
    
    def get_all_controls(self):
        queryctrl = v4l2.v4l2_queryctrl()
        controls = {}

        control_id = v4l2.V4L2_CID_BASE
        while control_id < v4l2.V4L2_CID_LASTP1:
            queryctrl.id = control_id
            try:
                fcntl.ioctl(self.fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
                if not (queryctrl.flags & v4l2.V4L2_CTRL_FLAG_DISABLED):
                    control_info = {
                        'id': queryctrl.id,
                        'name': queryctrl.name.decode(),
                        'minimum': queryctrl.minimum,
                        'maximum': queryctrl.maximum,
                        'step': queryctrl.step,
                        'default_value': queryctrl.default_value,
                        'current_value': self.get_control_value(queryctrl.id),
                    }
                    controls[queryctrl.name.decode()] = control_info
            except IOError:
                pass
            
            control_id += 1

        control_id = v4l2.V4L2_CID_PRIVATE_BASE
        while True:
            queryctrl.id = control_id
            try:
                fcntl.ioctl(self.fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
                if not (queryctrl.flags & v4l2.V4L2_CTRL_FLAG_DISABLED):
                    control_info = {
                        'id': queryctrl.id,
                        'name': queryctrl.name.decode(),
                        'minimum': queryctrl.minimum,
                        'maximum': queryctrl.maximum,
                        'step': queryctrl.step,
                        'default_value': queryctrl.default_value,
                        'current_value': self.get_control_value(queryctrl.id),
                    }
                    controls[queryctrl.name.decode()] = control_info
            except IOError:
                break
            
            control_id += 1
        
        return controls
    
    def configure_camera(self, config):
        for control_name, settings in config.items():
            try:
                self.set_control_value(settings['id'], settings['current_value'])
            except Exception as e:
                print(f"Error setting {control_name}: {e}")
    
    def close(self):
        os.close(self.fd)
