# -*- coding: utf-8 -*-

'''
File: arithmetic_coordinates.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Parse arithmetic based coordinates in order to evaluate them
'''

import re
from geoshaker.core import arithmetic_expr

# Base regular expression
arithm_expr = r'\[[\(\) a-z0-9\+\-\*\\]+\]'
atom_expr = r'[0-9a-z]'
coord_expr = '(?:%s|%s)' % (arithm_expr, atom_expr)

# Whole coordinate regular expression
coordinates_re = re.compile(
    "\s*"
    "(?P<lat_pos>(?:N|S))" # Latitude position
    "\s*"
    "(?P<lat_deg>%s{1,2})"
    "\s+"
    "(?P<lat_min_1>%s{1,2})"
    "\."
    "(?P<lat_min_2>%s{1,3})"
    "\s+"
    "(?P<lon_pos>(?:E|W))" # Longitude position
    "\s*"
    "(?P<lon_deg>%s{1,3})"
    "\s+"
    "(?P<lon_min_1>%s{1,2})"
    "\."
    "(?P<lon_min_2>%s{1,3})"
    % (coord_expr, coord_expr, coord_expr, coord_expr, coord_expr, coord_expr)
)

class CoordinatesExpression(object):
    def eval(self, values):
        pass


class StringExpression(CoordinatesExpression):
    """
        A string expression contains variables but with no arithmetic operations
        Example : '4ab'
    """

    def __init__(self, expr):
        self.expr = expr

    def eval(self, values):
        """ Consist in replacing each variable by its value """
        str_value = self.expr
        for symbol, value in values.items():
            str_value = str_value.replace(symbol, str(value))
        return str_value


class ArithmeticExpression(CoordinatesExpression):
    """
        An arithmetic expression contains arithmetic operations (+, -, *, /)
        Example : 4 * (a + b) + c
    """
    def __init__(self, expr):
        self.expr = arithmetic_expr.parse_expr(expr)
        if self.expr is None:
            raise SyntaxError

    def eval(self, values):
        return self.expr.eval(values)



class ArithmeticCoordinates:
    def __init__(self, str_coordinates):
        """
            Parse a set of coordinates into several parts (coordinates expression)
            so that it could be evaluted
            Example : N50 40.A(B+C*A)5 E003 23.(A+B*C)
        """
        # Try to match the regular expression
        coord_m = coordinates_re.match(str_coordinates)
        if not coord_m:
            raise SyntaxError

        # Positions
        self.lat_pos = 1 if coord_m.group('lat_pos') == 'N' else -1
        self.lon_pos = 1 if coord_m.group('lon_pos') == 'E' else -1

        # Latitude data
        self.lat_deg = extract_expressions(coord_m.group('lat_deg'))
        self.lat_min_1 = extract_expressions(coord_m.group('lat_min_1'))
        self.lat_min_2 = extract_expressions(coord_m.group('lat_min_2'))

        # Longitude data
        self.lon_deg = extract_expressions(coord_m.group('lon_deg'))
        self.lon_min_1 = extract_expressions(coord_m.group('lon_min_1'))
        self.lon_min_2 = extract_expressions(coord_m.group('lon_min_2'))

    def eval(self, values):
        """
        Eval each part of expressions and return a decimal degree instance
        """
        lat = (
            self.lat_pos,
            int(self.eval_expressions(self.lat_deg, values)),
            int(self.eval_expressions(self.lat_min_1, values)),
            int(self.eval_expressions(self.lat_min_2, values))
        )
        lon = (
            self.lon_pos,
            int(self.eval_expressions(self.lon_deg, values)),
            int(self.eval_expressions(self.lon_min_1, values)),
            int(self.eval_expressions(self.lon_min_2, values))
        )

        return lat, lon

    def eval_expressions(self, expressions, values):
        return ''.join([str(elt.eval(values)) for elt in expressions])


def extract_expressions(str_expressions):
    expressions = []
    for expr in re.findall(coord_expr, str_expressions):
        if len(expr) == 1:
            # Basic string expression
            expressions.append(StringExpression(expr))
        else:
            # Arithmetic operation (need to remove brackets)
            expressions.append(ArithmeticExpression(expr[1:-1]))
    return expressions




if __name__ == '__main__':
    expr = 'N5a 4[b + a].1[a+c+b][a+c] E003 10.231'
    values = {
        'a' : 5,
        'b' : 2,
    }
    a = ArithmeticCoordinates(expr)
    print a.eval(values)
