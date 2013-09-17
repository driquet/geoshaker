# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

from wtforms import Form, TextField, SelectField, FormField, validators


class GPSCoordinateForm(Form):
    # Latitude data
    lat_pos = SelectField('Position', choices=[('1', 'N'), ('-1', 'S')])
    lat_deg = TextField('Degree', [validators.required(), validators.length(max=2)])
    lat_min_floor = TextField('Minute floor', [validators.required(), validators.length(max=2)])
    lat_min_decimal = TextField('Minute decimal', [validators.required(), validators.length(max=3)])

    # Longitude data
    lon_pos = SelectField('Position', choices=[('-1', 'E'), ('-1', 'W')])
    lon_deg = TextField('Degree', [validators.required(), validators.length(max=2)])
    lon_min_floor = TextField('Minute floor', [validators.required(), validators.length(max=2)])
    lon_min_decimal = TextField('Minute decimal', [validators.required(), validators.length(max=3)])

class UnknownForm(Form):
    pass

class ShakerForm(Form):
    """
        A skaker form is composed of several fields :
            - an origin point
            - a maximum distance to this origin point
            - the mystery coordinates
            - up to six unknowns with boundaries
    """
    # Origin and mystery data
    origin = FormField(GPSCoordinateForm)
    mystery = FormField(GPSCoordinateForm)
    max_distance = TextField('Max distance', [validators.required()])
