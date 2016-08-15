[![Code Climate](https://codeclimate.com/github/scienceopen/radioutils/badges/gpa.svg)](https://codeclimate.com/github/scienceopen/radioutils)
[![Health](https://landscape.io/github/scienceopen/radioutils/master/landscape.png)](https://landscape.io/github/scienceopen/radioutils/master)
[![Build Status](https://travis-ci.org/scienceopen/radioutils.svg?branch=master)](https://travis-ci.org/scienceopen/radioutils)
[![Coverage Status](https://coveralls.io/repos/scienceopen/radioutils/badge.svg)](https://coveralls.io/r/scienceopen/radioutils)

radio-sim
=========

Collection of scripts over the years simulating radio communications

fspl.py: Trivial implementation of free space path loss calcuation

ssbmoddemod.py: simulated SSB transmitter and reciever, with optional frequency error


Installation:
-------------
[Install PyGame](https://scivision.co/python-pygame-installation/)


    python setup.py develop

Demo:
-----
SSB modulation / demodulation of a piano note.  You can use the -e option to introduce a "mistuned" receiver frequency.

    wget http://www.kozco.com/tech/piano2.wav
    
    python ssbmoddemod.py piano2.wav



1km link at 902MHz with 10mW EIRP transmit power and -85dBm receive threshold with 0dBi antenna

    python free_space_loss.py -h
    python fspl.py 1e3 902e6 10 -85

