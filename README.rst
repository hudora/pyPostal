========
pyPostal
========
pyPostal is an Interface for sending real (paper-based) letters via an API.


There are several providers which offer printing, envelope stuffing and posting services but currently only
https://www.pixelletter.de/ provides such services to SME without contractual hassles and the like.

This interface only supports mailing PDFs which have the Address Placed in the PDF at the `DIN 5008 <http://de.wikipedia.org/wiki/DIN_5008>`_ Address Location.


High-Level Usage
================

Usage is very easy: Just set up your credentials in the Environment before starting Python::

    export PYPOSTAL_PIXELLETTER_CRED='your@email.com:PASSWORD'

Then call ``pypostal.send_post_pixelletter()`` with the open PDF files or PDF datatream to send and the country code of the recipient::

    >>> import pypostal
    >>> pypostal.send_post_pixelletter(
            [open('/Users/md/Desktop/Testbrief.pdf').read()], 'DE')

If you prefer to hardcode credentials you can provide them via a function call instead via the environment::

    >>> pypostal.send_post_pixelletter([open('Testbrief.pdf')], 'DE', 
                                       username='your@email.com', 
                                       password='PASSWORD')


Pixelletter Interface
=====================

Pixelletter offers a `Bunch of Documentation <https://www.pixelletter.de/de/doku2.php>`_ and a `PHP Library <http://www.pixelletter.de/xml/pixelletter.class.txt>`_. Unfortunately there is no specification of the HTTP-API and the documentation seems also somewhat incomplete and outdated. Also it seems that Pixelletter uses no prebuild XML processing and parsing pipeline but build one arround print statements. This library was build by using trial and error and reverse engeneering the website.


Example Usage
-------------

The Pixelletter interface is streightforwart::

    # Log in
    >>> from pypostal import Pixelletter
    >>> pix = Pixelletter('your_email', 'your_password', test_mode=True)
    
    # Show how many Cents Pixelletter owes you.
    >>> print pix.get_account_info()['customer_credit']
    1995
    
    # Send two PDFs from your Desktop as en Letter
    >>> print pix.sendPost([open('/Users/md/Desktop/Testbrief.pdf'), 
                            open('/Users/md/Desktop/Thesis.pdf')])

    # Send one PDF printet in color and in CO2 neutral fashion.
    >>> print pix.sendPost([open('/Users/md/Desktop/Testbrief.pdf').read()], 
                           guid='0815-4711', service=['green', 'color'])

You can provide a GUID ("Transaction Identifier" in the Pixelletter Documenttion) - this might support a Track and Trace Interface but I havn't seen any documentation on this. Something like https://www.pixelletter.de/de/auftraege.php as an `Atom Feed <http://en.wikipedia.org/wiki/Atom_(standard)>`_ vertainly would be nice.

The Python library currently supports following services:

* green (default, use ``service=[]`` to disable)
* einschreiben (see `DHL / Deutsche Post AG <http://www.deutschepost.de/dpag?skin=lo&check=no&lang=de_DE&tab=1&xmlFile=link1015321_6396>`_ on the differences)
* einschreibeneinwurf
* eigenhaendig
* eigenhaendigrueckschein
* rueckschein
* color

The Pixelletter API also seems to support "Nachnahme", "Postident Comfort" and "Ueberweisungsvordruck" but they are undocumented and currently not supported by this library. 


Planned other Interfaces
========================

We want to support

* Sipgate and Pixelletter Fax interfaces
* Pawisda L-Vin Post / Pinbriefportal SOAP Interface


Links
=====

* `WWW::Pixelletter <http://cpansearch.perl.org/src/RCL/WWW--Pixelletter-0.1/lib/WWW/Pixelletter.pm>`_ (Perl Module) for Pixelletter
* `PHP Library <http://www.pixelletter.de/xml/pixelletter.class.txt>`_ for Pixelletter
* `Pixelletter Documentation <https://www.pixelletter.de/de/doku2.php>`_
* `pyJasper <http://github.com/hudora/pyJasper>`_ and `iReport <http://www.jaspersoft.com/de/ireport>`_ are a decent way to generate PDFs.
