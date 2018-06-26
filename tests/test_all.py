#!/usr/bin/env python
""" selftest """
from math import isclose
import pytest
from radioutils.distrssi import dist2rssi, rssi2dist
from radioutils import Link
from radioutils.impairments import rain_attenuation


def test_distrssi():
    assert isclose(dist2rssi(10),  -74.23110491)
    assert isclose(rssi2dist(ctx=-54, rssi=-74), 10)


def test_fspl():
    assert isclose(Link(10, 2450e6).fspl(), 60.23110491)


def test_rainatt():
    assert isclose(rain_attenuation(60e9, 10, 45, 40), 4.96584344906)


if __name__ == '__main__':
    pytest.main()
