from matplotlib.pyplot import figure
import numpy as np
import scipy.signal as signal

def plotfir(b,fs):

    w, h = signal.freqz(b, worN=2048)

    ax = figure().gca()
    ax.semilogx(fs*0.5/np.pi*w, 20*np.log10(abs(h)))
    ax.set_title('filter frequency response')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    ax.grid(which='both', axis='both')
    ax.set_ylim((-70,None))

def plotraw(sig, fs:int, Nraw:int=10000):
    t = np.arange(0, sig.size/fs, 1/fs)

    ax = figure().gca()
    ax.plot(t[:Nraw], sig[:Nraw].real, 'b')

    ax.set_title('raw waveform preview')
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('amplitude')


def plot_fmbaseband(sig, fs:int, fmax:float):
    """
    inputs:
    -------
    sig: baseband of FM signal (after discriminator)
    fs: sampling freq. [Hz]
    """
#%% demodulated audio
    t = np.arange(0., sig.size / fs, 1/fs)

    ax = figure().gca()
    ax.plot(t,sig)
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('amplitude')
    ax.set_title('FM baseband')
    ax.grid(True)
#%% spectrogram
    fg = figure()
    ax = fg.gca()

    hi = ax.specgram(sig,
                     Fs=fs,  vmin=-100)[-1]
    fg.colorbar(hi,ax=ax)
    ax.set_title('WBFM baseband multiplex')
    ax.set_ylabel('frequency [Hz]')
    ax.set_xlabel('time [sec]')
#%% periodogram
    fg = figure()
    ax = fg.gca()

    f,Sp = signal.welch(sig, fs,
                nperseg=4096,
                window = 'hann',
#                    noverlap=Nol,
                nfft=4096,
                return_onesided=True
                )

    ax.plot(f,10*np.log10(Sp))
    ax.set_ylabel('PSD [dB/Hz]')
    ax.set_xlabel('frequency [Hz]')
    ax.set_title('WBFM baseband multiplex: periodogram')
    ax.set_xlim((0,fmax))
    ax.set_ylim((-80,None))
    ax.grid(True)
    fg.tight_layout()
