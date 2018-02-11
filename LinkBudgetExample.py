#!/usr/bin/env python
"""
Link Budget worksheet. Here for Sirius Radio QPSK single channel.
Assumes no processing/spreading gain.

Assume 10^-4 BER is adequate and that the Reed-Solomon coding makes this occur with Eb/No ~ 4 dB

Then, the system as modeled below easily has enough SNR (due to giant EIRP of satellite).
However, it is apparent link margin is too small in face of multipath or intermittant blockage without
further mechanisms such as Sirius does sending two copies of the stream, one time-delayed 4 seconds.
And FEC, etc.
"""
import numpy as np
from scipy.constants import c

freqHz = 2345e6
#%% Thermal noise
kB = 1.38064852e-23 # [m^2 kg s^-2 K^-1]
T = 290 # K
B = 4.5e6 # s^-1

Pn_W = kB*T*B # Watts = kg m^2 s^-3
Pn=10*np.log10(Pn_W) + 30 # dBm 
#%% Path loss
Lrain = 0.1 # [dB] FIXME: guesstimate
Dm = 40000e3 # slant range [meters]

Lpath =  20*np.log10(4*np.pi/c * Dm * freqHz) #[dB]
Lant = 0. #[dB] # assume LNA gain balances cable loss, antenna gain balanced by other uncharacterized losses

Seirp = 60+30 # [dBm] satellite transmit power EIRP

Prx = Seirp-Lrain-Lpath-Lant

print(f'Prx {Prx:.1f} dBm   Pn {Pn:.1f} dBm')

