#!/usr/bin/env python3
""" michael hirsch
1-D simulation of free-space propagation--signal strength differences with omni antennas
and devices passing at different closest approach distances

This is not what real-life signals would show (except in outer space) due to multipath constructive/destrubtive interference
"""

from __future__ import division
import numpy as np
from matplotlib.pyplot import show,subplots
import seaborn as sns
#
try:
    from .fspl import Link
except:
    from fspl import Link

def comprx(Pt_W, d):
    """
    Input:
    Pt_W: conducted transmit power in Watt
    d: 2-D array of distances from transmitter, where rows are time and columns are each device
    Output:
    Pr_dbm: received power at RX antenna terminals in dBm
    """
    Pt_dbm = 10*np.log10(Pt_W*1000)
    L = Link(d,2450e6,Pt_dbm)
    return Pt_dbm - L.fspl()

def plotsig(x,d,Pr_dbm):
    fg,(ax1,ax2) = subplots(2,1,sharex=True)

    ax1.set_title('distance of receiver from transmitters,y='+str(y))
    ax1.plot(x,d)
    ax1.set_ylabel('distance [m]')
    #ax1.set_xlabel('x-location [m]')
   # ax1.legend(loc='best')


    ax2.plot(x,Pr_dbm)
    ax2.set_title('Power received, y='+str(y),fontsize=18)
    ax2.set_ylabel('$P_R$ [dBm]',fontsize=16)
    ax2.set_xlabel('x-location [m]',fontsize=16)
   # ax2.legend(loc='best')
    ax2.grid(True)

if __name__ == '__main__':
    x = x = np.linspace(-10.,10., 500)
    y=[3,5.5] #distance from transmitter at closest approach [m]

    dist = np.hstack((np.hypot(x,y[0])[:,None],
                               np.hypot(x,y[1])[:,None]))

    Pr_dbm = comprx(Pt_W=1e-4, d=dist)
    plotsig(x,dist,Pr_dbm)

    show()