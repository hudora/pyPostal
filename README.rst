========
pyPostal
========
pyPostal is an Interface for sending real (paper-based) letters via an API.


There are several providers which offer printing, envelope stuffing and posting services but currently only
https://www.pixelletter.de/ provides such services to SME without contractual hassles and the like.

This interface only supports mailing PDFs which have the Address Placed in the PDF at the `DIN 5008 <http://de.wikipedia.org/wiki/DIN_5008>`_ Address Location.


High-Level Usage
================




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
    >>> print pix.sendPost(['/Users/md/Desktop/Testbrief.pdf', '/Users/md/Desktop/Thesis.pdf'])

    # Send one PDF printet in color and in CO2 neutral fashion.
    >>> print pix.sendPost(['/Users/md/Desktop/Testbrief.pdf'], guid='0815-4711', service=['green', 'color'])

You can provide a GUID ("Transaction IDentifier" in the Pixelletter Documenttion) - this might support a Track and Trace Interface but I havn't seen any documentation on this. Something like https://www.pixelletter.de/de/auftraege.php as an `Atom Feed <http://en.wikipedia.org/wiki/Atom_(standard)>`_ vertainly would be nice.

The Python library currently supports following services:

* green (default, use ``service=[]`` to disable)
* einschreiben
* einschreibeneinwurf
* eigenhaendig
* eigenhaendigrueckschein
* rueckschein
* color

The Pixelletter API also seems to support "Nachnahme", "Postident Comfort" and "Überweisungsvordruck" but they are undocumented and currently not supported by this library. 


See Also
========

* `WWW::Pixelletter <http://cpansearch.perl.org/src/RCL/WWW--Pixelletter-0.1/lib/WWW/Pixelletter.pm>`_ (Perl Module) for Pixelletter
* `PHP Library <http://www.pixelletter.de/xml/pixelletter.class.txt>`_ for Pixelletter
* `Pixelletter Documentation <https://www.pixelletter.de/de/doku2.php>`_
