#!/usr/bin/env python
"""
Wideband FM demodulation and plotting of baseband multiplex spectrum
Michael Hirsch, Ph.D.

Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
"""
from pathlib import Path
from matplotlib.pyplot import show
import seaborn
seaborn.set_context('talk')
#
from radioutils import loadbin, fm_demod, playaudio

fsaudio = 48e3  # [Hz], sampling rate of your soundcard for playback


def main(fn:Path, fs:int, fc:float, tlim:tuple, verbose:bool):
    fn = Path(fn).expanduser()

    assert isinstance(fs, (float, int))
    fs = int(fs)
# %%
    sig = loadbin(fn, fs, tlim)
# %%
    m = fm_demod(sig, fs, fsaudio, fc, 75e3, verbose)
    playaudio(m, fsaudio)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn', help='binary raw IQ capture SDR file to analyze')
    p.add_argument('fs', help='sampling frequency [Hz]', type=float)
    p.add_argument('-fc',help='baseband tunding freq [Hz]',type=float)
    p.add_argument('-t', '--tlim',
                   help='start stop increment [seconds] to load',
                   type=float, nargs=2, default=(0., None))
    p.add_argument('-v','--verbose',action='store_true')

    p = p.parse_args()

    main(p.fn, p.fs, p.fc, p.tlim,p.verbose)

    show()
