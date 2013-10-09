# -*- coding: utf-8 -*-

'''
File: views.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Flask views
'''

import os, operator
from flask import session, Blueprint, render_template, current_app, request, send_from_directory, flash, redirect, url_for
from geoshaker.frontend import forms, rst_reader
from geoshaker.core import shaker, coordinates, arithmetic_coordinates

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
                [(v.form.symbol.data, int(v.form.min_val.data), int(v.form.max_val.data)) for v in form.variables],
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

        cache = arithmetic_coordinates.ArithmeticCoordinates(shake['cache'])
        variables = [shaker.UnknownValue(*elt) for elt in shake['variables']]
        nb_combinations = reduce(operator.mul, [len(elt) for elt in variables])

        if nb_combinations > 100000:
            flash('Too much combinations to shake. Limit is 100000. There are %d combinations with your variables' % nb_combinations)
            return render_template('home.html', form=form)

        # Manage custom markers
        shake['customs'] = []
        customs = []
        for custom in form.customs:

            c_split = forms.cache_re.match(custom.coordinates.data)
            c_coord= coordinates.geocaching2decimal(
                (
                    1 if c_split.group(1) == 'N' else -1,
                    int(c_split.group(2)),
                    float(c_split.group(3))
                ), (
                    1 if c_split.group(4) == 'E' else -1,
                    int(c_split.group(5)),
                    float(c_split.group(6)),
                )
            )
            c = {
                'name': custom.custom_name.data,
                'coordinates': c_coord,
                'circle_radius': int(custom.circle_radius.data),
                'circle_draw': bool(custom.circle_draw.data),
            }
            shake['customs'].append(c)
            if bool(custom.exclude_from.data):
                customs.append((c_coord, c['circle_radius']))

        # Compute combinations
        combinations = shaker.generate_solutions(mystery, cache, variables, customs, shake['max_distance'])

        context = {
            'shake' : shake,
            'mystery_coord' : coordinates.geocaching2decimal(*mystery),
            'nb_combinations' : nb_combinations,
            'combinations' : combinations
        }

        return render_template('shaked.html', **context)


    return render_template('home.html', form=form)

@frontend.route('/help')
def help():
    help_path = 'translations/%s/help.rst' % get_language()
    help_content = rst_reader.read_rst(help_path)

    return render_template('help.html', help_content=help_content)


@frontend.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join(frontend.root_path, 'templates', 'static')
    return send_from_directory(static_path, filename)

@frontend.route('/locale/<locale>/')
def set_locale(locale):
    if locale in current_app.config['LANGUAGES']:
        session['locale'] = locale
    return redirect(url_for('.home'))

def get_language():
    if 'locale' in session:
        return session['locale']
    return request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())
