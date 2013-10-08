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
from flask import Flask, request
from flask.ext.babel import Babel
from geoshaker.frontend import views


# App creation
app = Flask(__name__)
app.debug = True
app.config.from_pyfile(os.path.join(os.getcwd(), 'config.py'))
app.register_blueprint(views.frontend, url_prefix=app.config['FRONTEND_PREFIX'])

# Language/Babel
babel = Babel(app)


@app.context_processor
def utility_processor():
    def format_variables(variables, combination):
        var_symbols = [elt[0] for elt in variables]
        return ', '.join(['%s = %d' % elt for elt in zip(var_symbols, combination)])
    return dict(format_variables=format_variables)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


def main():
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])

if __name__ == '__main__':
    main()
