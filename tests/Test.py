#!/usr/bin/env python
""" selftest """
from numpy import isclose
from numpy.testing import run_module_suite
from radioutils.distrssi import dist2rssi,rssi2dist
from radioutils import Link


def test_distrssi():
    assert isclose(dist2rssi(10),  -74.23110491)
    assert isclose(rssi2dist(ctx=-54,rssi=-74),10)

def test_fspl():
    assert isclose(Link(10,2450e6).fspl(), 60.23110491)

if __name__ == '__main__':
    run_module_suite()
