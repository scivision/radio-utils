from matplotlib.pyplot import figure
from numpy import pi,log10
import scipy.signal as signal

def plotfir(b,fs):

    w, h = signal.freqz(b, worN=2048)

    ax = figure().gca()
    ax.semilogx(fs*0.5/pi*w, 20*log10(abs(h)))
    ax.set_title('filter frequency response')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    ax.grid(which='both', axis='both')
    ax.set_ylim((-70,None))