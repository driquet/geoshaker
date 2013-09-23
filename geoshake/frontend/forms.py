# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

import re
from wtforms import Form, TextField, FormField, IntegerField, FieldList, validators


# Mystery regexp
# It must be valid coordinates
# Format example : N50 40.000 E003 10.000
mystery_re = re.compile(
    "\s*"
    "(?P<lat_pos>(?:N|S))" # Latitude position
    "\s*"
    "(?P<lat_deg>\d{1,2})" # Latitude degrees
    "\s+" # At least one space
    "(?P<lat_min>\d{1,2}\.\d{1,3})" # Latitude minutes
    "\s+" # At least one space
    "(?P<lon_pos>(?:E|W))" # Latitude position
    "\s*"
    "(?P<lon_deg>\d{1,3})" # Longitude degrees
    "\s+" # At least one space
    "(?P<lon_min>\d{1,2}\.\d{3})" # Longitude minutes
    "$"
)


# Cache regexp
# It must be valid coordinates but it can contains symbol like A-Z
# Format example : N50 40.A00 E3 10.00A
cache_re = re.compile(
    "\s*"
    "(?P<lat_pos>(?:N|S))" # Latitude position
    "\s*"
    "(?P<lat_deg>(?:\d|[A-Z]){1,2})" # Latitude degrees
    "\s+" # At least one space
    "(?P<lat_min>(?:\d|[A-Z]){1,2}\.(?:\d|[A-Z]){1,3})" # Latitude minutes
    "\s+" # At least one space
    "(?P<lon_pos>(?:E|W))" # Latitude position
    "\s*"
    "(?P<lon_deg>(?:\d|[A-Z]){1,3})" # Longitude degrees
    "\s+" # At least one space
    "(?P<lon_min>(?:\d|[A-Z]){1,2}\.(?:\d|[A-Z]){3})" # Longitude minutes
    "$"
)


class UnknownForm(Form):
    symbol = TextField('Symbol', [validators.required()], default="A")
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
    mystery = TextField('Mystery coordinates', [
        validators.Regexp(mystery_re, message="Wrong coordinates format.")
    ], default="N50 40.000 E003 10.000")
    cache = TextField('Cache coordinates', [
        validators.Regexp(cache_re, message="Wrong coordinates format.")
    ], default="N50 40.A00 E3 10.00A")
    max_distance = IntegerField('Max distance (km)', [
        validators.NumberRange(min=1, message="Must be greater or equal to %(min)d."),
    ], default=2)

    # Unknowns / Variables
    variables = FieldList(FormField(UnknownForm), [validators.required()], min_entries=1, max_entries=6)


if __name__ == '__main__':
    coord = "N50 40.A00 E3 10.00A"

    m = mystery_re.match(coord)
    if m:
        print 'MATCH'
        print m.groups()
