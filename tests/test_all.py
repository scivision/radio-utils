#!/usr/bin/env python
""" selftest """
import pytest
from pytest import approx
from radioutils.distrssi import dist2rssi, rssi2dist
from radioutils import Link
from radioutils.impairments import rain_attenuation


def test_distrssi():
    assert dist2rssi(10) == approx(-74.23110491)
    assert rssi2dist(ctx=-54, rssi=-74) == approx(10.0)


def test_fspl():
    assert Link(10, 2450e6).fspl() == approx(60.23110491)


def test_rainatt():
    assert rain_attenuation(60e9, 10, 45, 40) == approx(4.96584345)


if __name__ == "__main__":
    pytest.main(["-x", __file__])
