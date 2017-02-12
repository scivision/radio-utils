"""
Bluetooth Low Energy propagation utilities

These simple functions assume free space propagation, which is only mostly true in outer space. 
In reality, incredible amounts of multipath propagation lead to enhancements and cancellations of signal, 
which make Bluetooth Low Energy location a challenging problem, 
particularly if you need to do it in "real-time" with faster than walking speeds!

Functions:
dist2rssi: Assuming only free space (no reflections) propagation, what would RSSI be vs. distance,
  for a given reference Bluetooth Low Energy transmitter power measurement (dBm) power output in 50 ohms.
rssi2dist: given a reference transmitter power at 1 meter and the measured RSSI, and assuming
  free space propagation (no reflections), what must the distance between TX-RX be?

Michael Hirsch
https://scivision.co
"""

from __future__ import division
from warnings import warn

from . import Link

def dist2rssi(d,notionaltx=-14,freqHz=2450e6):
    """ compute Friis free space loss
    notionaltx: conducted transmit power [dBm] into 50 ohm load
    """
    return notionaltx - Link(d,freqHz).fspl()

def rssi2dist(ctx,rssi,rexp=2):
    ''' simple r^2 loss
    ctx = transmitter EIRP [dBm] received at 1 meter (reference quantity)
    rssi: currently received signal strength [dBm]
    '''
    if ctx>0:
        warn('does your BLE transmitter really give {} dBm at one meter distance?'.format(ctx))
    return (10**((ctx-rssi)/10))**(1/rexp)
