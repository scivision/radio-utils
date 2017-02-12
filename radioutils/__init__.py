from __future__ import division
from numpy import log10, pi,atleast_1d,nan

class Link:
    def __init__(self,range_m, freq_hz, tx_dbm=nan, rx_dbm=nan):
        self.range = atleast_1d(range_m)
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
    def freq_ghz(self):
        return self.freq/1e9
    def fspl(self):
        return 20*log10(4*pi/self.c * self.range * self.freq)
    def linkbudget(self):
        return self.txpwr - self.fspl() - self.rxsens
    def linkreport(self):
        print('link margin ' + str(self.linkbudget()) + ' dB ')
        print('based on isotropic 0dBi gain antennas and:')
        print('free space path loss ' + str(self.fspl()) + ' dB .')
        print('RX sensitivity {:0.1f} dBm'.format(self.rxsens))
        print('TX power {} watts'.format(self.power_watts()) )
        print('for Range [m]= '+str(self.range) + '  Frequency [MHz]={:0.1f}'.format(self.freq_mhz()))

