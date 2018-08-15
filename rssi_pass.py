#!/usr/bin/env python
""" michael hirsch
1-D simulation of free-space propagation--signal strength differences with omni antennas
and devices passing at different closest approach distances

This is not what real-life signals would show (except in outer space) due to multipath constructive/destrubtive interference
"""
import numpy as np
from matplotlib.pyplot import show, subplots
from radioutils import Link
from argparse import ArgumentParser
import seaborn as sns
sns.set_context('poster')


def main():
    p = ArgumentParser(description='Shows free space RSSI vs. simultaneous parallel tracks')
    p.add_argument('xm', help='start stop step values of x-displacement [m]', nargs=3, type=float)
    p.add_argument('-y', '--ym', help='y-offset [m] (closest approach to TX', nargs='+', type=float, default=[1])
    p.add_argument('-n', '--noisevar',
                   help='variance of noise (dB) to add', type=float, default=0)
    P = p.parse_args()

    x = np.arange(P.xm[0], P.xm[1], P.xm[2])
    y = np.atleast_1d(P.ym)

    dist = np.hypot(x[:, None], y[None, :])

    Pr_dbm = comprx(Pt_W=1e-4, d=dist)
    Pr_dbm = add_noise(Pr_dbm, P.noisevar)

    plotsig(x, y, dist, Pr_dbm)

    show()


def comprx(Pt_W, d):
    """
    Input:
    Pt_W: conducted transmit power in Watt
    d: 2-D array of distances from transmitter, where rows are time and columns are each device
    Output:
    Pr_dbm: received power at RX antenna terminals in dBm
    """
    Pt_dbm = 10*np.log10(Pt_W*1000)
    L = Link(d, 2450e6, Pt_dbm)
    return Pt_dbm - L.fspl()


def add_noise(sig, var):
    return sig + var*np.random.standard_normal(sig.shape)


def plotsig(x, y, d, Pr_dbm):
    fg, (ax1, ax2) = subplots(2, 1, sharex=True)

    ax1.set_title('distance of receiver from transmitters,y='+str(y))
    ax1.plot(x, d)
    ax1.set_ylabel('distance [m]')
    # ax1.set_xlabel('x-location [m]')
    # ax1.legend(loc='best')

    ax2.plot(x, Pr_dbm)
    ax2.set_title('Power received, y='+str(y))
    ax2.set_ylabel('$P_R$ [dBm]')
    ax2.set_xlabel('x-location [m]')
    # ax2.legend(loc='best')
    ax2.grid(True)


if __name__ == '__main__':
    main()
