#!/usr/bin/env python
req = ['numpy','matplotlib','scipy','nose','seaborn']

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except ImportError:    
    pip.main(['install'] + req)
# %%
from setuptools import setup

setup(name='radioutils',
      packages=['radioutils'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/radioutils',
      install_requires=req,
      version='1.0',
	  )
