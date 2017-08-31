#!/usr/bin/env python
req = ['numpy', 'matplotlib', 'scipy', 'nose', 'seaborn']

import pip
try:
    import conda.cli
    conda.cli.main('install', *req)
except ImportError:
    pip.main(['install'] + req)
# %%
from setuptools import setup

setup(name='radioutils',
      packages=['radioutils'],
      author='Michael Hirsch, Ph.D.',
      description=('Low-level radio communications modeling utilities'
                   'including AM, FM, SSB/DSB demodulation of GNU Radio data'),
      url='https://github.com/scivision/radioutils',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python :: 3',
      ],
      install_requires=req,
      version='1.4.0',
      )
