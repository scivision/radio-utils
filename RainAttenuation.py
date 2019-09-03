#!/usr/bin/env python
"""
Plots reference figures from
https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf

and normally used to give rain attenuation vs. frequency

NOTE: to make this useful over a satellite-ground path,
       consider factors like rain vs. altitude!

Example plot: 1-1000 GHz, 40 degree elevation angle, 10 mm/hour, vertical polarization (90 deg):
    ./RainAttenuation.py 10 -1 90 40
"""
import numpy as np
from matplotlib.pyplot import figure, show
from argparse import ArgumentParser
from radioutils.impairments import _rain_coeff, rain_attenuation


def main():
    p = ArgumentParser()
    p.add_argument("rainrate", help="rain rate [mm/hour]", type=float)
    p.add_argument(
        "freqHz",
        help="frequency in Hz. Specifying -1 gives full-range frequency sweep plot",
        type=float,
    )
    p.add_argument(
        "polarizationDegrees",
        help="polarization angle 0==horiz, 90==vert, 45==circ [degrees]",
        type=float,
    )
    p.add_argument("elevationDegrees", help="elevation angle above horizon [degrees]", type=float)
    p.add_argument("-v", "--verbose", help="reproduce report plots", action="store_true")
    P = p.parse_args()

    if P.freqHz <= 0 or P.verbose:
        f = np.logspace(9, 12, 200)
        dBkm = get_rain_atten(f, P.rainrate, P.polarizationDegrees, P.elevationDegrees, P.verbose)

        ax = figure().gca()
        ax.loglog(f / 1e9, dBkm)
        ax.set_title(
            f"ITU-R P.838-3 Rain attenuation\n {P.rainrate} mm/hour, elevation {P.elevationDegrees} degrees"
        )
        ax.set_xlabel("frequency [GHz]")
        ax.set_ylabel("rain attenuation [dB/km]")
        ax.grid(True, which="both")

        show()
    else:
        f = P.freqHz
        dBkm = get_rain_atten(f, P.rainrate, P.polarizationDegrees, P.elevationDegrees)

        print(f"{dBkm:0.2e} dB/km attenuation")


def get_rain_atten(f, rainrate, polarization, elevation, verbose=False):
    """ replicate figures from ITU report """

    rain_atten_dBkm = rain_attenuation(f, rainrate, polarization, elevation)

    if verbose:
        ah, kh = _rain_coeff(f, "h", 0.0)
        # %% Figure 1
        ax = figure(1).gca()
        ax.loglog(f / 1e9, kh)
        ax.grid(True, which="both")
        ax.set_title(r"Figure 1, $k$ coefficient for horizontal polarization")
        ax.set_xlabel("frequency [GHz]")
        ax.set_ylabel("$k_h$")
        ax.set_ylim(1e-5, 10)
        ax.set_xlim(1, 1000)
        # %% Figure 2
        ax = figure(2).gca()
        ax.semilogx(f / 1e9, ah)
        ax.grid(True, which="both")
        ax.set_title(r"Figure 2, $\alpha$ coefficient for horizontal polarization")
        ax.set_xlabel("frequency [GHz]")
        ax.set_ylabel(r"$\alpha_h$")
        ax.set_ylim(0.4, 1.8)
        ax.set_xlim(1, 1000)
        # %%
        av, kv = _rain_coeff(f, "v", 0.0)
        # %%
        ax = figure(3).gca()
        ax.loglog(f / 1e9, kv)
        ax.grid(True, which="both")
        ax.set_title(r"Figure 3, $k$ coefficient for vertical polarization")
        ax.set_xlabel("frequency [GHz]")
        ax.set_ylabel("$k_v$")
        ax.set_ylim(1e-5, 10)
        ax.set_xlim(1, 1000)
        # %%
        ax = figure(4).gca()
        ax.semilogx(f / 1e9, av)
        ax.grid(True, which="both")
        ax.set_title(r"Figure 4, $\alpha$ coefficient for vertical polarization")
        ax.set_xlabel("frequency [GHz]")
        ax.set_ylabel(r"$\alpha_v$")
        ax.set_ylim(0.4, 1.8)
        ax.set_xlim(1, 1000)

    return rain_atten_dBkm


if __name__ == "__main__":
    main()
