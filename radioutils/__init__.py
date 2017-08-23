from __future__ import division
from numpy import log10, pi,atleast_1d,nan
import scipy.signal as signal

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

#def am_demod(sig, fs:int, fc:float=10e3):
def am_demod(sig, fs, fsaudio, fc=10e3):
    """
    inputs:
    -------,
    sig: downconverted (baseband) signal, normally containing amplitude-modulated information with carrier
    fs: sampling frequency [Hz]

    outputs:
    --------
    msg: demodulated audio.
    """
# %% ideal diode: half-wave rectifier
    diode_out = sig * sig>0
# %% low-pass filter
    assert fc < 0.5*fsaudio,'aliasing due to filter cutoff > 0.5*fs'
    b = lpf_design(fs,fc)
    lpf_out = signal.lfilter(b,1,diode_out)
# %% resample
    return signal.resample(lpf_out, int(lpf_out.size*fsaudio/fs))

#def lpf_design(fs:int, fc:float, L:int):
def lpf_design(fs, fc, L=50):
    """
    Design FIR low-pass filter coefficients "b" using Remez algorithm
    fc: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """

    # 0.8*fc is arbitrary, for finite transition width

    return signal.remez(L, [0, 0.8*fc, fc, 0.5*fs], [1., 0.], Hz=fs)