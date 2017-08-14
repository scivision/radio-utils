.. image:: https://travis-ci.org/scivision/radioutils.svg?branch=master
    :target: https://travis-ci.org/scivision/radioutils
.. image:: https://coveralls.io/repos/scivision/radioutils/badge.svg
    :target: https://coveralls.io/r/scivision/radioutils

radio-sim
=========

Collection of scripts over the years simulating radio communications (commericial and amateur radio). 
Python scripts by Michael Hirsch, Ph.D.
Pascal code in the `Pascal <Pascal/>`_ directory by other authors, see `Pascal/README.rst <Pascal/README.rst>`_

fspl.py: Trivial implementation of free space path loss calcuation

ssbmoddemod.py: simulated SSB transmitter and reciever, with optional frequency error


Installation:
-------------
::

    python setup.py develop

Demo:
-----
SSB modulation / demodulation of a piano note.  
You can use the -e option to introduce a "mistuned" receiver frequency.::

    wget http://www.kozco.com/tech/piano2.wav
    
    python ssbmoddemod.py piano2.wav



1km link at 902MHz with 10mW EIRP transmit power and -85dBm receive threshold with 0dBi antenna::

    python free_space_loss.py -h
    python fspl.py 1e3 902e6 10 -85

