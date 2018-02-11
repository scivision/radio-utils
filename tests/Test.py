#!/usr/bin/env python
""" selftest """
from math import isclose
import unittest
from radioutils.distrssi import dist2rssi,rssi2dist
from radioutils import Link
from radioutils.impairments import rain_attenuation

class BasicTests(unittest.TestCase):

    def test_distrssi(self):
        assert isclose(dist2rssi(10),  -74.23110491)
        assert isclose(rssi2dist(ctx=-54,rssi=-74),10)

    def test_fspl(self):
        assert isclose(Link(10,2450e6).fspl(), 60.23110491)
        
    def test_rainatt(self):
        assert isclose(rain_attenuation(60e9,10, 45, 40), 4.96584344906)

if __name__ == '__main__':
    unittest.main()
