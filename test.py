#!/usr/bin/env python
""" selftest """
from numpy import isclose
#
try:
    from .distrssi import dist2rssi,rssi2dist
except:
    from distrssi import dist2rssi,rssi2dist

def test_distrssi():
    d = dist2rssi(x=10)
    assert isclose(d, -74.2333216873)
    assert isclose(rssi2dist(ctx=-54,rssi=-74),10)

if __name__ == '__main__':
    test_distrssi()