#!/usr/bin/env python
# encoding: utf-8
"""
pypostal/sipgate.py - fax a PDF via the sipgate API

See http://www.live.sipgate.de/api/rest for further description of the sipgate REST API.

Created by Maximillian Dornseif on 2010-08-14.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


# So far this does not work because of sipgate API issues.


import httplib
import urllib
import base64


def send_fax_sipgate(uploadfiles, dest_numbers=[], guid='', username=None, password=None):
    if not username:
        os.environ.get('PYPOSTAL_SIPGATE_CRED', ':').split(':')[0]
    if not password:
        os.environ.get('PYPOSTAL_SIPGATE_CRED', ':').split(':')[1]
    
    sip = Sipgate(username, password)
    return sip.sendFax(uploadfiles, dest_numbers)


class Sipgate(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def sendFax(self, uploadfiles, dest_numbers, guid=''):
        if len(uploadfiles) > 1:
            raise ValueError('Sipgate currently only supports single PDF uploading')
        if hasattr(uploadfiles[0], 'name'):
            filedata = uploadfiles[0].read()
        else:
            filedata = uploadfiles[0]
        
        params = urllib.urlencode({'version': '2.10', 
                                   'targets': ','.join(destnumbers),
                                   'source': filedata.encode('base64')})
        auth = base64.encodestring('%s:%s' % (username, password))[:-1]
        headers = {"Content-type": "application/x-www-form-urlencoded", 
                   "Accept": "application/json",
                   "Authorization": "Basic %s" % auth}
        conn = httplib.HTTPSConnection("api.sipgate.net")
        conn.request("POST", "/my/events/faxes/", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        conn.close()
        return guid

