from pathlib import Path
import warnings
import numpy as np
import scipy.signal as signal
try:
    import pygame
except ImportError:
    pygame = None
#
from .plots import plotfir, plot_fmbaseband

class Link:
    def __init__(self,range_m, freq_hz, tx_dbm=None, rx_dbm=None):
        self.range = np.atleast_1d(range_m)
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
        return 20 * np.log10(4*np.pi / self.c * self.range * self.freq)
    def linkbudget(self):
        if self.rxsens is not None:
            return self.txpwr - self.fspl() - self.rxsens
    def linkreport(self):
        print(f'link margin {self.linkbudget()} dB ')
        print('based on isotropic 0 dBi gain antennas and:')
        print(f'free space path loss {self.fspl()} dB .')
        print(f'RX sensitivity {self.rxsens:0.1f} dBm')
        print(f'TX power {self.power_watts()} watts')
        print(f'for Range [m]= {self.range}  Frequency [MHz]={self.freq_mhz():0.1f}')


def playaudio(dat, fs:int, ofn:Path=None):
    """
    playback radar data using PyGame audio
    """
    if dat is None:
        return

    fs = int(fs)
# %% rearrange sound array to [N,2] for Numpy playback/writing
    if isinstance(dat.dtype,np.int16):
        odtype = dat.dtype
        fnorm = 32768
    elif isinstance(dat.dtype,np.int8):
        odtype = dat.dtype
        fnorm = 128
    elif dat.dtype in ('complex128','float64'):
        odtype = np.float64
        fnorm = 1.0
    elif dat.dtype in ('complex64', 'float32'):
        odtype = np.float32
        fnorm = 1.0
    else:
        raise TypeError(f'unknown input type {dat.dtype}')

    if np.iscomplexobj(dat):
        snd = np.empty((dat.size,2),dtype=odtype)
        snd[:,0] = dat.real
        snd[:,1] = dat.imag
    else:
        snd = dat  # monaural

    snd = snd * fnorm / snd.max()
# %% optional write wav file
    if ofn:
        ofn = Path(ofn).expanduser()
        if not ofn.is_file():
            import scipy.io.wavfile
            print('writing audio to',ofn)
            scipy.io.wavfile.write(ofn, fs, snd)
        else:
            warnings.warn(f'did NOT overwrite existing {ofn}')
# %% play sound
    if 100e3 > fs > 1e3:
        Nloop = 0
        if pygame is None:
            warnings.info('audio playback disabled due to missing Pygame')
            return

        assert snd.ndim in (1,2), 'mono or stereo Nx2'

        # scale to pygame required int16 format
        fnorm = 32768 / snd.max()
        pygame.mixer.pre_init(fs, size=-16, channels=snd.ndim)
        pygame.mixer.init()
        sound = pygame.sndarray.make_sound((snd * fnorm).astype(np.int16))

        sound.play(loops=Nloop)
    else:
        print(f'skipping playback due to fs={fs} Hz')

def loadbin(fn:Path, fs:int, tlim=(0,None), fx0=None, decim=None):
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
        sig = np.fromfile(f, np.complex64, count)

    assert sig.ndim == 1 and np.iscomplexobj(sig), 'file read incorrectly'
    assert sig.size > 0, 'read past end of file, did you specify incorrect time limits?'

    """
    It is useful to frequency translate and downsample the .bin file to drastically
    conserve RAM and CPU in later steps.
    """

    sig, t = freq_translate(sig, fx0, fs, decim)

    return sig, t

def am_demod(sig, fs:int, fsaudio:int, fcutoff:float=10e3, frumble:float=0., verbose:bool=False):
    """
    Envelope demodulates AM with carrier (DSB or SSB)

    inputs:
    -------,
    sig: downconverted (baseband) signal, normally containing amplitude-modulated information with carrier
    fs: sampling frequency [Hz]
    fsaudio: local sound card sampling frequency for audio playback [Hz]
    fcutoff: cutoff frequency of output lowpass filter [Hz]
    frumble: optional cutoff freq for carrier beating removal [Hz]

    outputs:
    --------
    msg: demodulated audio.

    Reference: https://www.mathworks.com/help/dsp/examples/envelope-detection.html
    """
    sig = downsample(sig, fs, fsaudio, verbose)

    # reject signals outside our channel bandwidth
    sig = final_filter(sig, fsaudio, fcutoff, ftype='lpf', verbose=verbose)
# %% ideal diode: half-wave rectifier
    sig = 2*(sig**2)
    sig = np.sqrt(sig).astype(sig.dtype)

    if frumble:
        sig = final_filter(sig, fsaudio, frumble, ftype='hpf', verbose=verbose)

    return sig

