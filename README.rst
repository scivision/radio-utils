.. image:: https://travis-ci.org/scivision/radio-utils.svg?branch=master
    :target: https://travis-ci.org/scivision/radio-utils
    
.. image:: https://coveralls.io/repos/scivision/radio-utils/badge.svg
    :target: https://coveralls.io/r/scivision/radio-utils

=========
radio-sim
=========

Collection of scripts over the years simulating radio communications (commericial and amateur radio). 
Python scripts by Michael Hirsch, Ph.D.

* fspl.py: Trivial implementation of free space path loss calcuation
* ssbmoddemod.py: simulated SSB transmitter and reciever, with optional frequency error


Install
=======
::

    python -m pip install -e .

Usage
=====


Rain Attenuation
----------------
`**ITU P.838 Specific attenuation model for rain for use in prediction methods** <https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf>`_

considers:

* rain rate [mm/hour]
* frequency [Hz]  1-1000 GHz
* polarization: 0 (horiz)  90 (vertical) or elliptical (degrees)
* elevation angle (degrees)

Show a plot over whole frequency range by setting frequency ``-1``.
Show replication of ITU report plots with ``-v`` option.


SSB mod/demod
--------------  
You can use the ``-e`` option to introduce a "mistuned" receiver frequency.::

    wget http://www.kozco.com/tech/piano2.wav
    
    python ssbmoddemod.py piano2.wav


Free Space Loss
---------------
1km link at 902MHz with 10mW EIRP transmit power and -85dBm receive threshold with 0dBi antenna::

    python free_space_loss.py -h
    python fspl.py 1e3 902e6 10 -85

