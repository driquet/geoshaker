# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

import re, string, collections
from wtforms import Form, TextField, FormField, IntegerField, FieldList, validators, FloatField, BooleanField


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
# It must be valid coordinates but it can contains symbol like a-z
# Format example : N50 40.A00 E3 10.00A
cache_re = re.compile(
    "\s*"
    "(?P<lat_pos>(?:N|S))" # Latitude position
    "\s*"
    "(?P<lat_deg>(?:\d|[a-z]){1,2})" # Latitude degrees
    "\s+" # At least one space
    "(?P<lat_min>(?:\d|[a-z]){1,2}\.(?:\d|[a-z]){1,3})" # Latitude minutes
    "\s+" # At least one space
    "(?P<lon_pos>(?:E|W))" # Latitude position
    "\s*"
    "(?P<lon_deg>(?:\d|[a-z]){1,3})" # Longitude degrees
    "\s+" # At least one space
    "(?P<lon_min>(?:\d|[a-z]){1,2}\.(?:\d|[a-z]){3})" # Longitude minutes
    "$"
)


class UnknownForm(Form):
    symbol = TextField('Symbol', [validators.required()], default="a")
    min_val = TextField('Minimum value', [validators.required()], default='0')
    max_val = TextField('Minimum value', [validators.required()], default='9')

    def validate_symbol(form, field):
        if len(field.data) > 1 or field.data not in string.lowercase:
            raise validators.ValidationError('Symbol must be a character (a-z)')


    def validate_min_val(form, field):
        if not field.data.isdigit():
            raise validators.ValidationError('Min value must be an integer')
        val = int(field.data)
        if val < 0:
            raise validators.ValidationError('Min value must be positive')

        if form.max_val.data.isdigit():
            val_max = int(form.max_val.data)
            if val > val_max:
                raise validators.ValidationError('Min value must greater or equal to max value')

    def validate_max_val(form, field):
        if not field.data.isdigit():
            raise validators.ValidationError('Max value must be an integer')
        val = int(field.data)
        if val < 0:
            raise validators.ValidationError('Max value must be positive')


class CustomItem(Form):
    custom_name = TextField('Name', [validators.required()])
    coordinates = TextField('Coordinates', [validators.Regexp(mystery_re, message="Wrong coordinates format.")])
    circle_draw = BooleanField('Draw circle')
    circle_radius = IntegerField('Circle radius (m)', [
        validators.NumberRange(min=1, message="Must be greater or equal to %(min)d.")
    ], default=161)
    exclude_from = BooleanField('Exclude combinations')




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
    ], default="N50 38.455 E003 02.670")
    cache = TextField('Cache coordinates', [
        validators.Regexp(cache_re, message="Wrong coordinates format.")
    ], default="N50 38.aa2 E003 02.5a3")
    max_distance = FloatField('Max distance (km)', [
        validators.NumberRange(min=0, message="Must be greater or equal to %(min)d."),
    ], default=2)

    # Unknowns / Variables
    variables = FieldList(FormField(UnknownForm), [validators.required()], min_entries=1, max_entries=6)

    # Custom items
    customs = FieldList(FormField(CustomItem))

    def validate_cache(form, field):
        symbols = set(c for c in field.data if c in string.lowercase)
        variables = [s.form.symbol.data for s in form.variables]

        if len(symbols - set(variables)):
            raise validators.ValidationError('Missing unknown value(s) : %s' % ', '.join(symbols - set(variables)))

        # Looking for multiple declaration of the same variable
        variables_counter = collections.Counter(variables)
        multi_declaration = [var for var,count in variables_counter.items() if count > 1]

        if len(multi_declaration):
            raise validators.ValidationError('Multi declaration of variable(s) below : %s' % ', '.join(multi_declaration))

        # Looking for variable not used in the cache coordinates
        variables_used = [var for var in variables if var not in symbols]

        if len(variables_used):
            raise validators.ValidationError('Useless variable declaration(s) below : %s' % ', '.join(variables_used))



if __name__ == '__main__':
    coord = "N50 40.A00 E3 10.00A"

    m = mystery_re.match(coord)
    if m:
        print 'MATCH'
        print m.groups()
