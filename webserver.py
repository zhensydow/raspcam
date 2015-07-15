#!/usr/bin/env python
""" Raspberry Camera Web Server main file.
"""
#------------------------------------------------------------------------------
import web
import config

#------------------------------------------------------------------------------
URLS = (
    '/', 'Main',
    '/lastimage.jpg', 'LastImage',
)

WEB_ENV = {'version': config.VERSION, 'camera_name': config.CAMERA_NAME}
TMPLS = web.template.render('templates', globals=WEB_ENV)

web.config.debug = config.WEB_DEBUG


#------------------------------------------------------------------------------
class Main(object):
    """Class to Handle root urls."""
    def GET(self):
        return TMPLS.main()


#------------------------------------------------------------------------------
class LastImage(object):
    def GET(self):
        web.header("Content-Type", "images/jpeg")
        return open("lastimage.jpg","rb").read()


#------------------------------------------------------------------------------
def main():
    """ Main function."""
    app = web.application(URLS, globals())
    app.run()


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------
