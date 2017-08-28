#!/usr/bin/env python
"""
Wideband FM demodulation and plotting of baseband multiplex spectrum
Michael Hirsch, Ph.D.

Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
"""
from pathlib import Path
from matplotlib.pyplot import show
#
from radioutils import loadbin, fm_demod, plot_fmbaseband, playaudio

fsaudio = 48e3  # [Hz], sampling rate of your soundcard for playback


def main(fn:Path, fs:int, tlim:tuple):
    fn = Path(fn).expanduser()

    assert isinstance(fs,(float,int))
    fs = int(fs)

    sig,t = loadbin(fn, fs, tlim)

    m = fm_demod(sig, fs, fsaudio)
    playaudio(m, fsaudio)

    plot_fmbaseband(sig, fs)






if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='binary raw IQ capture file recorded by SDR to analyze')
    p.add_argument('fs',help='sampling frequency [Hz]',type=float)
    p.add_argument('-t','--tlim',help='start stop increment [seconds] to load',type=float,nargs=2,default=(0.,None))

    p = p.parse_args()

    main(p.fn, p.fs, p.tlim)

    show()