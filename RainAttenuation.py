#!/usr/bin/env python
"""
Plots reference figures from
https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf

and normally used to give rain attenuation vs. frequency

NOTE: to make this useful over a satellite-ground path,
       consider factors like rain vs. altitude!
"""
import numpy as np
from matplotlib.pyplot import figure,show
#
from radioutils.impairments import _rain_coeff,rain_attenuation


def get_rain_atten(f, rainrate, polarization, elevation, verbose=False):
    rain_atten_dBkm = rain_attenuation(f, rainrate, polarization, elevation)

    if verbose:
# %%
        ah,kh = _rain_coeff(f, 'h', 0.)
# %%
        ax = figure().gca()
        ax.loglog(f/1e9, kh)
        ax.grid(True, which='both')
        ax.set_xlabel('frequency [GHz]')
        ax.set_ylabel('$k_h$')
# %%
        ax = figure().gca()
        ax.semilogx(f/1e9, ah)
        ax.grid(True, which='both')
        ax.set_xlabel('frequency [GHz]')
        ax.set_ylabel(r'$\alpha_h$')
# %%
        av, kv = _rain_coeff(f, 'v', 0.)
# %%
        ax = figure().gca()
        ax.loglog(f/1e9, kv)
        ax.grid(True, which='both')
        ax.set_xlabel('frequency [GHz]')
        ax.set_ylabel('$k_v$')
# %%
        ax = figure().gca()
        ax.semilogx(f/1e9, av)
        ax.grid(True, which='both')
        ax.set_xlabel('frequency [GHz]')
        ax.set_ylabel(r'$\alpha_v$')

    return rain_atten_dBkm


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('rainrate', help='rain rate [mm/hour]', type=float)
    p.add_argument('freqHz', type=float)
    p.add_argument('polarization',
                   help='polarization angle 0==horiz, 90==vert, 45==circ [degrees]',
                   type=float)
    p.add_argument('elevation', 
                   help='elevation angle above horizon [degrees]',
                   type=float)
    p.add_argument('-v','--verbose', action='store_true')
    p = p.parse_args()

    if p.freqHz <= 0:
        f = np.logspace(9, 12, 200)
        dBkm = get_rain_atten(f, p.rainrate, p.polarization, p.elevation,
                              p.verbose)

        ax = figure().gca()
        ax.loglog(f/1e9, dBkm)
        ax.set_xlabel('frequency [GHz]')
        ax.grid(True, which='both')

        show()
    else:
        f = p.freqHz
