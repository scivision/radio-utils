# Radio Simulations in Python

[![ci](https://github.com/scivision/radio-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/radio-utils/actions/workflows/ci.yml)

Collection of scripts over the years simulating radio communications
(commericial and amateur radio).

```sh
python -m pip install -e .
```

## Rain Attenuation

[**ITU P.838 Specific attenuation model for rain for use in prediction methods**](https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.838-3-200503-I!!PDF-E.pdf)

considers:

-   rain rate [mm/hour]
-   frequency [Hz] 1-1000 GHz
-   polarization: 0 (horiz) 90 (vertical) or elliptical (degrees)
-   elevation angle (degrees)

Show a plot over whole frequency range by setting frequency `-1`. Show
replication of ITU report plots with `-v` option.

## SSB mod/demod

You can use the `-e` option to introduce a "mistuned" receiver
frequency.:

```sh
python scripts/ssbmoddemod.py my.wav
```

## Free Space Loss

1km link at 902MHz with 10mW EIRP transmit power and -85dBm receive
threshold with 0dBi antenna:

```sh
python scripts/free_space_loss.py -h
python scripts/free_space_loss.py 1e3 902e6 10 -85
```
