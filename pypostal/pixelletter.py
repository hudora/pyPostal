#!/usr/bin/env python
# encoding: utf-8
"""
pypostal/postal.py - API-Client für Pixelletter

Created by Maximillian Dornseif on 2010-08-12.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import huTools.http
import huTools.monetary

import logging
import os
import xml.etree.ElementTree as ET

try:
    import config
except ImportError:
    config = object()


class Pixelletter(object):
    """Interface to pixelletter.com"""

    def __init__(self, username, password, test_mode=False):
        self.test_mode = test_mode
        self.username = username
        self.password = password
        self.timeout = 5

    def request(self, content):
        """Send request to API server"""
        status, headers, content = huTools.http.fetch(
            'http://www.pixelletter.de/xml/index.php',
            method='POST',
            content=content,
            multipart=True,
            timeout=self.timeout)

        if status != 200:
            raise RuntimeError("%s -- %r" % (status, content))
        
        return content

    def _get_auth_xml(self):
        """Create the XML root element containing auth data"""
        root = ET.Element('pixelletter', version='1.0')
        auth = ET.SubElement(root, 'auth')
        ET.SubElement(auth, 'email').text = self.username
        ET.SubElement(auth, 'password').text = self.password
        ET.SubElement(auth, 'agb').text = 'ja'
        ET.SubElement(auth, 'widerrufsverzicht').text = 'ja'
        ET.SubElement(auth, 'testmodus').text = 'true' if self.test_mode else 'false'
        ET.SubElement(auth, 'ref').text = 'reference#'
        return root

    def get_account_info(self):
        """Return a dict with account status information, e.g

        {'company': 'Cyberlogi GmbH'
         'customer_credit': 2007, # Betrag in Cent
         'customer_data': '',
         'customer_id': '353***',
         'email': '***@cyberlogi.de',
         'payment_type': 'guthaben',
         'sex': 'yes',
         'tel': '184****',
         'tel_prefix': '017*',
         'title': 'Dr.',
         ...
         }
        """
        root = self._get_auth_xml()
        command = ET.SubElement(root, 'command')
        info = ET.SubElement(command, 'info')
        ET.SubElement(info, 'account:info', type='all')

        content = {'xml': ET.tostring(root)}
        reply = self.request(content)

        # Pixelletter's XML is invalid
        # it is messing with namespaces - remove them to generate valid XML
        content = reply.replace('customer:', 'customer_')
        content = content.replace('tel:prefix', 'tel_prefix')
        content = content.replace('fax:prefix', 'fax_prefix')
        content = content.replace('mobil:prefix', 'mobil_prefix')
        content = content.replace('payment:type', 'payment_type')
        response = ET.fromstring(content)
        info = {}
        for parent in response.getiterator():
            for child in parent:
                text = child.text
                if not text:
                    text = ''
                info[child.tag] = text.strip()
        info['customer_credit'] = int(huTools.monetary.euro_to_cent(info.get('customer_credit', '0')))
        return info

    def send_post(self, uploadfiles, dest_country='DE', guid='', services=None):
        """
        Instructs pixelletter.de to send a letter.

        Send one PDF printed in color and in CO2 neutral fashion.

        >>> print pix.send_post(['./Testbrief.pdf'],
                               guid='01fe190fb6b626154bad760334907ce9',
                               service=['green', 'color'])

        Uploadfiles is a list of files to be send (as a single letter). The first page must contain
        the destination Address.

        dest_country is the country where the letter is going to be send to - this is needed for
        postage calculation.

        guid is some tracking ID specific to the user and can be left blank

        services is a list of additional services requested. It defaults to ['green']
        The Python library currently supports following services:

        * green - GoGreen CO2 neutral postage(default, use ``service=[]`` to disable)
        * einschreiben
        * einschreibeneinwurf
        * eigenhaendig
        * eigenhaendigrueckschein
        * rueckschein
        * color
        """
        if not services:
            services = ['green']
        addoption = set()
        for service in services:
            if service == 'einschreiben':
                addoption.add('27')
            elif service == 'einschreibeneinwurf':
                addoption.add('30')
            elif service == 'eigenhaendig':
                addoption.add('27')
                addoption.add('29')
            elif service == 'eigenhaendigrueckschein':
                addoption.add('27')
                addoption.add('28')
                addoption.add('29')
            elif service == 'rueckschein':
                addoption.add('27')
                addoption.add('29')
            elif service == 'green':
                addoption.add('44')
            elif service == 'color':
                addoption.add('33')
            else:
                raise ValueError('Unbekannter Servicelevel %s - gueltig ist %r' % (service,
                    ['einschreiben', 'einschreibeneinwurf', 'eigenhaendig', 'eigenhaendigrueckschein',
                     'rueckschein', 'green', 'color']))

        root = self._get_auth_xml()

        order = ET.SubElement(root, 'order', type='upload')
        options = ET.SubElement(order, 'options')
        ET.SubElement(options, 'type').text = 'upload'
        ET.SubElement(options, 'action').text = '1'  # Brief
        ET.SubElement(options, 'destination').text = dest_country
        ET.SubElement(options, 'transaction').text = str(guid)
        ET.SubElement(options, 'addoption').text = ','.join(addoption)

        if not uploadfiles:
            raise ValueError('No files to send.')
        form = {'xml': ET.tostring(root)}
        for index, fd in enumerate(uploadfiles):
            form['uploadfile%d' % index] = fd

        reply = self.request(form)
        if not '<msg>Auftrag erfolgreich ' in reply:
            if 'Ihr Guthaben reicht nicht aus.' in reply:
                logging.critical("Pixelletter-Guthaben reicht nicht aus.")
            raise RuntimeError("API fehler: %s" % reply)
        return guid, ''


def send_post_pixelletter(uploadfiles, dest_country='DE', guid='', services=None,
                          username=None, password=None, test_mode=False):

    credentials = os.environ.get('PYPOSTAL_PIXELLETTER_CRED', None)
    if not credentials:
        credentials = getattr(config, 'PYPOSTAL_PIXELLETTER_CRED', None)

    if not username:
        username = credentials.split(':')[0]
    if not password:
        password = credentials.split(':')[1]

    if (not username) or (not password):
        raise RuntimeError('set PYPOSTAL_PIXELLETTER_CRED="user:pass"')
    pix = Pixelletter(username, password, test_mode=test_mode)
    return pix.send_post(uploadfiles, dest_country, guid=guid, services=services)
