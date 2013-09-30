# -*- coding: utf-8 -*-

'''
File: views.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Flask views
'''

import os, operator
from flask import Blueprint, render_template, request, send_from_directory
from geoshaker.frontend import forms
from geoshaker.core import shaker, coordinates

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

        # Splitting up coordinates
        m_split = forms.mystery_re.match(shake['mystery'])
        c_split = forms.cache_re.match(shake['cache'])

        mystery = (
            (
                1 if m_split.group(1) == 'N' else -1,
                int(m_split.group(2)),
                float(m_split.group(3))
            ), (
                1 if m_split.group(4) == 'E' else -1,
                int(m_split.group(5)),
                float(m_split.group(6)),
            )
        )

        cache = (
            (
                1 if c_split.group(1) == 'N' else -1,
                c_split.group(2),
                c_split.group(3).split('.')[0],
                c_split.group(3).split('.')[1],
            ), (
                1 if c_split.group(4) == 'E' else -1,
                c_split.group(5),
                c_split.group(6).split('.')[0],
                c_split.group(6).split('.')[1],
            )
        )
        variables = [shaker.UnknownValue(*elt) for elt in shake['variables']]

        # Compute combinations
        nb_combinations = reduce(operator.mul, [len(elt) for elt in variables])
        combinations = shaker.generate_solutions(mystery, cache, variables, shake['max_distance'])

        context = {
            'shake' : shake,
            'mystery_coord' : coordinates.geocaching2decimal(*mystery),
            'nb_combinations' : nb_combinations,
            'combinations' : combinations
        }

        return render_template('shaked.html', **context)

    # If no custom markers exists
    # Create one
    if not len(form.customs):
        form.customs.append_entry(forms.CustomItem())

    return render_template('home.html', form=form)

@frontend.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join(frontend.root_path, 'templates', 'static')
    return send_from_directory(static_path, filename)
