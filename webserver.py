#!/usr/bin/env python
""" Raspberry Camera Web Server main file.
"""
#------------------------------------------------------------------------------
import web
import config
import json
import multiprocessing
import time
import shutil
import os.path
import cv2

try:
    import picamera
    found_picamera = True
except ImportError:
    found_picamera = False

#------------------------------------------------------------------------------
DEF_BRIGHTNESS = 50
DEF_CONTRAST = 0

#------------------------------------------------------------------------------
URLS = (
    '/', 'Main',
    '/lastimage.jpg', 'LastImage',
    '/filterimage.jpg', 'FilterImage',
    '/ajax/camera', 'AjaxCamera',
    '/ajax/filter', 'AjaxFilter',
)

WEB_ENV = {'version': config.VERSION, 'camera_name': config.CAMERA_NAME}
TMPLS = web.template.render('templates', globals=WEB_ENV)

web.config.debug = config.WEB_DEBUG

camera_sleep = config.CAMERA_SLEEP

face_cascade = cv2.CascadeClassifier('hc_ff.xml')
eye_cascade = cv2.CascadeClassifier('hc_eye.xml')

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
class FilterImage(object):
    """Class to handle image queries."""

    def GET(self):
        """http GET response method."""

        web.header("Content-Type", "images/jpeg")
        return open("filterimage.jpg", "rb").read()


#------------------------------------------------------------------------------
class AjaxCamera(object):
    """Class to handle camera ajax queries."""

    def GET(self):
        """http GET response method."""

        web.header('Content-Type', 'application/json')
        cam_config = web.camera_config
        params = {}
        params.update(cam_config)
        return json.dumps({'ok': True, 'params': params})

    def PUT(self):
        """http PUT response method."""

        web.header('Content-Type', 'application/json')
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
class AjaxFilter(object):
    """Class to handle camera ajax filter queries."""
    
    def POST(self):
        """http POST response method."""
        web.header('Content-Type', 'application/json')
        params = web.input()
        print params

        if 'filter_function' in params:
            if params['filter_function'] == 'edges':
                img = cv2.imread('lastimage.jpg')
                edges = cv2.Canny(img, 100, 100 )
                cv2.imwrite('filterimage.jpg', edges)

            elif params['filter_function'] == 'laplacian':
                img = cv2.imread('lastimage.jpg')
                laplacian = cv2.Laplacian(img, cv2.CV_64F)
                cv2.imwrite('filterimage.jpg', laplacian)

            elif params['filter_function'] == 'faces':
                img = cv2.imread('lastimage.jpg')
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                cv2.imwrite('filterimage.jpg', img)

        return json.dumps({'ok': True})


#------------------------------------------------------------------------------
def camera_loop(camera_config):
    """Camera update loop."""

    camera = None
    if found_picamera:
        camera = picamera.PiCamera()

    while 1 == 1:
        if camera:
            camera.brightness = camera_config.get('brightness', DEF_BRIGHTNESS)
            camera.contrast = camera_config.get('contrast', DEF_CONTRAST)
            camera.hflip = camera_config.get('hflip', False)
            camera.vflip = camera_config.get('vflip', False)
            camera.capture('lastimage0.jpg')
            shutil.copy('lastimage0.jpg', 'lastimage.jpg')
        else:
            print "camera: ", camera_config

        time.sleep(camera_sleep)


#------------------------------------------------------------------------------
def main():
    """Main function."""

    if found_picamera:
        print "picamera founded"
    else:
        print "picamera not founded"

    if not os.path.isfile("lastimage.jpg"):
        shutil.copy("empty.jpg", "lastimage.jpg");

    if not os.path.isfile("filterimage.jpg"):
        shutil.copy("empty.jpg", "filterimage.jpg");

    manager = multiprocessing.Manager()

    camera_config = manager.dict()
    camera_config['brightness'] = DEF_BRIGHTNESS
    camera_config['contrast'] = DEF_CONTRAST
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
