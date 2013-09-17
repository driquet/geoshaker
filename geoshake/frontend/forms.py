# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

from wtforms import Form, TextField, IntegerField, validators


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
    mystery = TextField('Mystery coordinates', [validators.required()], default="N50 40.000 E003 10.000")
    cache = TextField('Mystery coordinates', [validators.required()], default="N50 40.ABC E3 10.CBA")
    max_distance = IntegerField('Max distance (km)', [validators.required()], default=2)
