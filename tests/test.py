#!/usr/bin/env python
""" selftest """
from numpy import isclose

from radioutils.distrssi import dist2rssi,rssi2dist
from radioutils.fspl import Link


def test_distrssi():
    assert isclose(dist2rssi(10),  -74.23110491)
    assert isclose(rssi2dist(ctx=-54,rssi=-74),10)

def test_fspl():
    assert isclose(Link(10,2450e6).fspl(), 60.23110491)

if __name__ == '__main__':
    test_distrssi()
    test_fspl()