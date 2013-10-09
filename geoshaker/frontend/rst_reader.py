#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: rst_reader.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: restructuredtext reader
'''

from docutils.core import publish_parts

def read_rst(file_path, initial_header_level=4):
    """ Read a restructuredtext file and return converted html data """
    try:
        with open(file_path) as f:
            content = ''.join(f.readlines())
            overrides = {'initial_header_level' : initial_header_level}
            parts = publish_parts(content , writer_name='html', settings_overrides=overrides)
            print parts.keys()
            return parts['html_body']
    except:
        return ''
