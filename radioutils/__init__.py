from pathlib import Path
from numpy import log10, pi,atleast_1d,nan,sqrt,arange,exp,diff
import scipy.signal as signal
#
from .plots import plotfir, plot_fmbaseband

class Link:
    def __init__(self,range_m, freq_hz, tx_dbm=nan, rx_dbm=nan):
        self.range = atleast_1d(range_m)
        self.freq = freq_hz
        self.txpwr = tx_dbm
        self.rxsens = rx_dbm
        self.c = 299792458. #m/s
    def power_dbm(self):
        return self.txpwr
    def power_watts(self):
        return 10.**((self.txpwr - 30) / 10.)
    def freq_mhz(self):
        return self.freq / 1e6
    def freq_ghz(self):
        return self.freq / 1e9
    def fspl(self):
        return 20*log10(4*pi / self.c * self.range * self.freq)
    def linkbudget(self):
        return self.txpwr - self.fspl() - self.rxsens
    def linkreport(self):
        print(f'link margin {self.linkbudget()} dB ')
        print('based on isotropic 0 dBi gain antennas and:')
        print(f'free space path loss {self.fspl()} dB .')
        print(f'RX sensitivity {self.rxsens:0.1f} dBm')
        print(f'TX power {self.power_watts()} watts')
        print(f'for Range [m]= {self.range}  Frequency [MHz]={self.freq_mhz():0.1f}')

def loadbin(fn:Path, fs:int, tlim=None, fx0=None, decim=None):
    """
    we assume PiRadar has single-precision complex floating point data
    Often we load data from GNU Radio in complex64 (what Matlab calls complex float32) format.
    complex64 means single-precision complex floating-point data I + jQ.

    We don't load the whole file by default, because it can greatly exceed PC RAM.
    """
    Lbytes = 8  # 8 bytes per single-precision complex
    fn = Path(fn).expanduser()

    startbyte = int(Lbytes * tlim[0] * fs)
    assert startbyte % 8 == 0,'must have multiple of 8 bytes or entire file is read incorrectly'

    if tlim[1] is not None:
        assert len(tlim) == 2,'specify start and end times'
        count = int((tlim[1] - tlim[0]) * fs)
    else: # read rest of file from startbyte
        count = -1 # count=None is not accepted

    with fn.open('rb') as f:
        f.seek(startbyte)
        sig = np.fromfile(f,'complex64', count)

    assert sig.ndim==1, 'file read incorrectly'
    assert sig.size > 0, 'read past end of file, did you specify incorrect time limits?'

    """
    It is useful to frequency translate and downsample the .bin file to drastically
    conserve RAM and CPU in later steps.
    """

    dat, t = freq_translate(sig, fx0, fs, decim)

    return dat, t

def am_demod(sig, fs:int, fsaudio:int, fcutoff:float=10e3, verbose:bool=False):
    """
    Envelope demodulates AM with carrier (DSB or SSB)

    inputs:
    -------,
    sig: downconverted (baseband) signal, normally containing amplitude-modulated information with carrier
    fs: sampling frequency [Hz]
    fsaudio: local sound card sampling frequency for audio playback [Hz]
    fcutoff: cutoff frequency of output lowpass filter [Hz]

    outputs:
    --------
    msg: demodulated audio.

    Reference: https://www.mathworks.com/help/dsp/examples/envelope-detection.html
    """
# %% ideal diode: half-wave rectifier
    s = sig**2 * 2
# %% low-pass filter (and anti-aliasing)
    assert fcutoff < 0.5*fsaudio,'aliasing due to filter cutoff > 0.5*fs'
    b = bpf_design(fs, fcutoff)
    s = signal.lfilter(b, 1, s)
# %% resample
    s = signal.resample(s, int(s.size*fsaudio/fs))
    s = sqrt(s).astype(sig.dtype)

    if verbose:
        plotfir(b, fs)

    return s

def fm_demod(sig, fs:int, fsaudio:int, fcutoff:float=10e3, verbose:bool=False):

    if isinstance(sig, Path):
        sig = loadbin(sig, fs)

    return am_demod(diff(sig),
                    fs, fsaudio, fcutoff, verbose)


def ssb_demod(sig, fs:int, fsaudio:int, fx:float, fcutoff:float=5e3, verbose:bool=False):
    """
    filter method SSB/DSB suppressed carrier demodulation

    sig: downconverted (baseband) signal, normally containing amplitude-modulated information
    fs: sampling frequency [Hz]
    fsaudio: local sound card sampling frequency for audio playback [Hz]
    fx: supressed carrier frequency (a priori)
    fcutoff: cutoff frequency of output lowpass filter [Hz]
    """
# %% assign elapsed time vector
    tend = sig.size / fs # end time [sec]
    t = arange(0, tend, 1/fs)
# %% SSB demod
    bx = exp(1j*2*pi*fx*t)
    sig *= bx[:sig.size]
# %% filter
    L = 100 # arbitrary
    b = bpf_design(fs,fcutoff=10e3)
    sig = signal.lfilter(b, 1, sig)

    if verbose:
        plotfir(b, fs)

    return sig, t


def freq_translate(sig, fx:float, fs:int, decim: int):

# %% frequency translate
    if fx is not None:
        bx = exp(1j*2*pi*fx*t)
        sig *= bx[:sig.size] # downshifted
# %% decimate
    sig, t = decim_sig(sig,fs,decim)
    return sig, t

def decim_sig(sig,fs,decim):
    Ntaps = 100 # arbitrary
    # %% assign elapsed time vector
    tend = sig.size / fs # end time [sec]
    t = arange(0, tend, 1/fs)

    if decim is not None:
        sig = signal.decimate(sig, decim, Ntaps, 'fir', zero_phase=True)
        t = t[::decim]

    return sig,t


#def lpf_design(fs:int, fc:float, L:int):
def lpf_design(fs, fcutoff, L=50):
    """
    Design FIR low-pass filter coefficients "b" using Remez algorithm
    fcutoff: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """
    # 0.8*fc is arbitrary, for finite transition width

    #return signal.remez(L, [0, 0.8*fcutoff, fcutoff, 0.5*fs], [1., 0.], Hz=fs)
    return signal.firwin(L, fcutoff, nyq=0.5*fs)

def bpf_design(fs, fcutoff, L=256):
    """
    Design FIR low-pass filter coefficients "b" using Remez algorithm
    fcutoff: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """

    # 0.8*fc is arbitrary, for finite transition width

    #return signal.remez(L, [0, 200, 300,0.8*fcutoff, fcutoff, 0.5*fs],
    #                    [0.,1., 0.], Hz=fs)

    b= signal.firwin(L, [300,fcutoff], pass_zero=False, width=100, nyq=0.5*fs,
                         window='kaiser', scale=True)

    #from oct2py import Oct2Py
    #oc = Oct2Py()
    #oc.eval('pkg load signal')
    #b = oc.fir1(L, [0.03,0.35],'bandpass')

    return b