#!/usr/bin/env python
'''
Single sideband modulation and demodulation
Refer to Lathi's communications text or another reputable source

https://scivision.co/python-pygame-installation/
'''
from pathlib import Path
from numpy import linspace, cos,  pi, arange, int16, log10
from numpy.fft import fft, fftshift
from scipy.signal import butter, lfilter, resample
from matplotlib.pyplot import figure, show
import logging
from argparse import ArgumentParser
# from scikits.audiolab import play #only works with python 2.7 for me, bad sound
import pygame
from scipy.io.wavfile import read

fsaudio = 44100


def main():
    p = ArgumentParser(description='simulate SSB communication')
    p.add_argument('wavfn', help='.wav file to transmit/receive')
    p.add_argument(
        '-e', '--rxerr', help='deliberate error in receive carrier frequency [Hz]', type=float, default=0)
    p.add_argument(
        '--noplot', help='disable media (typ. for selftest)', action='store_false')
    a = p.parse_args()

    ssbsim(a.wavfn, a.rxerr, a.noplot)

    show()


def ssbsim(wavfn, rxerr, doplot):
    wavfn = Path(wavfn).expanduser()
    if not wavfn.suffix == '.wav':
        raise NotImplementedError('only .wav files for now..')
    mfs, mraw = read(wavfn)
    if mraw.ndim == 1:
        mraw = mraw[:, None]

    fc = 50e3  # Hz
    # fm = 500  #Hz
    fs = 350e3  # Hz
    tend = 2
    wc = 2*pi*fc

    ts = 1/fs  # sec

    t = arange(0, tend, ts)
    ns = t.size
    nds = int(ns / (fs/fsaudio))  # number of downsamples to take
    print(ns, 'samples used')

    ncutsamples = int(mfs * tend)
    print(ncutsamples, 'taken from original waveform')
    mraw = mraw[:ncutsamples, 0]  # take left channel

    m, mt = resample(mraw, ns, t)
    m = (m/32768).astype(float)  # normalize for 16 bit file

    # float32 was so noisy
    f = linspace(0, fs/2, ns//2)  # [Hz] for single-sided spectral plotting

    xc = cos(wc*t)  # unmodulated carrier
    # m = np.cos(2*pi*fm*t) #modulation baseband

    # %% modulate SSB
    # sm = m*xc - np.imag(hilbert(m))*np.sin(wc*t) #SSBSC
    sm = m*xc  # DSBSC
    Sm = fftshift(fft(sm))
    # %% demodulate SSB using filter method
    rm = sm * cos((wc+rxerr)*t)  # perfect frequency sync
    # Rm = fftshift(fft(rm))
    # design butterworth lpf  (use FIR for real systems)
    b, a = butter(7, 0.2, 'low')
    # filter output
    rlpf = lfilter(b, a, rm)
    Rlpf = fftshift(fft(rlpf))
    # %% play sound
    if doplot:
        try:
            print(nds, 'resampled samples used for audio playback')
            rlpfrs, trs = resample(rlpf, nds, t)

            pygame.mixer.pre_init(fsaudio, size=-16, channels=1)
            pygame.mixer.init()
            sound = pygame.sndarray.make_sound((rlpfrs*32768).astype(int16))
            # sound = pygame.sndarray.make_sound((mraw).astype(np.int16))
            print(f'sound length {sound.get_length()} seconds')
            sound.play(loops=0)
        except Exception as e:
            logging.warning(f'skipping audio playback due to error  {e}')
        # %% plot
        ax = figure(3).gca()
        ax.plot(t, m)
        ax.set_title('modulation m(t)')
        ax.set_xlabel('time [sec]')
        ax.set_ylabel('amplitude')
        ax.grid(True)

        ax = figure(1).gca()
        ax.plot(f, 20*log10(abs(Sm[ns/2:])))  # plot single-sided spectrum
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('Modulated waveform [dB]')
        ax.set_title('Transmitted Spectrum X(f)')
        # plt.ylim((-100,150))
        ax.grid(True)

        ax = figure(2).gca()
        ax.plot(f, 20*log10(abs(Rlpf[ns/2:])))
        ax.set_title('demodulated m spectrm')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('amplitude [dB]')
        # ax.set_yscale('log')
        ax.grid(True)

        ax = figure(4).gca()
        ax.plot(trs, rlpfrs)
        ax.set_xlabel('time [sec]')
        ax.set_title('demodulated m(t)')
        ax.set_ylabel('amplitude')
        ax.grid(True)


if __name__ == '__main__':
    main()