def downsample(sig, fs:int, fsaudio:int, verbose:bool=False):
# %% resample
    decim = int(fs/fsaudio)
    print('downsampling by factor of',decim)
    sig = signal.decimate(sig, decim, zero_phase=True)

    return sig

def fm_demod(sig, fs:int, fsaudio:int, fmdev=75e3, verbose:bool=False):
    """
    currently this function discards all but the monaural audio.

    fmdev: FM deviation of monaural modulation in Hz  (for scaling)
    """
    if isinstance(sig, Path):
        sig,t = loadbin(sig, fs)

    # FM is a time integral, angle modulation--so let's undo the FM
    Cfm = fs/(2*np.pi * fmdev)  # a scalar constant
    sig = Cfm * np.diff(np.unwrap(np.angle(sig)))

    # demodulated monoaural audio (plain audio waveform)
    m = downsample(sig, fs, fsaudio, verbose)

    return m, sig


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
    t = np.arange(0, sig.size / fs, 1/fs)
# %% SSB demod
    bx = np.exp(-1j*2*np.pi*fx*t)
    sig *= bx[:sig.size] # sometimes length was off by one

    sig = downsample(sig, fs, fsaudio, fcutoff, verbose)

    return sig


def freq_translate(sig, fx:float, fs:int, decim: int):
# %% assign elapsed time vector
    t = np.arange(0, sig.size / fs, 1/fs)
# %% frequency translate
    if fx is not None:
        bx = np.exp(1j*2*np.pi*fx*t)
        sig *= bx[:sig.size] # downshifted
# %% decimate
    sig, t = decim_sig(sig,fs,decim)
    return sig, t

def decim_sig(sig,fs,decim):
    Ntaps = 100 # arbitrary
    # %% assign elapsed time vector
    t = np.arange(0, sig.size / fs, 1/fs)

    if decim is not None:
        sig = signal.decimate(sig, decim, Ntaps, 'fir', zero_phase=True)
        t = t[::decim]

    return sig,t


#def lpf_design(fs:int, fc:float, L:int):
def lpf_design(fs, fcutoff, L=50):
    """
    Design FIR low-pass filter coefficients "b"
    fcutoff: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """
    # 0.8*fc is arbitrary, for finite transition width

    #return signal.remez(L, [0, 0.8*fcutoff, fcutoff, 0.5*fs], [1., 0.], Hz=fs)
    return signal.firwin(L, fcutoff, nyq=0.5*fs, pass_zero=True)

def hpf_design(fs, fcutoff, L=199):
    """
    Design FIR high-pass filter coefficients "b"
    fcutoff: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """
    # 0.8*fc is arbitrary, for finite transition width

    #return signal.remez(L, [0, 0.8*fcutoff, fcutoff, 0.5*fs], [1., 0.], Hz=fs)
    return signal.firwin(L, fcutoff, nyq=0.5*fs, pass_zero=False,
                         width=10, window='kaiser',scale=True)


def bpf_design(fs, fcutoff, flow=300.,L=256):
    """
    Design FIR bandpass filter coefficients "b"
    fcutoff: cutoff frequency [Hz]
    fs: sampling frequency [Hz]
    flow: low cutoff freq [Hz] to eliminate rumble or beating carriers
    L: number of taps (more taps->narrower transition band->more CPU)

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.remez.html
    """

    # 0.8*fc is arbitrary, for finite transition width

    #return signal.remez(L, [0, 200, 300,0.8*fcutoff, fcutoff, 0.5*fs],
    #                    [0.,1., 0.], Hz=fs)

    b= signal.firwin(L, [flow,fcutoff], pass_zero=False, width=100, nyq=0.5*fs,
                         window='kaiser', scale=True)

    #from oct2py import Oct2Py
    #oc = Oct2Py()
    #oc.eval('pkg load signal')
    #b = oc.fir1(L, [0.03,0.35],'bandpass')

    return b

def final_filter(sig, fs:int, fcutoff:float, ftype:str, verbose:bool=False):

    assert fcutoff < 0.5*fs,'aliasing due to filter cutoff > 0.5*fs'

    if ftype=='lpf':
        b = lpf_design(fs, fcutoff)
    elif ftype=='bpf':
        b = bpf_design(fs, fcutoff)
    elif ftype=='hpf':
        b = hpf_design(fs, fcutoff)
    else:
        raise ValueError(f'Unknown filter type {ftype}')

    sig = signal.lfilter(b, 1, sig)

    if verbose:
        print(ftype,' filter cutoff [Hz] ',fcutoff)
        plotfir(b, fs)

    return sig

