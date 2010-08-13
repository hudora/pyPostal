#!/usr/bin/env python
# encoding: utf-8
"""
pypostal/__init__.py

Created by Maximillian Dornseif on 2010-08-12.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import xml.etree.ElementTree as ET
from httplib2 import Http
import uuid


def encode_multipart_formdata(fields):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    # Based on From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
    boundary = '----------ThIs_Is_tHe_bouNdaRY_$%s' % (uuid.uuid4())
    out = []
    # if it's dict like then use the items method to get the fields
    if hasattr(fields, "items"):
        fields = fields.items()
    for (key, value) in fields:
        out.append('--' + boundary)
        out.append('Content-Disposition: form-data; name="%s"' % key)
        out.append('')
        out.append(value)
    out.append('--' + boundary + '--')
    out.append('')
    body = '\r\n'.join([str(x) for x in out])
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body


class Pixelletter(object):
    def __init__(self, username, password, test_mode=False):
        self.url = 'http://www.pixelletter.de/xml/index.php'
        self.test_mode = test_mode
        self.username = username
        self.password = password
        self.files = []

    def get_account_info(self):
        root = ET.Element('pixelletter', version='1.0')
        auth = ET.SubElement(root, 'auth')
        ET.SubElement(auth, 'email').text = self.username
        ET.SubElement(auth, 'password').text = self.password

        command = ET.SubElement(root, 'command')
        info = ET.SubElement(command, 'info')
        ET.SubElement(info, 'account:info ', type='all')
        data = ET.tostring(root)
        content_type, content = encode_multipart_formdata(fields=dict(xml=data))
        resp, content = Http().request(self.url, 'POST', body=content, headers={"Content-Type": content_type})
        if not resp.get('status') == '200':
            raise RuntimeError("%s -- %r" % (content, resp))
        return content
    
# <?xml version="1.0" encoding="iso-8859-1"?>
# <pixelletter version="1.1">
#   <customer:id>353524</customer:id>
#   <customer:data>
#     <company>Cyberlogi GmbH</company>
#     <sex>m</sex>
#     <title>Dr.</title>
#     <firstname>Maximillian</firstname>
#     <lastname>Dornseif</lastname>
#     <street>?lfestr. 20</street>
#     <pcode>42477</pcode>
#     <city>Radevormwald</city>
#     <country>DE</country>
#     <tel:prefix>0175</tel:prefix>
#     <tel>1843787</tel>
#     <fax:prefix />
#     <fax />
#     <mobil:prefix />
#     <mobil />
#     <email>verwaltung@cyberlogi.de</email>
#     <payment:type>guthaben</payment:type>
#   </customer:data>
#   <customer:credit currency="EUR">20.08</customer:credit>
# </pixelletter>

    
    
    #def generate_pdf(self,
    #

    def addFile(self, filename):
        self.files.append(filename)

    def sendPost(self, dest_country='DE'):

        #if len(self.files) < 1:
        #    raise ValueError( "No files to send...")

        root = ET.Element('pixelletter', version='1.0')
        auth = ET.SubElement(root, 'auth')
        ET.SubElement(auth, 'email').text = self.username
        ET.SubElement(auth, 'password').text = self.password
        ET.SubElement(auth, 'agb').text = 'ja'
        ET.SubElement(auth, 'widerrufsverzicht').text = 'ja'
        ET.SubElement(auth, 'testmodus').text = 'true' if self.test_mode else 'false'

        order = ET.SubElement(root, 'order')
        options = ET.SubElement(order, 'options')
        ET.SubElement(options, 'type').text = 'upload'
        ET.SubElement(options, 'action').text = '1'
        ET.SubElement(options, 'destination').text = dest_country

        #<control>
        #<location>
        #<transaction> In der Zeile transaction: können Sie hinter den Doppelpunkt eine eigene Transaktionsnummer oder einen kurzen Text angeben, den Sie mit dem Auftrag in Verbindung bringen. Dieses Feld kann aber auch leer gelassen werden bzw. komplett entfernt werden.
        #<addoption> 27 steht für „Einschreiben“ 28 steht für zusätzlichen „Rückschein“ (nur zusammen mit 27) 29 steht für zusätzlich „Eigenhändig“ (nur zusammen mit 27) 30 steht für „Einschreiben Einwurf“
        # 30 ist nicht kombinierbar mit anderen Einschreibe-Variationen. 27 ist Pflichtangabe, wenn 28 oder 29 verwendet werden soll. 28 oder 29 können beide oder einzeln mit 27 kombiniert werden. Hier einige Beispiele:
        # addoption: addoption: addoption: addoption:
        # 27,28,29	-> bedeutet Eigenhändiges Einschreiben mit Rückschein 27,29	-> bedeutet Eigenhändiges Einschreiben ohne Rückschein 27	-> bedeutet normales Einschreiben 30	-> bedeutet Einschreiben Einwurf
        #<returnaddress>

        print ET.tostring(root)
        tree = ET.ElementTree(root)
        print dir(tree)
        #buf = StringIO()
        #tree.write(buf, encoding="utf-8")
        #ret = buf.getvalue()
        #buf.close()
        #return ret

        # $self->_submitForm( $xml );

pix = Pixelletter('mail', 'pass')
print pix.get_account_info()
