#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception:
    pass

setup(name='radioutils',
	  description='Radio simulation utilities',
	  url='https://github.com/scienceopen/radioutils',
	  install_requires=['pathlib2'],
      packages=['radioutils'],
	  )
