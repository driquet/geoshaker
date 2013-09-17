# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

from wtforms import Form, TextField, FormField, IntegerField, FieldList, validators


class UnknownForm(Form):
    symbol = TextField('Symbol', [], default="A")
    min_val = IntegerField('Minimum value', [], default=0)
    max_val = IntegerField('Minimum value', [], default=10)


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
    cache = TextField('Cache coordinates', [validators.required()], default="N50 40.A00 E3 10.00A")
    max_distance = IntegerField('Max distance (km)', [validators.required(), validators.NumberRange(min=1)], default=2)

    # Unknown values forms
    variables = FieldList(FormField(UnknownForm), min_entries=6, max_entries=6)
