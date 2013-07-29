#!/usr/bin/env python
# encoding: utf-8
"""
pypostal/sipgate.py - fax a PDF via the sipgate API

See http://www.live.sipgate.de/api/rest for further description of the sipgate REST API.

Created by Maximillian Dornseif on 2010-08-14.
Copyright (c) 2010 HUDORA. All rights reserved.
"""
import logging

import huTools.http


API_VERSION = '2.17.0'


def clean_number(number):
    """Try to clean a phone number"""

    if number.startswith('0'):
        number = '49' + number[1:]
    number = number.replace(' ', '').replace('-', '').replace('+', '').replace('/', '')
    return number


def send_fax_sipgate(uploadfiles, recipients, source=None, guid='', credentials=''):
    """Send a fax to a list of recipients"""

    if len(uploadfiles) > 1:
        raise ValueError('Sipgate currently only supports single PDF uploading')

    if callable(getattr(uploadfiles[0], 'read', None)):
        content = uploadfiles[0].read()
    else:
        content = uploadfiles[0]

    params = dict(version=API_VERSION, targets=','.join('tel:' + clean_number(dest) for dest in recipients))
    if sender:
        params['source'] = 'tel:' + clean_number(sender),

    url = 'https://api.sipgate.net/my/events/faxes/'

    status, response_headers, content = huTools.http.fetch(huTools.http.tools.add_query(url, params), 
                                                           method='POST', credentials=credentials,
                                                           content=content,
                                                           headers={"Content-Type": "application/pdf"})

    if status != 200:
        logging.warn(u'Response from api.sipgate.net: %s %s', status, content)

    return guid
