#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Geoholmes: Geocaching mysteries
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
Run the web frontend
'''

import os
from flask import Flask
from geoshaker.frontend import views


# App creation
app = Flask(__name__)
app.debug = True
app.config.from_pyfile(os.path.join(os.getcwd(), 'config.py'))
app.register_blueprint(views.frontend, url_prefix=app.config['FRONTEND_PREFIX'])

def main():
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])

if __name__ == '__main__':
    main()
