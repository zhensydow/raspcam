#!/usr/bin/env python
""" Raspberry Camera Web Server main file.
"""
#------------------------------------------------------------------------------
import web
import config
import json
import multiprocessing
import time

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

        if 'hflip' in params and params.hflip:
            cam_config['hflip'] = not cam_config.get('hflip', False)

        if 'vflip' in params and params.vflip:
            cam_config['vflip'] = not cam_config.get('vflip', False)

        return json.dumps({'ok': True})


#------------------------------------------------------------------------------
def camera_loop(camera_config):
    """Camera update loop."""

    print "start loop"
    try:
        while 1 == 1:
            time.sleep(5)
            print "camera ", camera_config

    except KeyboardInterrupt:
        print "Ending loop"


#------------------------------------------------------------------------------
def main():
    """Main function."""

    manager = multiprocessing.Manager()

    camera_config = manager.dict()
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
