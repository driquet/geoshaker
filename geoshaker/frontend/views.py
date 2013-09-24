# -*- coding: utf-8 -*-

'''
File: views.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Flask views
'''

import forms, os
from flask import Blueprint, render_template, request, send_from_directory

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/', methods=['GET', 'POST'])
def home():
    form = forms.ShakerForm(request.form)
    if request.method == 'POST' and form.validate():
        shake = {
            'mystery'   : form.mystery.data,
            'cache'     : form.cache.data,
            'max_distance'  : form.max_distance.data,
            'variables' :
                [(v.form.symbol.data, int(v.form.min_val.data), int(v.form.max_val.data)) for v in form.variables]
        }
        print shake
    return render_template('home.html', form=form)

@frontend.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join(frontend.root_path, 'templates', 'static')
    return send_from_directory(static_path, filename)
