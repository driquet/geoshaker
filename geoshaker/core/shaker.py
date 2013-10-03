#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: coordinates.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Deals with GPS coordinates
'''

import itertools
import coordinates

class UnknownValue:
    """ Represents an unknown value """
    def __init__(self, symbol, bound_min, bound_max):
        self.symbol = symbol
        self.bound_min = bound_min
        self.bound_max = bound_max

    def __iter__(self):
        return iter(xrange(self.bound_min, self.bound_max + 1))

    def __len__(self):
        return self.bound_max - self.bound_min + 1


def generate_solutions(origin, coord, unknowns, excluded_area, max_distance=2):

    origin = coordinates.geocaching2decimal(*origin)

    solutions = []
    for combination in itertools.product(*unknowns):
        substitutions = {unknowns[i].symbol: combination[i] for i in xrange(len(combination))}

        try:
            attempt_lat, attempt_lon = coord.eval(substitutions)
        except ValueError:
            continue
        # Specific process for last element (floating part)
        # If there is less than 3 digits, we add zeros (to the left)

        # Verify that values are valid
        if valid_coordinates(attempt_lat, attempt_lon):

            lat_floating_part = str(attempt_lat[3])
            lat_floating_part = '0' * (3 - len(lat_floating_part)) + lat_floating_part

            lon_floating_part = str(attempt_lon[3])
            lon_floating_part = '0' * (3 - len(lon_floating_part)) + lon_floating_part

            attempt_lat = (attempt_lat[0], attempt_lat[1], float('%d.%s' % (attempt_lat[2], lat_floating_part)))
            attempt_lon = (attempt_lon[0], attempt_lon[1], float('%d.%s' % (attempt_lon[2], lon_floating_part)))

            attempt = coordinates.geocaching2decimal(attempt_lat, attempt_lon)

            # Verify that this combination is not too far from the origin point
            d = origin.distance_to(attempt)
            if d > max_distance:
                continue

            # Is it inside a excluded area ?
            excluded = False
            for area_coord, area_distance in excluded_area:
                d = area_coord.distance_to(attempt)
                if d <= (area_distance/float(1000)):
                    excluded = True
                    break

            if not excluded:
                solutions.append((combination, attempt, d))


    return solutions


def substitute(coord_value, substitutions):
    str_value = str(coord_value)
    for symbol, value in substitutions:
        str_value = str_value.replace(symbol, str(value))
    return float(str_value)

def valid_coordinates(lat, lon):
    return value_between(lat[1], 0, 99) and \
       value_between(lat[2], 0, 99) and \
       value_between(lat[3], 0, 999) and \
       value_between(lon[1], 0, 999) and \
       value_between(lon[2], 0, 99) and \
       value_between(lon[3], 0, 999)


def value_between(val, val_min, val_max):
    return val >= val_min and val <= val_max


if __name__ == '__main__':
    a = UnknownValue('A', 0, 8)
    b = UnknownValue('B', 4, 8)
    c = UnknownValue('C', 0, 9)

    coord = ((1, '50', '40', 'AB4'), (1, 'A', '40', 'CC4'))
    orig = ((1, 50, 40.500), (1, 3, 40.225))


    total = len(a) * len(b) * len(c)
    print len(generate_solutions(orig, coord, [a,b,c])), total
