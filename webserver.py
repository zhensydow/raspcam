#!/usr/bin/env python
""" Raspberry Camera Web Server main file.
"""
#------------------------------------------------------------------------------
import web
import config
import json
import multiprocessing
import time

try:
    import picamera
    found_picamera = True
except ImportError:
    found_picamera = False

#------------------------------------------------------------------------------
URLS = (
    '/', 'Main',
    '/lastimage.jpg', 'LastImage',
    '/ajax/camera', 'AjaxCamera',
)

WEB_ENV = {'version': config.VERSION, 'camera_name': config.CAMERA_NAME}
TMPLS = web.template.render('templates', globals=WEB_ENV)

web.config.debug = config.WEB_DEBUG


#------------------------------------------------------------------------------
def getInt(string_value, default_value=0):
    try:
        int_value = int(string_value)
        return int_value
    except ValueError:
        return default_value


#------------------------------------------------------------------------------
class Main(object):
    """Class to Handle root urls."""

    def GET(self):
        """http GET response method."""

        return TMPLS.main()


#------------------------------------------------------------------------------
class LastImage(object):
    """Class to handle image queries."""

    def GET(self):
        """http GET response method."""

        web.header("Content-Type", "images/jpeg")
        return open("lastimage.jpg", "rb").read()


#------------------------------------------------------------------------------
class AjaxCamera(object):
    """Class to handle camera ajax queries."""

    def PUT(self):
        """http PUT response method."""

        params = web.input()
        cam_config = web.camera_config

        if 'brightness' in params:
            old_val = cam_config['brightness']
            cam_config['brightness'] = getInt(params['brightness'], old_val)

        if 'contrast' in params:
            old_val = cam_config['contrast']
            cam_config['contrast'] = getInt(params['contrast'], old_val)

        if 'hflip' in params and params.hflip:
            cam_config['hflip'] = not cam_config.get('hflip', False)

        if 'vflip' in params and params.vflip:
            cam_config['vflip'] = not cam_config.get('vflip', False)

        return json.dumps({'ok': True})


#------------------------------------------------------------------------------
def camera_loop(camera_config):
    """Camera update loop."""

    camera = None
    if found_picamera:
        camera = picamera.PiCamera()

    while 1 == 1:
        if camera:
            camera.capture('lastimage.jpg')
        else:
            print "camera: ", camera_config

        time.sleep(5)


#------------------------------------------------------------------------------
def main():
    """Main function."""

    if found_picamera:
        print "picamera founded"
    else:
        print "picamera not founded"

    manager = multiprocessing.Manager()

    camera_config = manager.dict()
    camera_config['brightness'] = 50
    camera_config['contrast'] = 0
    camera_config['hflip'] = False
    camera_config['vflip'] = False

    app = web.application(URLS, globals())

    web.camera_config = camera_config

    loop = multiprocessing.Process(target=camera_loop, args=(camera_config,))
    loop.start()
    app.run()
    loop.terminate()


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------
