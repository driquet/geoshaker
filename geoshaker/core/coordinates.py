#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: coordinates.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Deals with GPS coordinates
'''

from math import radians, cos, sin, asin, sqrt, floor, fabs

class DecimalDegrees:
    """
        Decimal degrees coordinates
        Composed of two values : latitude and longitude
    """
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


    def __repr__(self):
        return '%f %f' % (self.lat, self.lon)

    def to_geocaching_string(self):
        # Determining N/S and E/W
        lat_pos = 'N' if self.lat >= 0 else 'S'
        lon_pos = 'E' if self.lon >= 0 else 'W'

        lat = fabs(self.lat)
        lon = fabs(self.lon)

        # Computing degrees
        lat_deg = floor(lat)
        lon_deg = floor(lon)

        # Computing minutes
        lat_min = (lat - lat_deg) * 60
        lon_min = (lon - lon_deg) * 60

        return '%s%d %.3f %s%d %.3f' % (lat_pos, lat_deg, lat_min, lon_pos, lon_deg, lon_min)

    def distance_to(self, other):
        """
            Compute the distance between two coordinates
            Use the haversine formula to calculate the great-circle distance between two points
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [self.lon, self.lat, other.lon, other.lat])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km

def geocaching2decimal(lat, lon):
    """
        Create decimal degrees coordinates from geocaching coordinates
        Geocaching coordinates are formated as follow:
            N50°40.232 E3°03.232
        lat and lon are tuples:
            (sign, degree, minutes)
        usage:
            geocaching2decimal((1, 50, 40.232), (1, 3, 3.232))
    """
    lat = lat[0] * (lat[1] + lat[2]/60)
    lon = lon[0] * (lon[1] + lon[2]/60)
    return DecimalDegrees(lat, lon)



if __name__ == '__main__':
    a = geocaching2decimal((1, 41, 36.455), (-1, 88, 12.221))
    b = geocaching2decimal((1, 35, 8.073), (-1, 85, 21.505))

    print a
    print b

    print a.distance_to(b)

    a = DecimalDegrees(41.607583, -88.203683)
    b = DecimalDegrees(41.650667, -88.255467)

    print a
    print b

    print a.distance_to(b)

