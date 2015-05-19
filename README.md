[![Code Climate](https://codeclimate.com/github/scienceopen/radio-sim/badges/gpa.svg)](https://codeclimate.com/github/scienceopen/radio-sim)
[![Health](https://landscape.io/github/scienceopen/radio-sim/master/landscape.png)](https://landscape.io/github/scienceopen/radio-sim/master)

radio-sim
=========

Collection of scripts over the years simulating radio communications

fspl.py: Trivial implementation of free space path loss calcuation

ssbmoddemod.py: simulated SSB transmitter and reciever, with optional frequency error


Installation:
-------------
[Install PyGame](https://scivision.co/python-pygame-installation/)

```
git clone --depth 1 https://github.com/scienceopen/radio-sim
```

Demo:
-----
```
wget http://www.kozco.com/tech/piano2.wav
python ssbmoddemod.py piano2.wav
```

1km link at 902MHz with 10mW transmit power and -85dBm receive threshold
```
python fspl.py -h
python fspl.py 1e3 902e6 10 -85
```
