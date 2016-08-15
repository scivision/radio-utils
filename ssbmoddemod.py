#!/usr/bin/env python
'''
Single sideband modulation and demodulatoin
Refer to Lathi's communications text or another reputable source

https://scivision.co/python-pygame-installation/
'''
from __future__ import division
from numpy import linspace,cos,pi,arange,int16,log10,absolute
from numpy.fft import fft,fftshift
from scipy.signal import hilbert,butter,lfilter,resample
from matplotlib.pyplot import figure,show
from warnings import warn
#from scikits.audiolab import play #only works with python 2.7 for me, bad sound
import pygame
from scipy.io.wavfile import read
from os.path import expanduser



def ssbsim(wavfn,rxerr, doplot):
    wavfn = expanduser(wavfn)
    if not wavfn.endswith('.wav'):
        raise NotImplementedError('only .wav files for now..')
    mfs,mraw = read(expanduser(wavfn))
    if mraw.ndim == 1: mraw = mraw[:,None]

    fc = 50e3  #Hz
    #fm = 500  #Hz
    fs = 350e3 #Hz
    tend = 2
    wc = 2*pi*fc
    pbfs = 44100

    ts = 1/fs #sec

    t = arange(0,tend,ts)
    ns = t.size
    nds = int(ns/(fs/pbfs)) #number of downsamples to take
    print(str(ns) + ' samples used')


    ncutsamples = int(mfs * tend)
    print(str(ncutsamples) + ' taken from original waveform')
    mraw = mraw[:ncutsamples,0] #take left channel

    m,mt = resample(mraw,ns,t)
    m = (m/32768).astype(float) #normalize for 16 bit file

    #float32 was so noisy
    f = linspace(0,fs/2,ns//2) #[Hz] for single-sided spectral plotting

    xc = cos(wc*t) #unmodulated carrier
    #m = np.cos(2*pi*fm*t) #modulation baseband

    #%% modulate SSB
    #sm = m*xc - np.imag(hilbert(m))*np.sin(wc*t) #SSBSC
    sm = m*xc #DSBSC
    Sm = fftshift(fft(sm))
    #%% demodulate SSB using filter method
    rm = sm * cos((wc+rxerr)*t) #perfect frequency sync
    Rm = fftshift(fft(rm))
    #design butterworth lpf
    b,a = butter(7,0.2,'low')
    #filter output
    rlpf = lfilter(b,a,rm)
    Rlpf = fftshift(fft(rlpf))
    #%% play sound
    if doplot:
        try:
            print(str(nds) + ' resampled samples used for audio playback')
            rlpfrs,trs = resample(rlpf,nds,t)
            #play(m,rate=44100) #garbage audiolab
            pygame.mixer.pre_init(pbfs,size=-16,channels=1)
            pygame.mixer.init()
            sound = pygame.sndarray.make_sound((rlpfrs*32768).astype(int16))
            #sound = pygame.sndarray.make_sound((mraw).astype(np.int16))
            print('sound length ' + str(sound.get_length()) + ' seconds')
            sound.play(loops=0)
        except Exception as e:
            warn('skipping audio playback due to error  {}'.format(e))
        #%% plot
        ax = figure(3).gca()
        ax.plot(t,m)
        ax.set_title('modulation m(t)')
        ax.set_xlabel('time [sec]')
        ax.set_ylabel('amplitude')
        ax.grid(True)

        ax = figure(1).gca()
        ax.plot(f,20*log10(absolute(Sm[ns/2:]))) #plot single-sided spectrum
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('Modulated waveform [dB]')
        ax.set_title('Transmitted Spectrum X(f)')
        #plt.ylim((-100,150))
        ax.grid(True)

        ax = figure(2).gca()
        ax.plot(f,20*log10(absolute(Rlpf[ns/2:])))
        ax.set_title('demodulated m spectrm')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('amplitude [dB]')
        #ax.set_yscale('log')
        ax.grid(True)

        ax = figure(4).gca()
        ax.plot(trs,rlpfrs)
        ax.set_xlabel('time [sec]')
        ax.set_title('demodulated m(t)')
        ax.set_ylabel('amplitude')
        ax.grid(True)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='simulate SSB communication')
    p.add_argument('wavfn',help='.wav file to transmit/receive',type=str)
    p.add_argument('-e','--rxerr',help='deliberate error in receive carrier frequency [Hz]',type=float,default=0)
    p.add_argument('--noplot',help='disable media (typ. for selftest)',action='store_false')
    a = p.parse_args()

    ssbsim(a.wavfn,a.rxerr, a.noplot)

    show()
