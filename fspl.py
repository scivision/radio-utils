#!/usr/bin/env python3
from __future__ import division
from math import log10, pi

class Link:
    def __init__(self,range_m,freq_hz,tx_dbm,rx_dbm):
        self.range = range_m
        self.freq = freq_hz
        self.txpwr = tx_dbm
        self.rxsens = rx_dbm
        self.c = 299792458 #m/s
    def power_dbm(self):
        return self.txpwr
    def power_watts(self):
        return 10**((self.txpwr-30)/10)
    def freq_mhz(self):
        return self.freq/1e6
    def fspl(self):
        return 20*log10(4*pi/self.c * self.range * self.freq)
    def linkbudget(self):
        return self.txpwr - self.fspl() - self.rxsens
    def linkreport(self):
        print('link budget {:0.1f}'.format(self.linkbudget()) + ' dB ')
        print('free space path loss {:0.1f}'.format(self.fspl()) + ' dB ')
        print('RX sensitivity {:0.1f}'.format(self.rxsens) + ' dBm')
        print('TX power {:0.1f}'.format(self.power_watts()) + ' watts')
        print('for Range [m]={:0.0f}'.format(self.range) +
              ' Frequency [MHz]={:0.1f}'.format(self.freq_mhz()))

if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser(description='analyzes HST data and makes simulations')
    p.add_argument('range_m', type=float, help='range between tx/rx [meters]')
    p.add_argument('freq_hz', type=float, help='frequency [MHz]')
    p.add_argument('tx_dbm',type = float, help='TX power [dBm]')
    p.add_argument('rx_dbm',type = float, help='RX sensitivity [dBm]')
    ar = p.parse_args()

    Link(ar.range_m,ar.freq_hz,ar.tx_dbm,ar.rx_dbm).linkreport()
