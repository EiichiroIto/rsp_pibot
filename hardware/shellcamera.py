#!/usr/bin/env python
# author: Eiichiro Ito
# e-mail: e-itoh@ygu.ac.jp
# created: 2018/5/29
# License: MIT License
#
# Still Camera Support using Shell scripts
import commands

shell_scripts = './takephoto.sh'
image_basename = 'camera.'
_camera = None

class Camera(object):
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.camera_format = "jpg" # Parameter "jpg" or "gif" or "png"
        self.vehicle.add_variable('camera_format', self.set_camera_format)
        self.vehicle.add_handler('shoot', self.shoot)

    def set_camera_format(self, val):
        if val == 'jpg' or val == 'gif' or val == 'png':
            self.camera_format = val

    def shoot(self):
        print("shoot")
        filename = image_basename + self.camera_format
        (status,output) = commands.getstatusoutput(shell_scripts + ' ' + camera_format + ' ' + filename)
        print(output)
        if status > 0:
            print("Error: %s" % output)
            return
        f = None
        try:
            f = open(filename, "rb")
            data = f.read()
        except:
            print("Error in reading output: %s" % filename)
        finally:
            if f is not None:
                f.close()
                self.vehicle.server.send_image(data)

def setup(vehicle):
    _camera = Camera(vehicle)
