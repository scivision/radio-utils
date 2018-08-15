#!/usr/bin/env python
"""
Wideband FM demodulation and plotting of baseband multiplex spectrum
Michael Hirsch, Ph.D.

Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
"""
from pathlib import Path
from matplotlib.pyplot import show
from radioutils import loadbin, fm_demod, playaudio
from argparse import ArgumentParser
import seaborn
seaborn.set_context('talk')

fsaudio = 48000  # [Hz], sampling rate of your soundcard for playback


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='binary raw IQ capture SDR file to analyze')
    p.add_argument('fs', help='sampling frequency [Hz]', type=int)
    p.add_argument('-fc', help='baseband tunding freq [Hz]', type=float)
    p.add_argument('-t', '--tlim',
                   help='start stop increment [seconds] to load',
                   type=float, nargs=2, default=(0., None))
    p.add_argument('-v', '--verbose', action='store_true')

    P = p.parse_args()

    fn = Path(P.fn).expanduser()

    assert isinstance(P.fs, (float, int))
    fs = int(P.fs)
# %%
    sig = loadbin(fn, fs, P.tlim)
# %%
    m = fm_demod(sig, fs, fsaudio, P.fc, 75e3, P.verbose)
    playaudio(m, fsaudio)

    show()


if __name__ == '__main__':
    main()
