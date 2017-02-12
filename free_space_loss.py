#!/usr/bin/env python
from radioutils import Link

if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser(description='trivial computation of free space loss -- no obstructions or fresnel zones are considered!')
    p.add_argument('range_m', type=float, help='range between tx/rx [meters]')
    p.add_argument('freq_hz', type=float, help='frequency [Hz]')
    p.add_argument('tx_dbm',type = float, help='TX power [dBm]')
    p.add_argument('rx_dbm',type = float, help='RX sensitivity [dBm]')
    ar = p.parse_args()

    Link(ar.range_m,ar.freq_hz,ar.tx_dbm,ar.rx_dbm).linkreport()
