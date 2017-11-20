#!/usr/bin/env python
req = ['numpy', 'scipy', 'nose']
# %%
from setuptools import setup, find_packages

setup(name='radioutils',
      packages=find_packages(),
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
      extras_require={'plot':['matplotlib','seaborn'],
                      'io':['pygame']},
      python_requires='>=3.6',
      )
