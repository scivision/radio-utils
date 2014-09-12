#!/usr/bin/env python
import numpy as np
from numpy.fft import fft,fftshift
from scipy.signal import hilbert,butter,lfilter,resample
import matplotlib.pyplot as plt
#from scikits.audiolab import play #only works with python 2.7 for me, bad sound
import pygame
import pdb
from scipy.io.wavfile import read
from os.path import expanduser

def main(wavFN):
    mfs,mraw = read(expanduser(wavFN))
        
        
    fc = 50e3  #Hz
    #fm = 500  #Hz
    fs = 350e3 #Hz
    tend = 2.0
    pi = np.pi
    wc = 2*pi*fc
    pbfs = 44100
    
    ts = 1./fs #sec
    
    t = np.arange(0,tend,ts)
    ns = len(t)
    nds = int(ns/(fs/pbfs)) #number of downsamples to take
    print(str(ns) + ' samples used')
    
    mraw = mraw[...,0] #picks left channel
    nm = len(mraw)
    ncutsamples = int(mfs * tend)
    print(str(ncutsamples) + ' taken from original waveform')
    mraw = mraw[:ncutsamples]
    
    
    m,mt = resample(mraw,ns,t)
    m = (m/32768.).astype(float)
    
    #float32 was so noisy
    f = np.linspace(0,fs/2,ns/2) #[Hz] for single-sided spectral plotting
    
    xc = np.cos(wc*t) #unmodulated carrier
    #m = np.cos(2*pi*fm*t) #modulation baseband
    
    #%% modulate SSB
    #sm = m*xc - np.imag(hilbert(m))*np.sin(wc*t) #SSBSC
    sm = m*xc #DSBSC
    Sm = fftshift(fft(sm))
    #%% demodulate SSB using filter method
    rxferr = 0.
    rm = sm * np.cos((wc+rxferr)*t) #perfect frequency sync
    Rm = fftshift(fft(rm))
    #design butterworth lpf
    b,a = butter(7,0.2,'low')
    #filter output
    rlpf = lfilter(b,a,rm)
    Rlpf = fftshift(fft(rlpf))
    #%% play sound
    try:
        print(str(nds) + ' resampled samples used for audio playback')
        rlpfrs,trs = resample(rlpf,nds,t)
        #play(m,rate=44100) #garbage audiolab
        pygame.mixer.pre_init(pbfs,size=-16,channels=1)
        pygame.mixer.init()
        sound = pygame.sndarray.make_sound((rlpfrs*32768).astype(np.int16))
        #sound = pygame.sndarray.make_sound((mraw).astype(np.int16))
        print('sound length ' + str(sound.get_length()) + ' seconds')
        sound.play(loops=0)
    except:
        print('skipping audio playback due to error')   
        raise
    #%% plot
    ax = plt.figure(3).gca()
    ax.plot(t,m)
    ax.set_title('modulation m(t)')
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('amplitude')
    ax.grid(True)
    
    ax = plt.figure(1).gca()
    ax.plot(f,20*np.log10(np.abs(Sm[ns/2:]))) #plot single-sided spectrum
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel('Modulated waveform [dB]')
    ax.set_title('Transmitted Spectrum X(f)')
    #plt.ylim((-100,150))
    ax.grid(True)
    
    ax = plt.figure(2).gca()
    ax.plot(f,20*np.log10(np.abs(Rlpf[ns/2:])))
    ax.set_title('demodulated m spectrm')
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel('amplitude [dB]')
    #ax.set_yscale('log')
    ax.grid(True)
    
    
    ax = plt.figure(4).gca()
    ax.plot(trs,rlpfrs)
    ax.set_xlabel('time [sec]')
    ax.set_title('demodulated m(t)')
    ax.set_ylabel('amplitude')
    ax.grid(True)
    
    plt.show()
    
if __name__ == '__main__':
    wavfn = '~/MyVoice.wav'
    main(wavfn)